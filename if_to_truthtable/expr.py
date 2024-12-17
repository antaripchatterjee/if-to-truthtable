import re

from .error import ExpressionError

class ExpressionBuilder(object):
    def __init__(self, code):
        super(ExpressionBuilder, self).__init__()
        self.__code = code
    def cleanComments(self):
        self.__code = re.sub(r'#.*$', lambda m: ' ' * len(m.group()), self.__code, flags=re.MULTILINE)
        return self
    def expressions(self):
        is_string = False
        quote_char = ''
        is_escaped = False
        start_pos = 0
        # paran_depth = 0
        # open_paran_posisions = []

        for index, char in enumerate(self.__code):
            if not is_string:
                if char == '"' or char == "'":
                    is_string = True
                    quote_char = char
                elif char == ';':
                    yield self.__code[start_pos:index]
                    start_pos = index + 1
                # elif char == '(':
                #     paran_depth += 1
                #     open_paran_posisions.append(str(index+1))
                # elif char == ')':
                #     paran_depth -= 1
                #     if paran_depth < 0:
                #         raise ExpressionError(f"unexpected occurance of closing paranthesis at {index+1}")
                #     else:
                #         open_paran_posisions.pop()
            else:
                if char == quote_char and not is_escaped:
                    is_string = False
                    quote_char = ''
                elif char == '\n' or char == '\r':
                    raise ExpressionError(f"unterminated string literal at {index+1}")
                elif char == '\\' and not is_escaped:
                    is_escaped = True
                elif is_escaped:
                    is_escaped = False
        # if paran_depth != 0:
        #     raise ExpressionError(f'unclosed paranthesis at positions {''.join(open_paran_posisions)}')
        yield self.__code[start_pos:]