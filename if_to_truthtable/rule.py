PAT_IDENTIFIER = r'\b(?:(?!true\b|false\b|null\b)[a-zA-Z_][a-zA-Z0-9_]*)\b'
PAT_STRING_LITERAL = r'(?:"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\')'
PAT_UNSIGNED_NUMERIC_LITERAL = r'\b(?P<BASE2>0b[01]+)|(?P<BASE8>0o[0-7]+)|(?P<BASE16>0x[\da-fA-F]+)|(?P<BASE10>\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)\b'
PAT_BINARY_OPERATOR = r'(?P<CONDITIONAL>==|!=|>=|<=|>|<)|(?P<LOGICAL>&&|\|\|)|(?P<BITWISE>\^|>>|<<|&|\|)|(?P<ARITHMATIC>\*|/|%|\*\*|//)'
PAT_SIGN_OPERATOR = r'(?:[+-])'
PAT_UNARY_OPERATOR = r'(?:[!~])'
PAT_PARANTHESIS = r'(?:[\(\)])'
PAT_RESERVED_LITERAL = r'\b(?:true|false|null)\b'

RULE_ORDERS = [
    ('PAT_STRING_LITERAL', PAT_STRING_LITERAL, 'OPERAND'),
    ('PAT_NUMERIC_LITERAL', PAT_UNSIGNED_NUMERIC_LITERAL, 'OPERAND'),
    ('PAT_RESERVED_LITERAL', PAT_RESERVED_LITERAL, 'OPERAND'),
    ('PAT_IDENTIFIER', PAT_IDENTIFIER, 'OPERAND'),
    ('PAT_PARANTHESIS',  PAT_PARANTHESIS, lambda gv: \
        'PARANTHESIS' if gv == '(' else 'OPERAND' if gv == ')' else 'UNKNWON'),
    ('PAT_BINARY_OPERATOR', PAT_BINARY_OPERATOR, 'OPERATOR'),
    ('PAT_UNARY_OPERATOR', PAT_UNARY_OPERATOR, 'OPERATOR'),
    (lambda pt: 'PAT_UNARY_OPERATOR' if (pt is None or pt.is_operator() or pt.is_paranthesis() \
        ) else 'PAT_BINARY_OPERATOR', PAT_SIGN_OPERATOR, 'OPERATOR')
]