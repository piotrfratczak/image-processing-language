from src.lexer.token_type import TokenType
from .syntax import *
from ..exceptions.exceptions import SyntaxException


class Parser:
    def __init__(self, lexer):
        self.program = None
        self.__lexer = lexer
        self._token = None
        self._comments = []
        self.get_next_token()

    def parse_program(self):
        function_definitions = []
        operator_definitions = []

        function_definition = self.parse_function_definition()
        operator_definition = self.parse_operator_definition()
        while function_definition or operator_definition:
            if function_definition:
                function_definitions.append(function_definition)
            if operator_definition:
                operator_definitions.append(operator_definition)

            function_definition = self.parse_function_definition()
            operator_definition = self.parse_operator_definition()

        self.program = Program(function_definitions, operator_definitions, self._comments)

    def parse_function_definition(self):
        id_token = self.parse_next_token(TokenType.ID)
        if not id_token:
            return None

        self.try_or_exception(TokenType.L_PARENTHESIS, "Function definition is missing an opening parenthesis")
        parameters = []
        parameter = self.parse_next_token(TokenType.ID)
        if parameter:
            parameters = [parameter.value]
            while self.parse_next_token(TokenType.COMMA):
                parameter = self.try_or_exception(TokenType.ID,
                                                  "Function definition is missing another parameter after ','")
                parameters.append(parameter.value)
        self.try_or_exception(TokenType.R_PARENTHESIS, "Function definition is missing a closing parenthesis")
        block = self.parse_block()
        self.try_or_exception(block, "Function definition is missing its body")
        self.try_or_exception(isinstance(block.statements[-1], ReturnStatement),
                              "Function body is missing a return statement at the end")
        return FunctionDefinition(id_token.value, parameters, block)

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

        return None

    def parse_reference_or_call(self):
        id_token = self.parse_next_token(TokenType.ID)
        if not id_token:
            return None

        _id = id_token.value
        matrix_lookup = self.parse_matrix_lookup(_id)
        if matrix_lookup:
            return matrix_lookup
        reference = self.parse_reference(_id)
        if reference:
            return reference
        function_call = self.parse_function_call(_id)
        if function_call:
            return function_call
        return _id

    def parse_function_call(self, _id):
        if not self.parse_next_token(TokenType.L_PARENTHESIS):
            return None

        arguments = self.parse_argument_list()
        self.try_or_exception(arguments, "Unexpected arguments in a function call")
        self.try_or_exception(TokenType.R_PARENTHESIS, "Function call missing right parenthesis")
        return FunctionCall(_id, arguments)

    def parse_argument_list(self):
        expressions = []
        expression = self.parse_expression()
        if expression:
            expressions.append(expression)
            while self.parse_next_token(TokenType.COMMA):
                expression = self.parse_expression()
                self.try_or_exception(expression, "Unexpected ',' without following arguments in an argument list")
                expressions.append(expression)
        return ArgumentList(expressions)

    def parse_if_statement(self):
        if not self.parse_next_token(TokenType.IF):
            return None

        self.try_or_exception(TokenType.L_PARENTHESIS, "If statement is missing an opening parenthesis")
        condition = self.parse_condition()
        self.try_or_exception(condition, "If statement is missing a condition")
        self.try_or_exception(TokenType.R_PARENTHESIS, "If statement is missing a closing parenthesis")
        block = self.parse_block()
        self.try_or_exception(block, "If statement is missing instructions to execute")
        if self.parse_next_token(TokenType.ELSE):
            else_block = self.parse_block()
            self.try_or_exception(block, "If statement is missing alternative instructions to execute after else")
            return IfStatement(condition, block, else_block)
        return IfStatement(condition, block)

    def parse_init_statement(self):
        _type = self.parse_type()
        if not _type:
            return None

        self.get_next_token()
        self.try_or_exception(TokenType.L_PARENTHESIS,
                              "Initiation of a variable is missing an opening parenthesis after {}".format(_type))
        arguments = self.parse_argument_list()
        self.try_or_exception(arguments, "Initiation of a variable is missing arguments")
        self.try_or_exception(TokenType.R_PARENTHESIS, "Initiation of a variable is missing a closing parenthesis")
        self.try_or_exception(TokenType.SEMICOLON, "Initiation of a variable is missing a semicolon a the end")
        return InitStatement(_type, arguments)

    def parse_return_statement(self):
        if not self.parse_next_token(TokenType.RETURN):
            return None

        expression = self.parse_expression()
        self.try_or_exception(TokenType.SEMICOLON, "Missing a semicolon after a return statement")
        return ReturnStatement(expression)

    def parse_block(self):
        if self.parse_next_token(TokenType.L_BRACE):
            statements = []
            statement = self.parse_statement()
            while statement:
                statements.append(statement)
                statement = self.parse_statement()
            self.try_or_exception(len(statements) > 0, "Empty block")
            self.try_or_exception(TokenType.R_BRACE, "Block is missing a closing brace")
            return Block(statements)
        else:
            statement = self.parse_statement()
            if statement:
                return Block([statement])
        return None

    def parse_assignment_or_call(self):
        token = self.parse_next_token(TokenType.ID)
        if not token:
            return None

        _id = token.value
        function_call = self.parse_function_call(_id)
        if function_call:
            self.try_or_exception(TokenType.SEMICOLON, "No semicolon after a function definition")
            return function_call

        reference = self.parse_reference(_id)
        assignment = self.parse_assignment(_id, reference)
        self.try_or_exception(assignment, "{} is not a part of any function definition nor any assignment".format(_id))
        self.try_or_exception(TokenType.SEMICOLON, "No semicolon after an assignment")
        return assignment

    def parse_reference(self, id1):
        if not self.parse_next_token(TokenType.DOT):
            return None

        id2_token = self.try_or_exception(TokenType.ID, "No identifier after {}.".format(id1))
        id2 = id2_token.value
        return Reference(id1, id2)

    def parse_assignment(self, _id=None, reference=None):
        if not self.parse_next_token(TokenType.ASSIGN):
            return None

        expression = self.parse_expression()
        self.try_or_exception(expression, "Assignment is missing assigned value")
        if reference:
            return Assignment(expression, reference=reference)
        return Assignment(expression, _id=_id)

    def parse_matrix_lookup(self, _id):
        if not self.parse_next_token(TokenType.L_BRACKET):
            return None

        expression = self.parse_expression()
        self.try_or_exception(expression, "No value specified to look up matrix field")
        expressions = [expression]
        while self.parse_next_token(TokenType.COMMA):
            expression = self.parse_expression()
            self.try_or_exception(expression, "No other index after a coma in a matrix lookup")
            expressions.append(expression)
        self.try_or_exception(TokenType.R_BRACKET, "Missing closing bracket to look up matrix field")
        return MatrixLookup(_id, expressions)

    def parse_operator_definition(self):
        if not self.parse_next_token(TokenType.NEW_OPERATOR):
            return None

        self.try_or_exception(TokenType.L_PARENTHESIS, "Operator definition is missing an opening parenthesis")
        operator_token = self.try_or_exception(TokenType.ID, "Operator definition is missing the defined operator")
        operator = operator_token.value
        self.try_or_exception(TokenType.COMMA, "Operator definition is missing a comma after the new operator")
        id1_token = self.try_or_exception(TokenType.ID, "Operator definition is missing a name for the first variable")
        id1 = id1_token.value
        self.try_or_exception(TokenType.OF, "Operator definition is missing the 'of' keyword")
        type1 = self.parse_type()
        self.try_or_exception(type1, "No type was specified for the first operand in operator definition")
        self.try_or_exception(TokenType.COMMA, "Operator definition is missing a coma separating the two operands")
        id2_token = self.try_or_exception(TokenType.ID, "Operator definition is missing a name for the second variable")
        id2 = id2_token.value
        self.try_or_exception(TokenType.OF, "Operator definition is missing the 'of' keyword")
        type2 = self.parse_type()
        self.try_or_exception(type2, "No type was specified for the second operand in operator definition")
        self.try_or_exception(TokenType.R_PARENTHESIS, "Operator definition is missing a closing parenthesis")
        block = self.parse_block()
        self.try_or_exception(block, "Operator definition is missing the definition of the intended behavior")
        return OperatorDefinition(operator, id1, type1, id2, type2, block)

    def parse_for_loop(self):
        if not self.parse_next_token(TokenType.FOR):
            return None

        self.try_or_exception(TokenType.L_PARENTHESIS, "For loop is missing an opening parenthesis after 'for' keyword")
        id_token = self.try_or_exception(TokenType.ID, "For loop is missing an iterating variable name")
        iterator = id_token.value
        self.try_or_exception(TokenType.IN, "For loop is missing 'in' keyword")
        expression = self.parse_expression()
        self.try_or_exception(expression, "For loop is missing a specification of number of iterations")
        self.try_or_exception(TokenType.R_PARENTHESIS, "For loop is missing a closing parenthesis")
        block = self.parse_block()
        self.try_or_exception(block, "For loop is missing the definition of the intended behavior")
        return ForLoop(iterator, expression, block)

    def parse_while_loop(self):
        if not self.parse_next_token(TokenType.WHILE):
            return None

        self.try_or_exception(TokenType.L_PARENTHESIS,
                              "While loop definition is missing an opening parenthesis after the 'while' keyword")
        condition = self.parse_condition()
        self.try_or_exception(condition, "While loop definition is missing the condition")
        self.try_or_exception(TokenType.R_PARENTHESIS,
                              "While loop definition is missing a closing parenthesis after the condition")
        block = self.parse_block()
        self.try_or_exception(block, "While loop is missing the definition of the intended behavior")
        return WhileLoop(condition, block)

    def parse_matrix3d(self):
        if not self.parse_next_token(TokenType.L_BRACE):
            return None

        matrix = self.parse_matrix()
        self.try_or_exception(matrix, "Matrix array is has no matrices")
        matrices = [matrix]
        rows_number = matrix.rows_number
        columns_number = matrix.columns_number
        while self.parse_next_token(TokenType.COMMA):
            matrix = self.parse_matrix()
            self.try_or_exception(matrix, "Matrix array is missing another matrix after ','")
            self.try_or_exception(matrix.rows_number == rows_number and matrix.columns_number == columns_number,
                                  "All matrices must have the same dimensions in a 3D matrix."
                                  " First matrix is {} by {}, matrix number {} is {} by {}"
                                  .format(rows_number, columns_number, len(matrices)+1,
                                          matrix.rows_number, matrix.columns_number))
            matrices.append(matrix)
        self.try_or_exception(TokenType.R_BRACE, "Matrix array is missing a closing brace")
        return Matrix3d(matrices)

    def parse_matrix(self):
        if not self.parse_next_token(TokenType.L_BRACKET):
            return None

        rows = []
        row = self.parse_argument_list()
        row_length = row.length
        while len(row.expressions) > 0:
            self.try_or_exception(TokenType.SEMICOLON,
                                  "Matrix definition is missing a ';' ending the row number {}".format(len(rows)+1))
            self.try_or_exception(row.length == row_length,
                                  "Matrix rows must have the same number of elements."
                                  " First row has {} elements, row number {} has {} elements"
                                  .format(row_length, len(rows)+1, row.length))
            rows.append(row)
            row = self.parse_argument_list()
        self.try_or_exception(len(rows) > 0, "Matrix has no values")
        self.try_or_exception(TokenType.R_BRACKET, "Matrix is missing a closing bracket")
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
            self.try_or_exception(expression, "Expression is missing arguments after an operator")
            operators.append(operator)
            expressions.append(expression)
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
            self.try_or_exception(expression, "Expression is missing arguments after an operator")
            operators.append(operator)
            expressions.append(expression)
            operator = self._token.type
        if len(operators) == 0:
            return expressions[0]
        else:
            return MultiplicativeExpression(expressions, operators)

    def parse_base_expression(self):
        subtraction = self._token.type == TokenType.SUBTRACT
        if subtraction:
            self.get_next_token()
        number_token = self.parse_next_token(TokenType.NUMBER)
        if number_token:
            number = number_token.value
            return BaseExpression(number, subtraction)
        matrix = self.parse_matrix()
        if matrix:
            return BaseExpression(matrix, subtraction)
        matrix3d = self.parse_matrix3d()
        if matrix3d:
            return BaseExpression(matrix3d, subtraction)
        init_statement = self.parse_init_statement()
        if init_statement:
            return BaseExpression(init_statement, subtraction)
        reference_or_call = self.parse_reference_or_call()
        if reference_or_call:
            return BaseExpression(reference_or_call, subtraction)
        expression = self.parse_expression_in_parenthesis()
        if expression:
            return BaseExpression(expression, subtraction)
        self.try_or_exception((not subtraction), "Unary '-' operator is missing an operand")
        return None

    def parse_expression_in_parenthesis(self):
        if not self.parse_next_token(TokenType.L_PARENTHESIS):
            return None

        expression = self.parse_condition()
        self.try_or_exception(expression, "Parenthesis opened without any expression inside")
        self.try_or_exception(TokenType.R_PARENTHESIS, "No closing parenthesis found to enclose the expression")
        return ExpressionInParenthesis(expression)

    def parse_condition(self):
        condition = self.parse_and_condition()
        if not condition:
            return None

        conditions = [condition]
        while self.parse_next_token(TokenType.OR):
            condition = self.parse_and_condition()
            self.try_or_exception(condition, "No logical value after alternative operator 'or'")
            conditions.append(condition)
        if len(conditions) == 1 and isinstance(condition, LogicalExpression):
            return condition
        return Condition(conditions)

    def parse_and_condition(self):
        condition = self.parse_comparison_condition()
        if not condition:
            return None

        conditions = [condition]
        while self.parse_next_token(TokenType.AND):
            condition = self.parse_comparison_condition()
            self.try_or_exception(condition, "No logical value after conjunction operator 'and'")
            conditions.append(condition)
        if len(conditions) == 1:
            return condition
        return AndCondition(conditions)

    def parse_comparison_condition(self):
        condition1 = self.parse_logical_expression()
        if not condition1:
            return None

        operator = self._token.type
        if operator == TokenType.LESS_THAN or operator == TokenType.LESS_OR_EQUAL \
                or operator == TokenType.GREATER_THAN or operator == TokenType.GREATER_OR_EQUAL \
                or operator == TokenType.EQUAL or operator == TokenType.NOT_EQUAL:
            self.get_next_token()
            condition2 = self.parse_logical_expression()
            self.try_or_exception(condition2,
                                  "Logical expression missing the second logical value after a comparison operator")
            return ComparisonCondition(condition1, operator, condition2)
        return condition1

    def parse_logical_expression(self):
        negation = self._token.type == TokenType.NOT
        if negation:
            self.get_next_token()
        expression = self.parse_expression()
        if expression:
            return LogicalExpression(expression, negation)
        self.try_or_exception(negation, "Unary negation operator '!' is missing an operand")
        return None

    def try_or_exception(self, predicate, message: str):
        token = self._token
        if isinstance(predicate, TokenType):
            if token.type == predicate:
                self.get_next_token()
                return token
        elif predicate:
            return predicate
        raise SyntaxException(self.__lexer.token_start_position, self.__lexer.token_start_byte, message)

    def parse_type(self):
        _type = self._token.type
        if not (_type == TokenType.NUMBER_TYPE or _type == TokenType.PIXEL or _type == TokenType.MATRIX):
            return None
        return _type

    def parse_next_token(self, token_type):
        token = self._token
        if token.type == token_type:
            self.get_next_token()
            return token
        return None

    def get_next_token(self):
        self._token = self.__lexer.get_next_token()
        # parse comments
        if self._token.type == TokenType.COMMENT:
            self._comments.append(self._token.value)
            self.get_next_token()
