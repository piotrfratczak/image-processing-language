# iml
An image processing language with build-in matrix and pixel types written with Python.  
A project at Warsaw University of Technology for Compilation Techniques course.

## Table of contents
* [Requirements](#requirements)
* [Run guide](#run-guide)
* [Language details](#language-details)
* [Grammar](#grammar)

## Requirements
Python 3.8.

## Run guide
```
/image-processing-language$ python3 imli.py <source_file>
```

**source_file** - path to source file with code to be interpreted. 

### Output
During execution, the program writes to the standard output.

## Language details
More about the language can be found in the [documentation](dokumentacja.pdf) (written in Polish).

## Grammar
The imli language grammar in EBNF notation.

| Symbol |  | Production rule |
| ------ | --- | --------------- |
|program                   |=| {function_definition &#124; operator_definition &#124; comment};|
|comment                   |=| "#", { ? any character ? }, ? carriage return ?;|
|statement                 |=| operator_definition &#124; for_loop &#124; while_loop &#124; if_statement &#124; return_statement &#124; assignment_or_call &#124; comment;|
|reference_or_call         |=| id, [ matrix_lookup &#124; (rest_of_reference,  [rest_of_function_call]) ];|
|function_definition       |=| id, "(", parameter_list, ")", block;|
|rest_of_function_call     |=| "(", argument_list, ")";|
|argument_list             |=| [ expression, {",", expression} ];|
|parameter_list            |=| [ id, {",", id} ];|
|if_statement              |=| "if", "(", condition, ")", block , ["else", block];|
|init_statement            |=| type, "(", argument_list, ")";|
|return_statement          |=| "return", [expression], ";";|
|block                     |=| statement &#124; ( "{", {statement}, "}" );|
|assignment_or_call        |=| id, ( matrix_lookup &#124; rest_of_function_call &#124; ([rest_of_reference], rest_of_assignment) ), ";";|
|rest_of_assignment        |=| assignment_operator, expression;|
|matrix_lookup             |=| "[", expression, {",", expression}, "]";|
|rest_of_reference         |=| member_operator, id ;|
|operator_definition       |=| new_operator, "(", id, ",", id, of_operator, type, ",", id, of_operator, type, ")", block;|
|for_loop                  |=| "for", "(", id, "in", expression, ")", block;|
|while_loop                |=| "while", "(", condition, ")", block;|
|matrix3d                  |=| "{", matrix, {",", matrix}, "}";|
|matrix                    |=| "[", {row}, "]";|
|row                       |=| argument_list, ";"; (* list cannot be empty *)|
|expression                |=| additive_expression, {id, additive_expression};|
|additive_expression       |=| multiplicative_expression, {additive_operator, mulitiplicative_expression};|
|multiplicative_expression |=| base_expression, {mulitiplicative_operator, base_expression};|
|base_expression           |=| [subtraction_operator], (expression_in_parenthesis &#124; number &#124; matrix &#124; matrix3d &#124; init_statement &#124; reference_or_call);|
|expression_in_parenthesis |=| "(", condition, ")";|
|condition                 |=| and_condition, {alternative_operator, and_condition};|
|and_condition             |=| comparison_condition, {conjunction_operator, comparison_condition};|
|comparison_condition      |=| logical_expression, [comparison_operator, logical_expression];|
|logical_expression        |=| [negation_operator], expression;|
| | |(* no whitespaces between characters of the elements below *)|
|id                      |=| alpha, {word};|
|alpha                   |=| "a"..."z" &#124; "A"..."Z";|
|non_zero                |=| "1"..."9";|
|digit                   |=| "0" &#124; non_zero;|
|number                  |=| "0" &#124; ( non_zero, {digit} );|
|word                    |=| alpha &#124; digit &#124; "_";|
|negation_operator       |=| "!";|
|member_operator         |=| ".";|
|alternative_operator    |=| "or";|
|conjunction_operator    |=| "and";|
|comparison_operator     |=| "<" &#124; ">" &#124; "<=" &#124; ">=" &#124; "==" &#124; "!=";|
|additive_operator       |=| "+" &#124; subtraction_operator;|
|subtraction_operator    |=| "-";|
|multiplicative_operator |=| "*" &#124; "/" &#124; "@" &#124; "%";|
|assignment_operator     |=| "=";|
|of_operator             |=| "of";|
|new_operator            |=| "newop";|
|type                    |=| "pixel" &#124; "matrix" &#124; "number";|