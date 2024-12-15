from dataclasses import dataclass
from typing import Self

@dataclass
class Token:
    groupValue: str
    ruleName: str
    startPos: int
    endPos: int
    patternName: str
    tokenType: str

    @property
    def NOT_A_TOKEN(self):
        return 'NO_TOKEN'

    def __repr__(self):
        return f"Token(groupValue='{self.groupValue}', ruleName='{self.ruleName}', tokenType='{self.tokenType}' " + \
            f"startPos={self.startPos}, endPos={self.endPos}, patternName='{self.patternName}')"

    def is_operand(self):
        return self.tokenType == 'OPERAND'
    
    def is_operator(self):
        return self.tokenType == 'OPERATOR'
    
    def is_paranthesis(self):
        return self.tokenType == 'PARANTHESIS'
