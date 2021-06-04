from ..parser.syntax import *


class Visitor:
    def visit_program(self, program: Program):
        pass

    def visit_function_call(self, function_call: FunctionCall):
        pass

    def visit_assignment(self, assignment: Assignment):
        pass

    def visit_block(self, block: Block):
        pass

    def visit_reference(self, reference: Reference):
        pass

    def visit_matrix_lookup(self, matrix_lookup: MatrixLookup):
        pass

    def visit_function_definition(self, function_definition: FunctionDefinition):
        pass

    def visit_if_statement(self, if_statement: IfStatement):
        pass

    def visit_init_statement(self, init_statement: InitStatement):
        pass

    def visit_return_statement(self, return_statement: ReturnStatement):
        pass

    def visit_operator_definition(self, operator_definition: OperatorDefinition):
        pass

    def visit_for_loop(self, for_loop: ForLoop):
        pass

    def visit_while_loop(self, while_loop: WhileLoop):
        pass

    def visit_matrix3d(self, matrix3d: Matrix3d):
        pass

    def visit_matrix(self, matrix: Matrix):
        pass

    def visit_condition(self, condition: Condition):
        pass

    def visit_expression(self, expression: Expression):
        pass

    def visit_expression_in_parenthesis(self, expression_in_parenthesis: ExpressionInParenthesis):
        pass

    def visit_base_expression(self, base_expression: BaseExpression):
        pass

    def visit_multiplicative_expression(self, multiplicative_expression: MultiplicativeExpression):
        pass

    def visit_additive_expression(self, additive_expression: AdditiveExpression):
        pass

    def visit_logical_expression(self, logical_expression: LogicalExpression):
        pass

    def visit_comparison_condition(self, comparison_condition: ComparisonCondition):
        pass

    def visit_and_condition(self, and_condition: AndCondition):
        pass

    def visit_argument_list(self, argument_list: ArgumentList):
        pass
