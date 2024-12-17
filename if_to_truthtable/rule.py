PAT_IDENTIFIER = r'\b(?:(?!true\b|false\b|null\b|alias\b|begin\b|context\b|end\b|expr\b|enum\b|const\b|mut\b|eval\b)[a-zA-Z_][a-zA-Z0-9_]*)\b'
PAT_STRING_LITERAL = r'(?:"(?:[^"\\\r\n]|\\.)*"|\'(?:[^\'\\\r\n]|\\.)*\')'
PAT_UNSIGNED_NUMERIC_LITERAL = r'\b(?P<BASE2>0b[01]+)|(?P<BASE8>0o[0-7]+)|(?P<BASE16>0x[\da-fA-F]+)|(?P<BASE10>\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)\b'
PAT_BINARY_OPERATOR = r'(?:==|!=|>=|<=|>|<|&&|\|\||\^|>>|<<|&|\||\*|/|%|\*\*|//)'
PAT_SIGN_OPERATOR = r'(?:[+-])'
PAT_UNARY_OPERATOR = r'(?:[!~])'
PAT_PARANTHESIS = r'(?:[\(\)])'
PAT_RESERVED_LITERAL = r'\b(?:true|false|null)\b'
PAT_RESERVED_COMMAND = r'\b(?P<ALIAS>alias)|(?P<BEGIN>begin)|(?P<END>end)|(?P<EXPR>expr)|(?P<MUT>mut)|(?P<EVAL>eval)\b'
PAT_SCRIPT_NOUN = r'(?:`[a-zA-Z_][a-zA-Z0-9\t\ ]*`)'
PAT_ADDITIONAL_SYMBOL = r'(?P<ARROW>=>)|(?P<CMDARG>::)|(?P<COMMA>,)'


RULE_ORDERS = [
    ('PAT_STRING_LITERAL', PAT_STRING_LITERAL, 'OPERAND'),
    ('PAT_SCRIPT_NOUN', PAT_SCRIPT_NOUN, 'NOUN'),
    ('PAT_NUMERIC_LITERAL', PAT_UNSIGNED_NUMERIC_LITERAL, 'OPERAND'),
    ('PAT_RESERVED_LITERAL', PAT_RESERVED_LITERAL, 'OPERAND'),
    ('PAT_RESERVED_KEYWORD' , PAT_RESERVED_COMMAND, 'COMMAND'),
    ('PAT_IDENTIFIER', PAT_IDENTIFIER, 'OPERAND'),
    ('PAT_PARANTHESIS',  PAT_PARANTHESIS, lambda gv: \
        'PARANTHESIS' if gv == '(' else 'OPERAND' if gv == ')' else 'UNKNWON'),
    ('PAT_ADDITIONAL_SYMBOL', PAT_ADDITIONAL_SYMBOL, 'SYMBOL'),
    ('PAT_BINARY_OPERATOR', PAT_BINARY_OPERATOR, 'OPERATOR'),
    ('PAT_UNARY_OPERATOR', PAT_UNARY_OPERATOR, 'OPERATOR'),
    (lambda ptok: 'PAT_UNARY_OPERATOR' if (ptok is None or ptok.is_operator() or ptok.is_paranthesis() \
        ) else 'PAT_BINARY_OPERATOR', PAT_SIGN_OPERATOR, 'OPERATOR')
]