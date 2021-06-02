from typing import List
from ..interpreter.interpreter import Interpreter


class Node:
    def accept(self, visitor: Interpreter):
        pass


class ExpressionInParenthesis(Node):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: Interpreter):
        visitor.visit_expression_in_parenthesis(self)


class BaseExpression(Node):
    def __init__(self, expression, subtract_operator: bool = False):
        self.expression = expression
        self.subtract_operator = subtract_operator

    def accept(self, visitor: Interpreter):
        visitor.visit_base_expression(self)


class MultiplicativeExpression(Node):
    def __init__(self, base_expressions, multiplicative_operators=None):
        self.base_expressions = base_expressions
        self.multiplicative_operators = multiplicative_operators

    def accept(self, visitor: Interpreter):
        visitor.visit_multiplicative_expression(self)


class AdditiveExpression(Node):
    def __init__(self, multiplicative_expressions, additive_operators=None):
        self.multiplicative_expressions = multiplicative_expressions
        self.additive_operators = additive_operators

    def accept(self, visitor: Interpreter):
        visitor.visit_additive_expression(self)


class Expression(Node):
    def __init__(self, additive_expressions, new_operators: List[str] = None):
        self.additive_expressions = additive_expressions
        self.new_operators = new_operators

    def accept(self, visitor: Interpreter):
        visitor.visit_expression(self)


class LogicalExpression:
    def __init__(self, expression, negation_operator: bool = False):
        self.negation_operator = negation_operator
        self.expression = expression

    def accept(self, visitor: Interpreter):
        visitor.visit_base_condition(self)


class ComparisonCondition:
    def __init__(self, logical_expression: LogicalExpression,
                 comparison_operator,
                 logical_expression2: LogicalExpression):
        self.logical_expression = logical_expression
        self.comparison_operator = comparison_operator
        self.logical_expression2 = logical_expression2

    def accept(self, visitor: Interpreter):
        visitor.visit_comparison_condition(self)


class AndCondition(Node):
    def __init__(self, comparison_conditions: List[ComparisonCondition]):
        self.comparison_conditions = comparison_conditions

    def accept(self, visitor: Interpreter):
        visitor.visit_and_condition(self)


class Condition(Node):
    def __init__(self, and_conditions: List[AndCondition]):
        self.and_conditions = and_conditions

    def accept(self, visitor: Interpreter):
        visitor.visit_condition(self)


class ArgumentList(Node):
    def __init__(self, expressions: List[Expression]):
        self.expressions = expressions
        self.length = len(expressions)

    def accept(self, visitor: Interpreter):
        visitor.visit_argument_list(self)


class Matrix(Node):
    def __init__(self, rows: List[ArgumentList]):
        self.rows = rows
        self.rows_number = len(rows)
        self.columns_number = rows[0].length

    def accept(self, visitor: Interpreter):
        visitor.visit_matrix(self)


class Matrix3d(Node):
    def __init__(self, matrices: List[Matrix]):
        self.matrices = matrices

    def accept(self, visitor: Interpreter):
        visitor.visit_matrix3d(self)


class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor: Interpreter):
        visitor.visit_block(self)


class WhileLoop(Node):
    def __init__(self, condition: Condition, block: Block):
        self.condition = condition
        self.block = block

    def accept(self, visitor: Interpreter):
        visitor.visit_while_loop(self)


class ForLoop(Node):
    def __init__(self, iterator: str, expression: Expression, block: Block):
        self.iterator = iterator
        self.expression = expression
        self.block = block

    def accept(self, visitor: Interpreter):
        visitor.visit_for_loop(self)


class OperatorDefinition(Node):
    def __init__(self, operator: str, id1: str, type1, id2: str, type2, block: Block):
        self.operator = operator
        self.id1 = id1
        self.type1 = type1
        self.id2 = id2
        self.type2 = type2
        self.block = block
        self.parameter_list = [id1, id2]

    def accept(self, visitor: Interpreter):
        visitor.visit_operator_definition(self)


class ReturnStatement(Node):
    def __init__(self, expression: Expression = None):
        self.expression = expression

    def accept(self, visitor: Interpreter):
        visitor.visit_return_statement(self)


class InitStatement(Node):
    def __init__(self, _type, argument_list: ArgumentList):
        self.type = _type
        self.argument_list = argument_list

    def accept(self, visitor: Interpreter):
        visitor.visit_init_statement(self)


class IfStatement(Node):
    def __init__(self, condition: Condition, block: Block, else_block: Block = None):
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def accept(self, visitor: Interpreter):
        visitor.visit_if_statement(self)


class FunctionDefinition(Node):
    def __init__(self, _id: str,  parameter_list: List[str], block: Block):
        self.id = _id
        self.parameter_list = parameter_list
        self.block = block

    def accept(self, visitor: Interpreter):
        visitor.visit_function_definition(self)


class MatrixLookup(Node):
    def __init__(self, _id: str, indices: List[Expression]):
        self.id = _id
        self.indices = indices

    def accept(self, visitor: Interpreter):
        visitor.visit_matrix_lookup(self)


class Reference(Node):
    def __init__(self, id1: str, id2: str = None):
        self.id1 = id1
        self.id2 = id2

    def accept(self, visitor: Interpreter):
        visitor.visit_reference(self)


class Assignment(Node):
    def __init__(self, expression: Expression, _id: str = None, reference: Reference = None):
        self.id = _id
        self.reference = reference
        self.expression = expression

    def accept(self, visitor: Interpreter):
        visitor.visit_assignment(self)

    
class FunctionCall(Node):
    def __init__(self, _id: str, argument_list: ArgumentList):
        self.id = _id
        self.argument_list = argument_list

    def accept(self, visitor: Interpreter):
        visitor.visit_function_call(self)


class Program(Node):
    def __init__(self, function_definitions: List[FunctionDefinition] = None,
                 operator_definitions: List[OperatorDefinition] = None,
                 comments: List[str] = None):
        self.function_definitions = function_definitions
        self.operator_definitions = operator_definitions
        self.comments = comments

    def accept(self, visitor: Interpreter):
        visitor.visit_program(self)
