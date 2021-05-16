from typing import List


class ExpressionInParenthesis:
    def __init__(self, expression):
        self.expression = expression


class BaseExpression:
    def __init__(self, expression, subtract_operator: bool = False):
        self.expression = expression
        self.subtract_operator = subtract_operator


class MultiplicativeExpression:
    def __init__(self, base_expressions, multiplicative_operators=None):
        self.base_expressions = base_expressions
        self.multiplicative_operators = multiplicative_operators


class Expression:
    def __init__(self, multiplicative_expressions, additive_operators=None):
        self.multiplicative_expressions = multiplicative_expressions
        self.additive_operators = additive_operators


class ConditionInParenthesis:
    def __init__(self, condition):
        self.condition = condition


class BaseCondition:
    def __init__(self, expression, negation_operator: bool = False):
        self.negation_operator = negation_operator
        self.expression = expression


class ComparisonCondition:
    def __init__(self, base_condition: BaseCondition,
                 comparison_operator=None,
                 base_condition2: BaseCondition = None):
        self.base_condition = base_condition
        self.comparison_operator = comparison_operator
        self.base_condition2 = base_condition2


class AndCondition:
    def __init__(self, comparison_conditions: List[ComparisonCondition]):
        self.comparison_conditions = comparison_conditions


class Condition:
    def __init__(self, and_conditions: List[AndCondition]):
        self.and_conditions = and_conditions


class ArgumentList:
    def __init__(self, expressions: List[Expression]):
        self.expressions = expressions


class Matrix:
    def __init__(self, rows: List[ArgumentList]):
        self.rows = rows


class Matrix3d:
    def __init__(self, matrices: List[Matrix]):
        self.matrices = matrices


class Block:
    def __init__(self, statements):
        self.statements = statements


class WhileLoop:
    def __init__(self, condition: Condition, block: Block):
        self.condition = condition
        self.block = block


class ForLoop:
    def __init__(self, iterator: str, expression: Expression, block: Block):
        self.iterator = iterator
        self.expression = expression
        self.block = block


class OperatorDefinition:
    def __init__(self, operator: str, id1: str, type1, id2: str, type2, block: Block):
        self.operator = operator
        self.id1 = id1
        self.type1 = type1
        self.id2 = id2
        self.type2 = type2
        self.block = block


class ReturnStatement:
    def __init__(self, expression: Expression = None):
        self.expression = expression


class InitStatement:
    def __init__(self, _type, argument_list: ArgumentList):
        self.type = _type
        self.argument_list = argument_list


class IfStatement:
    def __init__(self, condition: Condition, block: Block, else_block: Block = None):
        self.condition = condition
        self.block = block
        self.else_block = else_block


class FunctionDefinition:
    def __init__(self, _id: str,  parameter_list: List[str], block: Block):
        self.id = _id
        self.parameter_list = parameter_list
        self.block = block


class MatrixLookup:
    def __init__(self, _id: str, indices: List[Expression]):
        self.id = _id
        self.indices = indices


class Reference:
    def __init__(self, id1: str, id2: str = None):
        self.id1 = id1
        self.id2 = id2


class Assignment:
    def __init__(self, expression: Expression, _id: str = None, reference: Reference = None):
        self.id = _id
        self.reference = reference
        self.expression = expression

    
class FunctionCall:
    def __init__(self, _id: str, argument_list: ArgumentList):
        self.id = _id
        self.argument_list = argument_list


class Program:
    def __init__(self, function_definitions: List[FunctionDefinition] = None,
                 operator_definitions: List[OperatorDefinition] = None,
                 comments: List[str] = None):
        self.function_definitions = function_definitions
        self.operator_definitions = operator_definitions
        self.comments = comments
