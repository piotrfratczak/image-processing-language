from typing import List


class ArgumentList:
    def ___init__(self, expressions:List[any]):
        self.expressions = expressions


class ExpressionInParenthesis:
    def __init__(self, expression):
        self.expression = expression


class BaseExpression:
    def __init__(self, subtract_operator:bool=False,
                       expression_in_parenthesis:ExpressionInParenthesis=None,
                       number:int=None,
                       matrix=None,
                       matrix3d=None,
                       reference_or_call=None):
        self.subtract_operator = subtract_operator
        self.expression_in_parenthesis = expression_in_parenthesis
        self.number = number
        self.matrix = matrix
        self.matrix3d = matrix3d
        self.reference_or_call = reference_or_call


class MultiplicativeExpression:
    def __init__(self, base_expressions:List[BaseExpression], multiplicative_operators:List[any]=None):
        self.base_expressions = base_expressions
        self.multiplicative_operators = multiplicative_operators


class Expression:
    def __init__(self, multiplicative_expressions:List[MultiplicativeExpression], additive_operators:List[any]=None):
        self.multiplicative_expressions = multiplicative_expressions
        self.additive_operators = additive_operators


class ConditionInParenthesis:
    def __init__(self, condition):
        self.condition = condition


class BaseCondition:
    def __init__(self, negation_operator:bool=False,
                       condition_in_parenthesis:ConditionInParenthesis=None,
                       expression:Expression=None):
        self.negation_operator = negation_operator
        self.condition_in_parenthesis = condition_in_parenthesis
        self.expression = expression


class RelationCondition:
    def __init__(self, base_condition:BaseCondition,
                       comparison_operator=None,
                       base_condition2:BaseCondition=None):
        self.base_condition = base_condition
        self.comparison_operator = comparison_operator
        self.base_condition2 = base_condition2


class EqualityCondition:
    def __init__(self, relation_condition:RelationCondition,
                       equal_operator=None,
                       relation_condition2:RelationCondition=None):
        self.relation_condition = relation_condition
        self.equal_operator = equal_operator
        self.relation_condition2 = relation_condition2


class AndCondition:
    def __init__(self, equality_conditions:List[EqualityCondition]):
        self.equality_conditions = equality_conditions


class Condition:
    def __init__(self, and_conditions:List[AndCondition]):
        self.and_conditions = and_conditions


class Matrix:
    def __init__(self, rows:List[ArgumentList]):
        self.rows = rows


class Matrix3d:
    def __init__(self, matrices:List[Matrix]):
        self.matrices = matrices


class Block:
    def __init__(self, statements):
        self.statements = statements


class WhileLoop:
    def __init__(self, condition:Condition, block:Block):
        self.condition = condition
        self.block = block


class ForLoop:
    def __init__(self, _id:str, expression:Expression, block:Block):
        self.id = _id
        self.expression = expression
        self.block = block


class OperatorDefinition:
    def __init__(self, id1:str, type1, id2:str, type2, block:Block):
        self.id1 = id1
        self.type1 = type1
        self.id2 = id2
        self.type2 = type2
        self.block = block


class ReturnStatement:
    def __init__(self, expression:Expression=None):
        self.expression = expression


class InitStatement:
    def __init__(self, _type, argument_list:ArgumentList):
        self.type = _type
        self.argument_list = argument_list


class IfStatement:
    def __init__(self, condition:Condition, blocks:List[Block]):
        self.condition = condition
        self.blocks = blocks


class FunctionDefinition:
    def __init__(self, _id:str, block:Block, argument_list:ArgumentList):
        self.id = _id
        self.argument_list = argument_list
        self.block = block


class MatrixLookup:
    def __init__(self, _id:str, indices:List[Expression]):
        self.id = _id
        self.indices = indices


class Reference:
    def __init__(self, id1:str, id2:str=None):
        self.id1 = id1
        self.id2 = id2


class Assignment:
    def __init__(self, expression:Expression, _id:str=None, reference:Reference=None):
        self.id = _id
        self.reference = reference
        self.expression = expression

    
class FunctionCall:
    def __init__(self, _id:str, argument_list:ArgumentList):
        self.id = _id
        self.argument_list = argument_list


class Program:
    def __init__(self, function_definitions:List[FunctionDefinition]=None,
                       comments:List[str]=None):
        self.function_definitions = function_definitions
        self.comments = comments
