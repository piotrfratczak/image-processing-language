from copy import copy
from .visitor import *
from .scope import ScopeManager
from ..exceptions.exceptions import *


class Interpreter(Visitor):
    def __init__(self, parser):
        self.parser = parser
        self.scope_manager = ScopeManager()

    def interpret(self):
        self.parser.parse_program()
        self.parser.program.accept(self)
        
    def visit_program(self, program: Program):
        main_function = None
        for function_definition in program.function_definitions:
            function_definition.accept(self)
            if function_definition.id == 'main':
                main_function = function_definition

        for operator_definition in program.operator_definitions:
            operator_definition.accept(self)

        for comment in program.comments:
            comment.accept(self)

        if main_function is None:
            raise NoMainFunctionException()
        main_function.block.accept(self)

    def visit_function_definition(self, function_definition: FunctionDefinition):
        self.scope_manager.add_function(function_definition.id, function_definition)

    def visit_block(self, block: Block):
        for statement in block.statements:
            statement.accept(self)
            if self.scope_manager.return_result is not None:
                return

    def visit_if_statement(self, if_statement: IfStatement):
        if_statement.condition.accept(self)
        if self.scope_manager.last_result:
            if_statement.block.accept(self)
        else:
            if_statement.else_block.accept(self)

    def visit_while_loop(self, while_loop: WhileLoop):
        while_condition = while_loop.condition.accept(self)
        while while_condition:
            while_loop.block.accept(self)
            while_condition = while_loop.condition.accept(self)

    def visit_for_loop(self, for_loop: ForLoop):
        for_iterator = 0
        for_limit = for_loop.expression.accept(self)
        while for_iterator < for_limit:
            for_loop.block.accept(self)
            for_iterator += 1

    def visit_function_call(self, function_call: FunctionCall):
        name = function_call.id
        function = self.scope_manager.get_function(name)
        function_call.argument_list.accept(self)
        arguments = self.scope_manager.last_result
        self.execute_function(function, arguments)

    def visit_argument_list(self, argument_list: ArgumentList):
        arguments = []
        for expression in argument_list.expressions:
            expression.accept(self)
            arguments.append(self.scope_manager.last_result)
        self.scope_manager.last_result = arguments

    def visit_matrix(self, matrix: Matrix):
        matrix.rows[0].accept(self)
        first_row = self.scope_manager.last_result
        row_length = len(first_row)
        rows = [first_row]
        for row in matrix.rows[1:]:
            row.accept(self)
            next_row = self.scope_manager.last_result
            if not len(next_row) == row_length:
                raise MatrixDimensionsException()
            rows.append(next_row)
        self.scope_manager.last_result = MatrixVariable('', rows)

    def visit_matrix3d(self, matrix3d: Matrix3d):
        matrices = []
        for matrix in matrix3d.matrices:
            matrix.accept(self)
            matrices.append(self.scope_manager.last_result)
        self.scope_manager.last_result = matrices

    def visit_expression_in_parenthesis(self, expression_in_parenthesis: ExpressionInParenthesis):
        expression_in_parenthesis.expression.accept(self)

    def visit_base_expression(self, base_expression: BaseExpression):
        if base_expression.expression:
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
            self.scope_manager.last_result.value *= sign

    def visit_multiplicative_expression(self, multiplicative_expression: MultiplicativeExpression):
        multiplicative_expression.base_expressions[0].accept(self)
        result = self.scope_manager.last_result
        for operator, expression in zip(multiplicative_expression.multiplicative_operators,
                                        multiplicative_expression.base_expressions[1:]):
            expression.accept(self)
            if operator == TokenType.MULTIPLY:
                result.value *= self.scope_manager.last_result.value
            elif operator == TokenType.DIVIDE:
                result.value /= self.scope_manager.last_result.value
            elif operator == TokenType.SPECIAL_MULTIPLY:
                if not isinstance(result, Matrix) and isinstance(self.scope_manager.last_result, Matrix):
                    raise IllicitOperatorException()
                # TODO multiply matrices in the special way
            self.scope_manager.last_result = result

    def visit_additive_expression(self, additive_expression: AdditiveExpression):
        additive_expression.multiplicative_expressions[0].accept(self)
        result = self.scope_manager.last_result
        for operator, expression in zip(additive_expression.additive_operators,
                                        additive_expression.multiplicative_expressions[1:]):
            expression.accept(self)
            if operator == TokenType.ADD:
                result.value += self.scope_manager.last_result.value
            elif operator == TokenType.SUBTRACT:
                result.value -= self.scope_manager.last_result.value
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
                raise TypeMismatchError(operator)

            self.execute_function(operator_function, [result, self.scope_manager.last_result])
            result = self.scope_manager.return_result

    def visit_condition_in_parenthesis(self, condition_in_parenthesis: ConditionInParenthesis):
        condition_in_parenthesis.condition.accept(self)

    def visit_base_condition(self, base_condition: BaseCondition):
        if isinstance(base_condition.expression, Condition):
            base_condition.expression.accept(self)
            result = self.scope_manager.last_result
            if base_condition.negation_operator:
                result = not result
            self.scope_manager.last_result = result
        elif isinstance(base_condition.expression, Expression):
            base_condition.expression.accept(self)
            if base_condition.negation_operator:
                self.scope_manager.last_result = not self.scope_manager.last_result.evaluate_to_bool()

    def visit_comparison_condition(self, comparison_condition: ComparisonCondition):
        comparison_condition.base_condition.accept(self)
        condition1 = self.scope_manager.last_result

        operator = comparison_condition.comparison_operator
        if operator is not None:
            comparison_condition.base_condition2.accept(self)
            condition2 = self.scope_manager.last_result

            if isinstance(condition1, bool) and isinstance(condition2, Variable):
                condition2 = condition2.evaluate_to_bool()
            if isinstance(condition1, Variable) and isinstance(condition2, bool):
                condition1 = condition1.evaluate_to_bool()

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
        # TODO
        if init_statement.type == TokenType.NUMBER_TYPE:
            if init_statement.argument_list.length == 0:
                self.scope_manager.last_result = NumberVariable('', 0)
            elif init_statement.argument_list.length == 1:
                value = init_statement.argument_list.expressions[0].accept(self)
                if not isinstance(value, int):
                    raise ArgumentTypeException()
                self.scope_manager.last_result =  NumberVariable('', value)
            else:
                raise InvalidArgumentsNumberException()

        elif init_statement.type == TokenType.PIXEL:
            if init_statement.argument_list.length == 0:
                self.scope_manager.last_result =  PixelVariable('')
            elif init_statement.argument_list.length == 3:
                self.scope_manager.last_result = PixelVariable('',
                                                               init_statement.argument_list.expressions[0],
                                                               init_statement.argument_list.expressions[1],
                                                               init_statement.argument_list.expressions[2])
            else:
                raise InvalidArgumentsNumberException()

        elif init_statement.type == TokenType.MATRIX:
            return
        raise InvalidVariableTypeException()

    def visit_return_statement(self, return_statement: ReturnStatement):
        return_statement.expression.accept(self)
        self.scope_manager.return_result = self.scope_manager.last_result

    def visit_operator_definition(self, operator_definition: OperatorDefinition):
        self.scope_manager.add_function(operator_definition.operator, operator_definition)

    def visit_assignment(self, assignment: Assignment):
        assignment.expression.accept(self)
        if assignment.id is not None:
            self.scope_manager.last_result.name = assignment.id
            self.scope_manager.update_variable(assignment.id, self.scope_manager.last_result)
        elif assignment.reference is not None:
            #  TODO

    def visit_reference(self, reference: Reference):
        # TODO
        self.scope_manager.last_result = reference

    def visit_matrix_lookup(self, matrix_lookup: MatrixLookup):
        indices = []
        for index in matrix_lookup.indices:
            index.accept(self)
            indices.append(self.scope_manager.last_result)

    def execute_function(self, function, arguments):
        if function.id == 'print':
            result_string = ''
            for argument in arguments:
                result_string += str(argument)
            print(result_string)
        else:
            if len(arguments) != len(function.parameter_list):
                raise InvalidArgumentsNumberException()
            self.scope_manager.switch_to_new_scope(function)
            for argument, parameter in zip(arguments, function.parameter_list):
                self.scope_manager.add_variable(parameter, argument)
            function.block.accept(self)
            self.scope_manager.switch_to_parent_scope()
