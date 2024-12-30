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

    __tokenRules: dict[str, Callable[[str], bool]] = {
        'NO_STATEMENT': None,
        'STATEMENT_ALIAS': lambda tr: tr == 'STATEMENT::RESERVED_KEYWORD::ALIAS',
        'STATEMENT_MUT': lambda tr: tr == 'STATEMENT::RESERVED_KEYWORD::MUT',
        'STATEMENT_CONST': lambda tr: tr == 'STATEMENT::RESERVED_KEYWORD::MUT',
        'STATEMENT_EXPR': lambda tr: tr == 'STATEMENT::RESERVED_KEYWORD::EXPR',
        'STATEMENT_EVAL': lambda tr: tr == 'STATEMENT::RESERVED_KEYWORD::EVAL',
        'STATEMENT_BEGIN': lambda tr: tr == 'STATEMENT::RESERVED_KEYWORD::BEGIN',
        'STATEMENT_END': lambda tr: tr == 'STATEMENT::RESERVED_KEYWORD::END',
        'OPEN_PARANTHESIS': lambda tr: tr == 'PARANTHESIS::PARANTHESIS',
        'CLOSE_PARANTHESIS': lambda tr: tr == 'OPERAND::PARANTHESIS',
        'GENERIC_OPERAND': lambda tr: tr == fnmatch.fnmatch(tr, 'OPERAND::[_a-z][_a-z0-9]*::[_a-z][_a-z0-9]*') \
            and not str.startswith(tr.upper(), 'OPERAND::PARANTHESIS'),
        'UNARY_OPERATOR': lambda tr: tr == 'OPERATOR::UNARY_OPERATOR',
        'BINARY_OPERATOR': lambda tr: tr == 'OPERATOR::BINARY_OPERATOR'
    }

    def __init__(self, expr: str):
        super(Lexer, self).__init__()
        self.__expr: str = expr
        self.__tokens: List[Token] = list()
        
    
    def __insert_into_sorted_tokens(self, startPositions: List[int], startPos: int) -> int:
        inserting_index = bisect.bisect_left(startPositions, startPos)
        return inserting_index
    
    def tokenize(self):
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
                sortedPositions = [token.startPos for token in self.__tokens]
                insertPos = self.__insert_into_sorted_tokens(sortedPositions, startPos)
                token = Token(
                    groupValue=groupValue,
                    ruleName=rule(None if insertPos == 0 else copy.copy(self.__tokens[insertPos-1])) \
                        if callable(rule) else patternName if rule is None else rule,
                    startPos=startPos,
                    endPos=endPos,
                    className = className(groupValue) if callable(className) else className
                )
                self.__tokens.insert(insertPos, token)
                expr = expr[:startPos] + (' ' * (endPos-startPos)) + expr[endPos:]
        # err = self.__validate(expr)
        # if err is None:
        #     return self.__tokens
        # else:
        #     raise ExpressionError(err)
        match = re.search(r'\S', expr)
        if match is not None:
            raise ExpressionError(f"occurance of unknown token '{match.group()}' found at {match.group()}")
        
        self.__validate()

    def __validate(self) -> Optional[str]:
        patternFriendlyNames = {
            'STRING_LITERAL': 'string literal',
            'BINARY_LITERAL': 'base 2 numeric literal',
            'OCTAL_LITERAL': 'base 8 numeric literal',
            'HEX_LITERAL': 'base 16 numeric literal',
            'DECIMAL_LITERAL': 'base 10 numeric literal',
            'RESERVED_LITERAL': 'immutable operand',
            'IDENTIFIER': 'mutable operand',
            'PARANTHESIS': lambda t: f'{dict(PARANTHESIS="opening", OPERAND="closing").get(t.ruleName)} paranthesis',
            'BINARY_OPERATOR': 'binary operator',
            'UNARY_OPERATOR': 'unary operator',
            'SIGN_OPERATOR': 'sign operator',
            'SYM_ARROW': 'fat-arrow symbol',
            'SYM_CMDARG': 'cmdarg symbol',
            'SYM_COMMA': 'comma',
            'STMT_ALIAS': 'statement',
            'STMT_MUT': 'statement',
            'STMT_CONST': 'statement',
            'STMT_BEGIN': 'statement',
            'STMT_END': 'statement',
            'STMT_EXPR': 'statement',
            'STMT_EVAL': 'statement'
        }
        
        currentTokenRuleName = 'INITIAL_RULE'
        prevToken = None
        for token in self.__tokens:
            tokeRule = f'{token.tokenType}::{token.ruleName}{"" if token.patternName.strip() == "" else f"::{token.patternName}"}'
            expectedTokenRules = ((expectedTokenRuleName, Lexer.__compiledTokenRules[expectedTokenRuleName]) \
                for expectedTokenRuleName in Lexer.__expectations(currentTokenRuleName))
            fulfilled = False
            for expectedTokenRuleName, compiledPattern in expectedTokenRules:
                if compiledPattern.match(tokeRule) is not None:
                    fulfilled = True
                    currentTokenRuleName = expectedTokenRuleName
                    break

            if not fulfilled:
                pfn = patternFriendlyNames.get(token.ruleName)
                ppfn = '' if prevToken is None else patternFriendlyNames.get(prevToken.ruleName)
                return f'unexpected occurrance of {pfn(token) if callable(pfn) else pfn} ' + \
                    f'"{token.groupValue}"{ppfn(prevToken) if callable(ppfn) else f' after {ppfn}'} at {token.startPos+1}'
            prevToken = token
        
        return None
