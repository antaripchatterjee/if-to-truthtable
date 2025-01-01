import re
import copy
import bisect
import fnmatch

from typing import List, Optional, Callable

from .error import ExpressionError
from .rule import RULE_ORDERS
from .token import Token

from .grammer import *


class Lexer(object):
    def __init__(self, expr: str):
        super(Lexer, self).__init__()
        self.__expr: str = expr
        
    
    def __insert_into_sorted_tokens(self, startPositions: List[int], startPos: int) -> int:
        inserting_index = bisect.bisect_left(startPositions, startPos)
        return inserting_index
    
    def tokenize(self) -> List[Token]:
        __tokens = []
        expr = self.__expr.rstrip()
        for pattern, rule, className in RULE_ORDERS:
            matches = re.finditer(pattern, expr, flags=re.MULTILINE)
            for match in matches:
                patternName = 'UNNAMED'
                for k, v in match.groupdict().items():
                    if v is not None:
                        patternName = k
                        break
                groupValue = match.group()
                startPos = match.start()
                endPos = match.end()
                sortedPositions = [token.startPos for token in __tokens]
                insertPos = self.__insert_into_sorted_tokens(sortedPositions, startPos)
                token = Token(
                    groupValue=groupValue,
                    ruleName=rule(None if insertPos == 0 else copy.copy(__tokens[insertPos-1])) \
                        if callable(rule) else patternName if rule is None else rule,
                    startPos=startPos,
                    endPos=endPos,
                    className = className
                )
                __tokens.insert(insertPos, token)
                expr = expr[:startPos] + (' ' * (endPos-startPos)) + expr[endPos:]
        
        match = re.search(r'\S', expr)
        if match is not None:
            raise ExpressionError(f"occurance of unknown token '{match.group()}' found at {match.group()}")
        
        __tokens.append(
            Token(groupValue='', startPos=-1, endPos=-1, ruleName='EOS', className='STATEMENT')
        )
        return __tokens

    # def __validate(self) -> Optional[str]:
    #     patternFriendlyNames = {
    #         'STRING_LITERAL': 'string literal',
    #         'BINARY_LITERAL': 'base 2 numeric literal',
    #         'OCTAL_LITERAL': 'base 8 numeric literal',
    #         'HEX_LITERAL': 'base 16 numeric literal',
    #         'DECIMAL_LITERAL': 'base 10 numeric literal',
    #         'RESERVED_LITERAL': 'immutable operand',
    #         'IDENTIFIER': 'mutable operand',
    #         'PARANTHESIS': lambda t: f'{dict(PARANTHESIS="opening", OPERAND="closing").get(t.ruleName)} paranthesis',
    #         'BINARY_OPERATOR': 'binary operator',
    #         'UNARY_OPERATOR': 'unary operator',
    #         'SIGN_OPERATOR': 'sign operator',
    #         'SYM_ARROW': 'fat-arrow symbol',
    #         'SYM_CMDARG': 'cmdarg symbol',
    #         'SYM_COMMA': 'comma',
    #         'STMT_ALIAS': 'statement',
    #         'STMT_MUT': 'statement',
    #         'STMT_CONST': 'statement',
    #         'STMT_BEGIN': 'statement',
    #         'STMT_END': 'statement',
    #         'STMT_EXPR': 'statement',
    #         'STMT_EVAL': 'statement'
    #     }
        
    #     currentTokenRuleName = 'INITIAL_RULE'
    #     prevToken = None
    #     for token in self.__tokens:
    #         tokeRule = f'{token.tokenType}::{token.ruleName}{"" if token.patternName.strip() == "" else f"::{token.patternName}"}'
    #         expectedTokenRules = ((expectedTokenRuleName, Lexer.__compiledTokenRules[expectedTokenRuleName]) \
    #             for expectedTokenRuleName in Lexer.__expectations(currentTokenRuleName))
    #         fulfilled = False
    #         for expectedTokenRuleName, compiledPattern in expectedTokenRules:
    #             if compiledPattern.match(tokeRule) is not None:
    #                 fulfilled = True
    #                 currentTokenRuleName = expectedTokenRuleName
    #                 break

    #         if not fulfilled:
    #             pfn = patternFriendlyNames.get(token.ruleName)
    #             ppfn = '' if prevToken is None else patternFriendlyNames.get(prevToken.ruleName)
    #             return f'unexpected occurrance of {pfn(token) if callable(pfn) else pfn} ' + \
    #                 f'"{token.groupValue}"{ppfn(prevToken) if callable(ppfn) else f' after {ppfn}'} at {token.startPos+1}'
    #         prevToken = token
        
    #     return None
