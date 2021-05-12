from src.lexer.token_type import TokenType
from .syntax import *
from ..exceptions.exceptions import SyntaxError


class Parser:
    def __init__(self, lexer):
        self.program = None
        self.__lexer = lexer
        self._token = None
        self.get_next_token()

    def parse_program(self):
        function_definitions = []
        comments = []

        definition = self.parse_function_definition()
        while definition or self._token.type == TokenType.COMMENT:
            if definition:
                function_definitions.append(definition)
            else:
                comments.append(self._token.value)
                self.get_next_token()
            definition = self.parse_function_definition()
        self.program = Program(function_definitions, comments)

    def parse_function_definition(self):
        if self._token.type != TokenType.ID:
            return None

        _id = self._token.value
        self.get_next_token()
        if self._token.type == TokenType.L_PARENTHESIS:
            self.get_next_token()
            parameters = self.parse_parameter_list()
            if parameters:
                #ExceptionIfNot(TokenType.R_PARENTHESIS, "Brk ....")
                #refaktoryzacja -> w każdej linijce albo dalej albo exception jap f. poniżej
                if self._token.type == TokenType.R_PARENTHESIS:
                    self.get_next_token()
                    block = self.parse_block()
                    if block:
                        if isinstance(block.statements[-1], ReturnStatement):
                            self.get_next_token()
                            return FunctionDefinition(_id, block, parameters)
        self.raise_syntax_error()

    def parse_statement(self):
        statement = self.parse_operator_definition()
        if statement:
            return statement
        statement = self.parse_for_loop()
        if statement:
            return statement
        statement = self.parse_while_loop()
        if statement:
            return statement
        statement = self.parse_if_statement()
        if statement:
            return statement
        statement = self.parse_return_statement()
        if statement:
            return statement
        statement = self.parse_assignment_or_call()
        if statement:
            return statement
        if self._token.type == TokenType.COMMENT:
            comment = self._token.value
            self.get_next_token()
            return comment
        return None

    def parse_reference_or_call(self):
        if self._token.type != TokenType.ID:
            _id = self._token.value
            self.get_next_token()

            matrix_lookup = self.parse_matrix_lookup(_id)
            if matrix_lookup:
                return matrix_lookup
            reference = self.parse_reference(_id)
            if reference:
                return reference
            function_call = self.parse_function_call(_id)
            if function_call:
                return function_call
            return None

    def parse_function_call(self, _id):
        if self._token.type == TokenType.L_PARENTHESIS:
            self.get_next_token()
            arguments = self.parse_argument_list()
            if arguments:
                if self._token.type == TokenType.R_PARENTHESIS:
                    self.get_next_token()
                    return FunctionCall(_id, arguments)
        return None

    def parse_argument_list(self):
        expressions = []
        expression = self.parse_expression()
        if expression:
            expressions.append(expression)
            while self._token.type == TokenType.COMMA:
                self.get_next_token()
                expression = self.parse_expression()
                if expression:
                    expressions.append(expression)
                else:
                    self.raise_syntax_error()
        return ArgumentList(expressions)

    def parse_if_statement(self):
        if self._token.type == TokenType.IF:
            blocks = []
            self.get_next_token()
            if self._token.type == TokenType.L_PARENTHESIS:
                self.get_next_token()
                condition = self.parse_condition()
                if condition:
                    if self._token.type == TokenType.R_PARENTHESIS:
                        self.get_next_token()
                        block = self.parse_block()
                        if block:
                            blocks.append(block)
                            while self._token.type == TokenType.ELSE:
                                self.get_next_token()
                                block = self.__lexer.parse_block()
                                if block:
                                    blocks.append(block)
                                else:
                                    self.raise_syntax_error()
                            return IfStatement(condition, blocks)

            self.raise_syntax_error()
        return None

    def parse_init_statement(self):
        _type = self._token.type
        if _type == TokenType.NUMBER or _type == TokenType.PIXEL or _type == TokenType.MATRIX:
            self.get_next_token()
            if self._token.type == TokenType.L_PARENTHESIS:
                self.get_next_token()
                arguments = self.parse_argument_list()
                if arguments:
                    if self._token.type == TokenType.R_PARENTHESIS:
                        self.get_next_token()
                        if self._token.type == TokenType.SEMICOLON:
                            self.get_next_token()
                            return InitStatement(_type, arguments)
            self.raise_syntax_error()
        return None

    def parse_return_statement(self):
        if self._token.type == TokenType.RETURN:
            self.get_next_token()
            expression = self.parse_expression()
            if self._token.type == TokenType.SEMICOLON:
                return ReturnStatement(expression)
            self.raise_syntax_error()
        return None

    def parse_block(self):
        if self._token.type == TokenType.L_BRACE:
            self.get_next_token()
            statements = []
            statement = self.parse_statement()
            while statement:
                statements.append(statement)
                statement = self.parse_statement()
            if len(statements) > 0:
                if self._token.type == TokenType.R_BRACE:
                    self.get_next_token()
                    return Block(statements)
            self.raise_syntax_error()
        else:
            statement = self.parse_statement()
            if statement:
                return Block([statement])
        return None

    def parse_assignment_or_call(self):
        if self._token.type == TokenType.ID:
            _id = self._token.value
            self.get_next_token()

            function_call = self.parse_function_call(_id)
            if function_call:
                if self._token.type == TokenType.SEMICOLON:
                    self.get_next_token()
                    return function_call
                self.raise_syntax_error()

            reference = self.parse_reference(_id)
            assignment = self.parse_assignment(_id, reference)
            if assignment:
                if self._token.type == TokenType.SEMICOLON:
                    self.get_next_token()
                    return assignment
            self.raise_syntax_error()
        return None

    def parse_reference(self, id1):
        if self._token.type == TokenType.DOT:
            self.get_next_token()
            if self._token.type == TokenType.ID:
                id2 = self._token.value
                self.get_next_token()
                return Reference(id1, id2)
            self.raise_syntax_error()
        return None

    def parse_assignment(self, _id=None, reference=None):
        if self._token.type == TokenType.ASSIGN:
            self.get_next_token()
            expression = self.parse_expression()
            if expression:
                return Assignment(expression, _id, reference)
            self.raise_syntax_error()
        return None

    def parse_matrix_lookup(self, _id):
        if self._token.type == TokenType.L_BRACKET:
            self.get_next_token()
            expressions = []
            expression = self.parse_expression()
            if expression:
                expressions.append(expression)
                while self._token.type == TokenType.COMMA:
                    self.get_next_token()
                    expression = self.parse_expression()
                    if expression:
                        expressions.append(expression)
                    else:
                        self.raise_syntax_error()
                if self._token.type == TokenType.R_BRACKET:
                    self.get_next_token()
                    return MatrixLookup(_id, expressions)
            self.raise_syntax_error()
        return None

    def parse_operator_definition(self):
        if self._token.type == TokenType.NEW_OPERATOR:
            self.get_next_token()
            if self._token.type == TokenType.L_PARENTHESIS:
                self.get_next_token()
                if self._token.type == TokenType.ID:
                    id1 = self._token.value
                    self.get_next_token()
                    if self._token.type == TokenType.OF:
                        self.get_next_token()
                        type1 = self._token.type
                        if type1 == TokenType.NUMBER or type1 == TokenType.PIXEL or type1 == TokenType.MATRIX:
                            self.get_next_token()
                            if self._token.type == TokenType.COMMA:
                                self.get_next_token()
                                if self._token.type == TokenType.ID:
                                    id2 = self._token.value
                                    self.get_next_token()
                                    if self._token.type == TokenType.OF:
                                        self.get_next_token()
                                        type2 = self._token.type
                                        if type2 == TokenType.NUMBER or type2 == TokenType.PIXEL \
                                                or type2 == TokenType.MATRIX:
                                            self.get_next_token()
                                            if self._token.type == TokenType.R_PARENTHESIS:
                                                self.get_next_token()
                                                block = self.parse_block()
                                                if block:
                                                    return OperatorDefinition(id1, type1, id2, type2, block)
            self.raise_syntax_error()
        return None

    def parse_for_loop(self):
        if self._token.type == TokenType.FOR:
            self.get_next_token()
            if self._token.type == TokenType.L_PARENTHESIS:
                self.get_next_token()
                if self._token.type == TokenType.ID:
                    _id = self._token.value
                    self.get_next_token()
                    if self._token.type == TokenType.IN:
                        self.get_next_token()
                        expression = self.parse_expression()
                        if expression:
                            if self._token.type == TokenType.R_PARENTHESIS:
                                self.get_next_token()
                                block = self.parse_block()
                                if block:
                                    return ForLoop(_id, expression, block)
            self.raise_syntax_error()
        return None

    def parse_while_loop(self):
        if self._token.type == TokenType.WHILE:
            self.get_next_token()
            if self._token.type == TokenType.L_PARENTHESIS:
                self.get_next_token()
                condition = self.parse_condition()
                if condition:
                    if self._token.type == TokenType.R_PARENTHESIS:
                        self.get_next_token()
                        block = self.parse_block()
                        if block:
                            return WhileLoop(condition, block)
            self.raise_syntax_error()
        return None

    def parse_matrix3d(self):
        if self._token.type == TokenType.L_BRACE:
            self.get_next_token()
            matrices = []
            matrix = self.parse_matrix()
            if matrix:
                matrices.append(matrix)
                while self._token.type == TokenType.COMMA:
                    self.get_next_token()
                    matrix = self.parse_matrix()
                    if matrix:
                        matrices.append(matrix)
                    else:
                        self.raise_syntax_error()
                if self._token.type == TokenType.R_BRACE:
                    self.get_next_token()
                    return Matrix3d(matrices)
            self.raise_syntax_error()
        return None

    # { [1,2,3; 2,3,4;], [] }

    def parse_matrix(self):
        if self._token.type == TokenType.L_BRACKET:
            self.get_next_token()
            rows = []
            row = self.parse_argument_list()
            while row:
                if self._token.type == TokenType.SEMICOLON:
                    self.get_next_token()
                    rows.append(row)
                else:
                    self.raise_syntax_error()
                row = self.parse_argument_list()
            if len(rows) > 0:
                if self._token.type == TokenType.R_BRACKET:
                    self.get_next_token()
                    return Matrix(rows)

    def parse_expression(self):
        expression = self.parse_multiplicative_expression()
        if expression is None:
            return None
        expressions = []
        operators = []
        expressions.append(expression)
        operator = self._token.type
        while operator == TokenType.ADD or operator == TokenType.SUBTRACT:
            self.get_next_token()
            expression = self.parse_multiplicative_expression()
            if expression:
                operators.append(operator)
                expressions.append(expression)
            else:
                self.raise_syntax_error()
            operator = self._token.type
        if len(operators) == 0:
            return expressions[0]
        else:
            return Expression(expressions, operators)


    def parse_multiplicative_expression(self):
        expression = self.parse_base_expression()
        if expression is None:
            return None
        expressions = []
        operators = []
        expressions.append(expression)
        operator = self._token.type
        while operator == TokenType.MULTIPLY or operator == TokenType.DIVIDE:
            self.get_next_token()
            expression = self.parse_base_expression()
            if expression:
                operators.append(operator) # dodawanie do listy razem
                expressions.append(expression)
            else:
                self.raise_syntax_error()
            operator = self._token.type
        if len(operators) == 0:
            return expressions[0]
        else:
            return Expression(expressions, operators)


    def parse_base_expression(self):
        subtraction = self._token.type == TokenType.SUBTRACT
        if subtraction:
            self.get_next_token()
        expression = self.parse_expression_in_parenthesis()
        if expression:
            return BaseExpression(subtraction, expression_in_parenthesis=expression)
        if self._token.type == TokenType.NUMBER:
            number = self._token.value
            self.get_next_token()
            return BaseExpression(subtraction, number=number)
        matrix = self.parse_matrix()
        if matrix:
            return BaseExpression(subtraction, matrix=matrix)
        matrix3d = self.parse_matrix3d()
        if matrix3d:
            return BaseExpression(subtraction, matrix3d=matrix3d)
        init_statement = self.parse_init_statement()
        if init_statement:
            return BaseExpression(subtraction, init_statement=init_statement)
        reference_or_call = self.parse_reference_or_call()
        if reference_or_call:
            return BaseExpression(subtraction, reference_or_call=reference_or_call)
        if subtraction:
            self.raise_syntax_error()
        return None

    def parse_expression_in_parenthesis(self):
        if self._token.type == TokenType.L_PARENTHESIS:
            self.get_next_token()
            expression = self.parse_expression()
            if expression:
                if self._token.type == TokenType.R_PARENTHESIS:
                    self.get_next_token()
                    return ExpressionInParenthesis(expression)
            self.raise_syntax_error()
        return None

    def parse_condition(self):
        condition = self.parse_and_condition()
        if condition:
            conditions = []
            conditions.append(condition)
            while self._token.type == TokenType.OR:
                self.get_next_token()
                condition = self.parse_and_condition()
                if condition:
                    conditions.append(condition)
                else:
                    self.raise_syntax_error()
            return Condition(conditions)
        return None

    def parse_and_condition(self):
        condition = self.parse_equality_condition()
        if condition:
            conditions = [condition]
            while self._token.type == TokenType.AND:
                self.get_next_token()
                condition = self.parse_equality_condition()
                if condition:
                    conditions.append(condition)
                else:
                    self.raise_syntax_error()
            return AndCondition(conditions)
        return None

    def parse_equality_condition(self):
        condition1 = self.parse_relation_condition()
        if condition1:
            operator = self._token.type
            if operator == TokenType.EQUAL or operator == TokenType.NOT_EQUAL:
                self.get_next_token()
                condition2 = self.parse_relation_condition()
                if not condition2:
                    self.raise_syntax_error()
            return EqualityCondition(condition1, operator, condition2)
        return None

    def parse_relation_condition(self):
        condition1 = self.parse_base_condition()
        if condition1:
            operator = self._token.type
            if operator == TokenType.LESS_THAN or operator == TokenType.LESS_OR_EQUAL \
                    or operator == TokenType.GREATER_THAN or operator == TokenType.GREATER_OR_EQUAL:
                self.get_next_token()
                condition2 = self.parse_base_condition()
                if not condition2:
                    self.raise_syntax_error()
            return EqualityCondition(condition1, operator, condition2)
        return None

    def parse_base_condition(self):
        negation = self._token.type == TokenType.NOT
        if negation:
            self.get_next_token()
        condition = self.parse_condition_in_parenthesis()
        if condition:
            return BaseCondition(negation, condition_in_parenthesis=condition)
        expression = self.parse_expression()
        if expression:
            return BaseCondition(negation, expression=expression)
        if negation:
            self.raise_syntax_error()
        return None

    def parse_condition_in_parenthesis(self):
        if self._token.type == TokenType.L_PARENTHESIS:
            self.get_next_token()
            condition = self.parse_condition()
            if condition:
                if self._token.type == TokenType.R_PARENTHESIS:
                    self.get_next_token()
                    return ConditionInParenthesis(condition)
            self.raise_syntax_error()
        return None

    def raise_syntax_error(self):
        raise SyntaxError(self.__lexer.token_start_position, self.__lexer.token_start_byte)

    def get_next_token(self):
        self._token = self.__lexer.get_next_token()
