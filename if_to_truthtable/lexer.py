import re
import copy
import bisect

from typing import List, Optional

from .error import ExpressionError
from .rule import RULE_ORDERS
from .token import Token


class Lexer(object):

    __compiledTokenRules: dict[str, Optional[re.Pattern]] = {
        'INITIAL_RULE': None,
        'OPEN_PARANTHESIS': re.compile(r'^PARANTHESIS::PAT_PARANTHESIS$'),
        'CLOSE_PARANTHESIS': re.compile(r'^OPERAND::PAT_PARANTHESIS$'),
        'GENERIC_OPERAND': re.compile(r'^OPERAND::\b(?!PAT_PARANTHESIS\b)[a-z_][a-z0-9_]*$', re.IGNORECASE),
        'UNARY_OPERATOR': re.compile(r'^OPERATOR::PAT_UNARY_OPERATOR$'),
        'BINARY_OPERATOR': re.compile(r'^OPERATOR::PAT_BINARY_OPERATOR$')
    }

    def __init__(self, expr: str, expr_id: int):
        super(Lexer, self).__init__()
        self.__expr: str = expr
        self.__expr_id: int = expr_id
        self.__tokens: List[Token] = list()

        
    
    def __insert_into_sorted_tokens(self, startPositions: List[int], startPos: int) -> int:
        inserting_index = bisect.bisect_left(startPositions, startPos)
        return inserting_index

    @staticmethod
    def __expectations(tokenRuleName) -> dict[str, tuple[str]]:
        tokenRuleNames = {
            'INITIAL_RULE': (
                'OPEN_PARANTHESIS',
                'GENERIC_OPERAND',
                'UNARY_OPERATOR'
            ),
            'OPEN_PARANTHESIS': (
                'OPEN_PARANTHESIS',
                'GENERIC_OPERAND',
                'UNARY_OPERATOR'
            ),
            'CLOSE_PARANTHESIS': (
                'BINARY_OPERATOR',
                'CLOSE_PARANTHESIS'
            ),
            'GENERIC_OPERAND': (
                'BINARY_OPERATOR',
                'CLOSE_PARANTHESIS'
            ),
            'UNARY_OPERATOR': (
                'GENERIC_OPERAND',
                'UNARY_OPERATOR',
                'OPEN_PARANTHESIS'
            ),
            'BINARY_OPERATOR': (
                'GENERIC_OPERAND',
                'UNARY_OPERATOR',
                'OPEN_PARANTHESIS'
            )
        }
        return tokenRuleNames.get(tokenRuleName)
    
    def tokenize(self):
        expr = self.__expr.rstrip()
        for rule, pattern, tokenType in RULE_ORDERS:
            matches = re.finditer(pattern, expr, flags=re.MULTILINE)
            for match in matches:
                patternName = 'DEFAULT'
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
                        if callable(rule) else rule,
                    startPos=startPos,
                    endPos=endPos,
                    patternName=patternName,
                    tokenType = tokenType(groupValue) if callable(tokenType) else tokenType
                )
                self.__tokens.insert(insertPos, token)
                expr = expr[:startPos] + (' ' * (endPos-startPos)) + expr[endPos:]
        err = self.__validate(expr)
        if err is None:
            return self.__tokens
        else:
            raise ExpressionError(err)


    def __validate(self, exprWithoutTokens: str) -> Optional[str]:
        patternFriendlyNames = {
            'PAT_STRING_LITERAL': 'string literal',
            'PAT_NUMERIC_LITERAL': 'numeric literal',
            'PAT_RESERVED_LITERAL': 'immutable operand',
            'PAT_IDENTIFIER': 'mutable operand',
            'PAT_PARANTHESIS': lambda t: f'{dict(PARANTHESIS="opening", OPERAND="closing").get(t.ruleName)} paranthesis',
            'PAT_BINARY_OPERATOR': 'binary operator',
            'PAT_UNARY_OPERATOR': 'unary operator'
        }
        match = re.search(r'\S', exprWithoutTokens)
        if match is not None:
            return f"occurance of unknown token '{match.group()}' found at {match.group()}"

        currentTokenRuleName = 'INITIAL_RULE'
        prevToken = None
        for token in self.__tokens:
            tokeRule = f'{token.tokenType}::{token.ruleName}'
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
