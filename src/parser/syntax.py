from typing import List


class Visitable:
    def accept(self, visitor):
        pass


class Callable(Visitable):
    def verify_arguments(self, arguments):
        pass


class ExpressionInParenthesis(Visitable):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_expression_in_parenthesis(self)


class BaseExpression(Visitable):
    def __init__(self, expression, subtract_operator: bool = False):
        self.expression = expression
        self.subtract_operator = subtract_operator

    def accept(self, visitor):
        visitor.visit_base_expression(self)


class MultiplicativeExpression(Visitable):
    def __init__(self, base_expressions, multiplicative_operators=None):
        self.base_expressions = base_expressions
        self.multiplicative_operators = multiplicative_operators

    def accept(self, visitor):
        visitor.visit_multiplicative_expression(self)


class AdditiveExpression(Visitable):
    def __init__(self, multiplicative_expressions, additive_operators=None):
        self.multiplicative_expressions = multiplicative_expressions
        self.additive_operators = additive_operators

    def accept(self, visitor):
        visitor.visit_additive_expression(self)


class Expression(Visitable):
    def __init__(self, additive_expressions, new_operators: List[str] = None):
        self.additive_expressions = additive_expressions
        self.new_operators = new_operators

    def accept(self, visitor):
        visitor.visit_expression(self)


class LogicalExpression(Visitable):
    def __init__(self, expression, negation_operator: bool = False):
        self.negation_operator = negation_operator
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_logical_expression(self)


class ComparisonCondition(Visitable):
    def __init__(self, logical_expression: LogicalExpression,
                 comparison_operator,
                 logical_expression2: LogicalExpression):
        self.logical_expression = logical_expression
        self.comparison_operator = comparison_operator
        self.logical_expression2 = logical_expression2

    def accept(self, visitor):
        visitor.visit_comparison_condition(self)


class AndCondition(Visitable):
    def __init__(self, comparison_conditions: List[ComparisonCondition]):
        self.comparison_conditions = comparison_conditions

    def accept(self, visitor):
        visitor.visit_and_condition(self)


class Condition(Visitable):
    def __init__(self, and_conditions: List[AndCondition]):
        self.and_conditions = and_conditions

    def accept(self, visitor):
        visitor.visit_condition(self)


class ArgumentList(Visitable):
    def __init__(self, expressions: List[Expression]):
        self.expressions = expressions
        self.length = len(expressions)

    def accept(self, visitor):
        visitor.visit_argument_list(self)


class Matrix(Visitable):
    def __init__(self, rows: List[ArgumentList]):
        self.rows = rows
        self.rows_number = len(rows)
        self.columns_number = rows[0].length

    def accept(self, visitor):
        visitor.visit_matrix(self)


class Matrix3d(Visitable):
    def __init__(self, matrices: List[Matrix]):
        self.matrices = matrices

    def accept(self, visitor):
        visitor.visit_matrix3d(self)


class Block(Visitable):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        visitor.visit_block(self)


class WhileLoop(Visitable):
    def __init__(self, condition: Condition, block: Block):
        self.condition = condition
        self.block = block

    def accept(self, visitor):
        visitor.visit_while_loop(self)


class ForLoop(Visitable):
    def __init__(self, iterator: str, expression: Expression, block: Block):
        self.iterator = iterator
        self.expression = expression
        self.block = block

    def accept(self, visitor):
        visitor.visit_for_loop(self)


class OperatorDefinition(Callable):
    def __init__(self, operator: str, id1: str, type1, id2: str, type2, block: Block):
        self.operator = operator
        self.id1 = id1
        self.type1 = type1
        self.id2 = id2
        self.type2 = type2
        self.block = block
        self.parameter_list = [id1, id2]
        self.id = operator

    def verify_arguments(self, arguments):
        return len(arguments) == 2

    def accept(self, visitor):
        visitor.visit_operator_definition(self)


class ReturnStatement(Visitable):
    def __init__(self, expression: Expression = None):
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_return_statement(self)


class InitStatement(Visitable):
    def __init__(self, _type, argument_list: ArgumentList):
        self.type = _type
        self.argument_list = argument_list

    def accept(self, visitor):
        visitor.visit_init_statement(self)


class IfStatement(Visitable):
    def __init__(self, condition: Condition, block: Block, else_block: Block = None):
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def accept(self, visitor):
        visitor.visit_if_statement(self)


class FunctionDefinition(Callable):
    def __init__(self, _id: str,  parameter_list: List[str], block: Block):
        self.id = _id
        self.parameter_list = parameter_list
        self.block = block

    def verify_arguments(self, arguments):
        return len(arguments) == len(self.parameter_list)

    def accept(self, visitor):
        visitor.visit_function_definition(self)


class MatrixLookup(Visitable):
    def __init__(self, _id: str, indices: List[Expression]):
        self.id = _id
        self.indices = indices

    def accept(self, visitor):
        visitor.visit_matrix_lookup(self)


class Reference(Visitable):
    def __init__(self, id1: str, id2: str = None):
        self.id1 = id1
        self.id2 = id2

    def accept(self, visitor):
        visitor.visit_reference(self)


class Assignment(Visitable):
    def __init__(self, expression: Expression, _id: str = None,
                 reference: Reference = None,
                 matrix_lookup: MatrixLookup = None):
        self.id = _id
        self.reference = reference
        self.matrix_lookup = matrix_lookup
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_assignment(self)

    
class FunctionCall(Visitable):
    def __init__(self, _id: str, argument_list: ArgumentList):
        self.id = _id
        self.argument_list = argument_list

    def accept(self, visitor):
        visitor.visit_function_call(self)


class Program(Visitable):
    def __init__(self, function_definitions: List[FunctionDefinition] = None,
                 operator_definitions: List[OperatorDefinition] = None,
                 comments: List[str] = None):
        self.function_definitions = function_definitions
        self.operator_definitions = operator_definitions
        self.comments = comments

    def accept(self, visitor):
        visitor.visit_program(self)
