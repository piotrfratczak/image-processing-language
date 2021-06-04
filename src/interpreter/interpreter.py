from .scope import ScopeManager
from .visitor import Visitor
from .variables import *
from .builtin_functions import *
from ..lexer.token_type import TokenType
from ..parser.syntax import *
from ..exceptions.exceptions import *


class Interpreter(Visitor):
    def __init__(self, parser):
        self.parser = parser
        self.scope_manager = ScopeManager()

    def interpret(self):
        self.__load_built_in_functions()
        self.parser.parse_program()
        self.parser.program.accept(self)
        return self.__return_result()
        
    def visit_program(self, program: Program):
        main_function = None
        for function_definition in program.function_definitions:
            self.scope_manager.add_function(function_definition.id, function_definition)
            if function_definition.id == 'main':
                main_function = function_definition

        for operator_definition in program.operator_definitions:
            self.scope_manager.add_function(operator_definition.id, operator_definition)

        if main_function is None:
            raise NoMainFunctionException()
        main_function.block.accept(self)

    def visit_block(self, block: Block):
        for statement in block.statements:
            statement.accept(self)
            if self.scope_manager.return_result is not None:
                return

    def visit_if_statement(self, if_statement: IfStatement):
        if_statement.condition.accept(self)
        if self.scope_manager.last_result:
            if_statement.block.accept(self)
        elif if_statement.else_block is not None:
            if_statement.else_block.accept(self)

    def visit_while_loop(self, while_loop: WhileLoop):
        while_loop.condition.accept(self)
        while self.scope_manager.last_result is True:
            while_loop.block.accept(self)
            while_loop.condition.accept(self)

    def visit_for_loop(self, for_loop: ForLoop):
        for_iterator = 0
        for_loop.expression.accept(self)
        if not isinstance(self.scope_manager.last_result, NumberVariable):
            raise ArgumentTypeException(self.scope_manager.last_result.name,
                                        'number', type(self.scope_manager.last_result))

        iterator_variable = self.scope_manager.last_result
        iterator_variable.name = for_loop.iterator

        for_limit = self.scope_manager.last_result.value
        while for_iterator < for_limit:
            iterator_variable.value = for_iterator
            self.scope_manager.add_update_variable(for_loop.iterator, iterator_variable)
            for_loop.block.accept(self)
            for_iterator += 1

    def visit_function_call(self, function_call: FunctionCall):
        name = function_call.id
        function = self.scope_manager.get_function(name)
        function_call.argument_list.accept(self)
        arguments = self.scope_manager.last_result
        self.__execute_function(function, arguments)

    def visit_function_definition(self, function_definition: FunctionDefinition):
        function_definition.block.accept(self)

    def visit_argument_list(self, argument_list: ArgumentList):
        arguments = []
        for expression in argument_list.expressions:
            expression.accept(self)
            arguments.append(self.scope_manager.last_result)
        self.scope_manager.last_result = arguments

    def visit_matrix(self, matrix: Matrix):
        rows = []
        for m_row in matrix.rows:
            m_row.accept(self)
            row = []
            for variable in self.scope_manager.last_result:
                row.append(variable.value)
            rows.append(row)
        self.scope_manager.last_result = MatrixVariable('', rows)

    def visit_matrix3d(self, matrix3d: Matrix3d):
        matrices = []
        for matrix in matrix3d.matrices:
            matrix.accept(self)
            matrices.append(self.scope_manager.last_result)
        self.scope_manager.last_result = Matrix3dVariable('', matrices)

    def visit_expression_in_parenthesis(self, expression_in_parenthesis: ExpressionInParenthesis):
        expression_in_parenthesis.expression.accept(self)

    def visit_base_expression(self, base_expression: BaseExpression):
        if base_expression.subtract_operator:
            sign = -1
        else:
            sign = 1
        if isinstance(base_expression.expression, int):
            self.scope_manager.last_result = NumberVariable('', sign * base_expression.expression)
        elif isinstance(base_expression.expression, str):
            variable = self.scope_manager.get_variable(base_expression.expression)
            self.scope_manager.last_result = copy(variable)
        elif isinstance(base_expression.expression, Matrix) or\
                isinstance(base_expression.expression, Matrix3d) or\
                isinstance(base_expression.expression, InitStatement) or\
                isinstance(base_expression.expression, Reference) or\
                isinstance(base_expression.expression, MatrixLookup) or\
                isinstance(base_expression.expression, FunctionCall) or\
                isinstance(base_expression.expression, ExpressionInParenthesis):
            base_expression.expression.accept(self)
            self.scope_manager.last_result *= NumberVariable('', sign)

    def visit_multiplicative_expression(self, multiplicative_expression: MultiplicativeExpression):
        multiplicative_expression.base_expressions[0].accept(self)
        result = self.scope_manager.last_result
        for operator, expression in zip(multiplicative_expression.multiplicative_operators,
                                        multiplicative_expression.base_expressions[1:]):
            expression.accept(self)
            if operator == TokenType.MULTIPLY:
                result *= self.scope_manager.last_result
            elif operator == TokenType.DIVIDE:
                if self.scope_manager.last_result.has_zero():
                    raise ZeroDivisionException()
                result /= self.scope_manager.last_result
            elif operator == TokenType.MODULO:
                result %= self.scope_manager.last_result
            elif operator == TokenType.SPECIAL_MULTIPLY:
                if not isinstance(result, MatrixVariable) or isinstance(result, Matrix3dVariable):
                    raise IllicitOperatorException(operator, type(result), type(self.scope_manager.last_result))
                result = result.special_multiply(self.scope_manager.last_result)

            if result is None:
                raise IllicitOperatorException(operator, type(result), type(self.scope_manager.last_result))
            self.scope_manager.last_result = result

    def visit_additive_expression(self, additive_expression: AdditiveExpression):
        additive_expression.multiplicative_expressions[0].accept(self)
        result = self.scope_manager.last_result
        for operator, expression in zip(additive_expression.additive_operators,
                                        additive_expression.multiplicative_expressions[1:]):
            expression.accept(self)
            if operator == TokenType.ADD:
                result += self.scope_manager.last_result
            elif operator == TokenType.SUBTRACT:
                result -= self.scope_manager.last_result

            if result is None:
                raise IllicitOperatorException(operator, type(result), type(self.scope_manager.last_result))
            self.scope_manager.last_result = result

    def visit_expression(self, expression: Expression):
        expression.additive_expressions[0].accept(self)
        result = self.scope_manager.last_result
        for operator, additive_expression in zip(expression.new_operators,
                                                 expression.additive_expressions[1:]):
            additive_expression.accept(self)
            operator_function = self.scope_manager.get_function(operator)

            if not (check_type(result, operator_function.type1) and
                    check_type(self.scope_manager.last_result, operator_function.type2)):
                raise TypeMismatchError(result, operator_function.type1, type(result))

            self.__execute_function(operator_function, [result, self.scope_manager.last_result])
            result = self.scope_manager.return_result

    def visit_logical_expression(self, logical_expression: LogicalExpression):
        result = self.scope_manager.last_result
        if isinstance(logical_expression.expression, Condition):
            logical_expression.expression.accept(self)
            if logical_expression.negation_operator:
                result = not result
            self.scope_manager.last_result = result
        else:
            logical_expression.expression.accept(self)
            if logical_expression.negation_operator:
                if isinstance(result, Variable):
                    result = result.evaluate_to_bool()
                self.scope_manager.last_result = not result

    def visit_comparison_condition(self, comparison_condition: ComparisonCondition):
        comparison_condition.logical_expression.accept(self)
        condition1 = self.scope_manager.last_result

        operator = comparison_condition.comparison_operator
        if operator is not None:
            comparison_condition.logical_expression2.accept(self)
            condition2 = self.scope_manager.last_result

            if isinstance(condition1, bool) and isinstance(condition2, Variable):
                condition2 = condition2.evaluate_to_bool()
            if isinstance(condition1, Variable) and isinstance(condition2, bool):
                condition1 = condition1.evaluate_to_bool()

            type1 = type(condition1)
            type2 = type(condition2)
            if type1 != type2:
                raise ComparisonTypeMismatchException(type1, type2, operator)

            if operator == TokenType.EQUAL:
                self.scope_manager.last_result = condition1 == condition2
            elif operator == TokenType.NOT_EQUAL:
                self.scope_manager.last_result = condition1 != condition2
            elif operator == TokenType.GREATER_THAN:
                self.scope_manager.last_result = condition1 > condition2
            elif operator == TokenType.LESS_THAN:
                self.scope_manager.last_result = condition1 < condition2
            elif operator == TokenType.GREATER_OR_EQUAL:
                self.scope_manager.last_result = condition1 >= condition2
            elif operator == TokenType.LESS_OR_EQUAL:
                self.scope_manager.last_result = condition1 <= condition2

        elif isinstance(condition1, Variable):
            self.scope_manager.last_result = condition1.evaluate_to_bool()

    def visit_and_condition(self, and_condition: AndCondition):
        for comparison_condition in and_condition.comparison_conditions:
            comparison_condition.accept(self)
            if not self.scope_manager.last_result:
                return

    def visit_condition(self, condition: Condition):
        for and_condition in condition.and_conditions:
            and_condition.accept(self)
            if self.scope_manager.last_result:
                return

    def visit_init_statement(self, init_statement: InitStatement):
        if init_statement.type == TokenType.NUMBER_TYPE:
            if init_statement.argument_list.length == 0:
                self.scope_manager.last_result = NumberVariable('', 0)

            elif init_statement.argument_list.length == 1:
                init_statement.argument_list.expressions[0].accept(self)
                if not isinstance(self.scope_manager.last_result, NumberVariable):
                    raise ArgumentTypeException(self.scope_manager.last_result.name,
                                                'number', type(self.scope_manager.last_result))

            else:
                raise InvalidArgumentsNumberException("To initialize a number variable input 0 or 1 variable.",
                                                      init_statement.argument_list.length)

        elif init_statement.type == TokenType.PIXEL:
            if init_statement.argument_list.length == 0:
                self.scope_manager.last_result = PixelVariable('')

            elif init_statement.argument_list.length == 1:
                init_statement.argument_list.accept(self)
                arguments = self.scope_manager.last_result
                self.scope_manager.last_result = PixelVariable('',
                                                               arguments[0].value,
                                                               arguments[0].value,
                                                               arguments[0].value)
            elif init_statement.argument_list.length == 3:
                init_statement.argument_list.accept(self)
                arguments = self.scope_manager.last_result
                self.scope_manager.last_result = PixelVariable('',
                                                               arguments[0].value,
                                                               arguments[1].value,
                                                               arguments[2].value)
            else:
                raise InvalidArgumentsNumberException("To initialize a pixel variable input 0 or 1 or 3 variables.",
                                                      init_statement.argument_list.length)

        elif init_statement.type == TokenType.MATRIX:
            if init_statement.argument_list.length == 1:
                init_statement.argument_list.accept(self)
                arguments = self.scope_manager.last_result
                row = [0] * arguments[0].value
                self.scope_manager.last_result = MatrixVariable('', [row])

            elif init_statement.argument_list.length == 2:
                init_statement.argument_list.accept(self)
                arguments = self.scope_manager.last_result
                rows = []
                for i in range(arguments[0].value):
                    rows.append([0] * arguments[1].value)
                self.scope_manager.last_result = MatrixVariable('', rows)

            elif init_statement.argument_list.length == 3:
                init_statement.argument_list.accept(self)
                arguments = self.scope_manager.last_result
                matrices = []
                for m in range(arguments[0].value):
                    rows = []
                    for r in range(arguments[1].value):
                        rows.append([0] * arguments[2].value)

                    matrices.append(MatrixVariable('', rows))
                self.scope_manager.last_result = Matrix3dVariable('', matrices)

            else:
                raise InvalidArgumentsNumberException("To initialize a matrix variable input 0 or 2 or 3 variables.",
                                                      init_statement.argument_list.length)
        else:
            raise InvalidVariableTypeException(init_statement.type)

    def visit_return_statement(self, return_statement: ReturnStatement):
        if return_statement.expression is None:
            self.scope_manager.return_result = None
        else:
            return_statement.expression.accept(self)
            self.scope_manager.return_result = self.scope_manager.last_result

    def visit_operator_definition(self, operator_definition: OperatorDefinition):
        operator_definition.block.accept(self)

    def visit_assignment(self, assignment: Assignment):
        assignment.expression.accept(self)
        if assignment.reference is not None:
            return_result = self.scope_manager.return_result
            self.scope_manager.return_result = self.scope_manager.last_result.value
            assignment.reference.accept(self)
            self.scope_manager.return_result = return_result

        if assignment.matrix_lookup is not None:
            return_result = self.scope_manager.return_result
            self.scope_manager.return_result = self.scope_manager.last_result.value
            assignment.matrix_lookup.accept(self)
            self.scope_manager.return_result = return_result

        if assignment.id is not None:
            self.scope_manager.last_result.name = assignment.id
            self.scope_manager.add_update_variable(assignment.id, self.scope_manager.last_result)

    def visit_reference(self, reference: Reference):
        reference_result = None
        variable = self.scope_manager.get_variable(reference.id1)
        if isinstance(variable, PixelVariable):
            pixel = variable
            if reference.id2 == 'r':
                if isinstance(self.scope_manager.return_result, int):
                    # value assigned to pixel channel
                    pixel.set_r(self.scope_manager.return_result)
                    reference_result = pixel
                else:
                    # pixel channel value assigned to variable
                    reference_result = NumberVariable('', pixel.r)
            elif reference.id2 == 'g':
                if isinstance(self.scope_manager.return_result, int):
                    # value assigned to pixel channel
                    pixel.set_g(self.scope_manager.return_result)
                    reference_result = pixel
                else:
                    # pixel channel value assigned to variable
                    reference_result = NumberVariable('', pixel.g)
            elif reference.id2 == 'b':
                if isinstance(self.scope_manager.return_result, int):
                    # value assigned to pixel channel
                    pixel.set_b(self.scope_manager.return_result)
                    reference_result = pixel
                else:
                    # pixel channel value assigned to variable
                    reference_result = NumberVariable('', pixel.b)

        elif isinstance(variable, MatrixVariable) or isinstance(variable, Matrix3dVariable):
            matrix = variable
            if reference.id2 == 'xdim':
                reference_result = NumberVariable('', matrix.xdim)
            elif reference.id2 == 'ydim':
                reference_result = NumberVariable('', matrix.ydim)
            elif reference.id2 == 'zdim' and isinstance(matrix, Matrix3dVariable):
                reference_result = NumberVariable('', matrix.zdim)
            elif reference.id2 == 'dims':
                if isinstance(matrix, MatrixVariable):
                    reference_result = NumberVariable('', 2)
                else:
                    reference_result = NumberVariable('', 3)

        if reference_result is not None:
            self.scope_manager.last_result = reference_result
        else:
            raise UndefinedReferenceException(reference.id2)

    def visit_matrix_lookup(self, matrix_lookup: MatrixLookup):
        indices = []
        for index in matrix_lookup.indices:
            index.accept(self)
            indices.append(self.scope_manager.last_result.value)

        matrix = self.scope_manager.get_variable(matrix_lookup.id)

        if isinstance(matrix, MatrixVariable):
            if len(indices) != 2:
                raise InvalidArgumentsNumberException("To look up matrix value use 2 indices.", len(indices))
            if indices[0] >= matrix.ydim or indices[1] >= matrix.xdim:
                raise IndexOutOfRangeError()
            if isinstance(self.scope_manager.return_result, int):
                # value assigned to matrix field
                matrix.rows[indices[0]][indices[1]] = self.scope_manager.return_result
                self.scope_manager.last_result = matrix
            else:
                # matrix field value assigned to variable
                self.scope_manager.last_result = NumberVariable('', matrix.rows[indices[0]][indices[1]])
        if isinstance(matrix, Matrix3dVariable):
            if len(indices) != 3:
                raise InvalidArgumentsNumberException("To look up matrix value use 3 indices.", len(indices))
            if indices[0] >= matrix.zdim or indices[1] >= matrix.ydim or indices[2] >= matrix.xdim:
                raise IndexOutOfRangeError()
            if isinstance(self.scope_manager.return_result, int):
                # value assigned to matrix field
                matrix.matrices[indices[0]].rows[indices[1]][indices[2]] = self.scope_manager.return_result
                self.scope_manager.last_result = matrix
            else:
                # matrix field value assigned to variable
                self.scope_manager.last_result = \
                    NumberVariable('', matrix.matrices[indices[0]].rows[indices[1]][indices[2]])

    def __execute_function(self, function, arguments):
        if not function.verify_arguments(arguments):
            raise InvalidArgumentsNumberException("To call " + function.id + " " + len(function.parameter_list) +
                                                  "arguments were expected.", len(arguments))
        self.scope_manager.switch_to_new_scope(function.id)
        for argument, parameter in zip(arguments, function.parameter_list):
            self.scope_manager.add_variable(parameter, argument)
        function.accept(self)
        self.scope_manager.switch_to_previous_scope()

    def __load_built_in_functions(self):
        builtin_functions = [PrintFunction(), RandomPixelFunction(), DeterminantFunction()]
        for function_definition in builtin_functions:
            self.scope_manager.add_function(function_definition.id, function_definition)

    def __return_result(self):
        if self.scope_manager.last_result is None:
            return 0

        if isinstance(self.scope_manager.last_result, NumberVariable):
            return self.scope_manager.last_result.value
        if self.scope_manager.last_result is not False:
            return 0
        return -1


def check_type(variable, expected_type):
    return (isinstance(variable, NumberVariable) and expected_type == TokenType.NUMBER_TYPE) or \
           (isinstance(variable, PixelVariable) and expected_type == TokenType.PIXEL) or \
           (isinstance(variable, MatrixVariable) and expected_type == TokenType.MATRIX)
