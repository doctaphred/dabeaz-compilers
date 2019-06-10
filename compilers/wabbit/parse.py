# parse.py
#
# Wabbit parser.   This needs to construct the data model or 
# an abstract syntax tree.  
#
# EBNF Syntax
#       'quoted'      - Literal text
#      { rule }       - Zero or more repetitions of rule
#      a | b          - a or b
#      ( ... )        - Grouping
#
# The Grammar
#
#   program = { statement }
#
#   statement = print_statement
#              | assign_statement
#              | if_statement
#              | while_statement
#              | const_declaration
#              | var_declaration
#              | func_decaration
#              | return_statement
#              | break_statement
#              | continue_statement
#              
#  expr = logterm { '||' logterm }
#
#  logterm = relation { && relation }
#
#  relation = additive { ('<'|'<='|'>'|'>='|'=='|'!=') additive }
#
#  additive = term { ('+'|'-') term }
#
#  term = factor { ('*'|'/') factor }
#
#  factor = INTEGER
#         | FLOAT
#         | CHAR
#         | '(' expr ')'
#         | ('+'|'-'|'!'|'^') expr
#         | location
#         | location '(' args ')'
#         | type '(' expr ')'
#
#  location = ID
#           | '`' expr
#
#
#  args = <empty>
#       | expr { ',' expr }
# 
#  print_statement = 'print' expr ';'
#
#  assign_statement = location '=' expr ';'
#
#  if_statement = 'if' expr '{' { statement } '}' [ 'else' '{' { statement } '}' ]
#
#  while_statement = 'while' expr '{' { statement } '}'
#
#  return_statement = 'return' expr ';'
#
#  break_statement = 'break' ';'
#
#  continue_statement = 'continue' ';'
#
#  var_declaration = 'var' ID [ type ] '=' expr ';'
#                  | 'var' ID type ';'
#
#  const_declaration = 'const' ID '=' expr ';'
#
#  func_declaration = 'func' ID '(' parameters ')' type '{' { statements } '}'
#                   | 'import' 'func' ID '(' parameters ')' type ';'
#
#  parameters = <empty>
#             | parameter {',' parameter }
#
#  parameter = ID type
#
#  type = ID
