PAT_IDENTIFIER = r'\b(?:(?!true\b|false\b|null\b|alias\b|begin\b|end\b|expr\b|const\b|mut\b|eval\b)[a-zA-Z_][a-zA-Z0-9_]*)\b'
PAT_STRING_LITERAL = r'(?:"(?:[^"\\\r\n]|\\.)*"|\'(?:[^\'\\\r\n]|\\.)*\')'
PAT_UNSIGNED_NUMERIC_LITERAL = r'\b(?P<BINARY_LITERAL>0b[01]+)|(?P<OCTAL_LITERAL>0o[0-7]+)|(?P<HEX_LITERAL>0x[\da-fA-F]+)|(?P<DECIMAL_LITERAL>\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)\b'
PAT_BINARY_OPERATOR = r'(?:==|!=|>=|<=|>|<|&&|\|\||\^|>>|<<|&|\||\*|/|%|\*\*|//)'
PAT_SIGN_OPERATOR = r'(?:[+-])'
PAT_UNARY_OPERATOR = r'(?:[!~])'
PAT_PARANTHESIS = r'(?P<OPEN_PARAN>\()|(?P<CLOSE_PARAN>\))'
PAT_RESERVED_LITERAL = r'\b(?:true|false|null)\b'
PAT_RESERVED_COMMAND = r'\b(?P<STMT_ALIAS>alias)|(?P<STMT_BEGIN>begin)|(?P<STMT_END>end)|(?P<STMT_EXPR>expr)|(?P<STMT_CONST>const)|(?P<STMT_MUT>mut)|(?P<STMT_EVAL>eval)\b'
PAT_SCRIPT_NOUN = r'(?:`[a-zA-Z_][a-zA-Z0-9\t\ ]*`)'
PAT_SCRIPT_SYMBOL = r'(?P<SYM_ARROW>=>)|(?P<SYM_CMDARG>::)|(?P<SYM_COMMA>,)'


RULE_ORDERS = [
    (PAT_STRING_LITERAL, 'STRING_LITERAL', 'OPERAND'),
    (PAT_SCRIPT_NOUN, 'SCRIPT_NOUN', 'NOUN'),
    (PAT_UNSIGNED_NUMERIC_LITERAL, None, 'OPERAND'),
    (PAT_RESERVED_LITERAL, 'RESERVED_LITERAL', 'OPERAND'),
    (PAT_RESERVED_COMMAND, None, 'STATEMENT'),
    (PAT_IDENTIFIER, 'IDENTIFIER', 'OPERAND'),
    (PAT_PARANTHESIS, None, 'PARANTHESIS'),
    (PAT_SCRIPT_SYMBOL, None, 'SYMBOL'),
    (PAT_BINARY_OPERATOR, 'BINARY_OPERATOR', 'OPERATOR'),
    (PAT_UNARY_OPERATOR, 'UNARY_OPERATOR', 'OPERATOR'),
    (PAT_SIGN_OPERATOR, lambda prvTok: 'SIGN_OPERATOR' if (prvTok is None or \
        prvTok.is_operator() or prvTok.is_paranthesis() \
            ) else 'BINARY_OPERATOR', 'OPERATOR')
]