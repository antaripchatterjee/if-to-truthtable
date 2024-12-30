from dataclasses import dataclass
from typing import Self

@dataclass
class Token:
    groupValue: str
    startPos: int
    endPos: int
    ruleName: str
    className: str

    @property
    def NOT_A_TOKEN(self):
        return 'NO_TOKEN'

    def __repr__(self):
        return f"Token(groupValue='{self.groupValue}', startPos={self.startPos}, endPos={self.endPos}, " + \
            f"className='{self.className}', ruleName='{self.ruleName}')"

    def is_operand(self):
        return self.className == 'OPERAND' or (self.className == 'PARANTHERIS' and self.ruleName == 'CLOSE_PARAN')
    
    def is_operator(self):
        return self.className == 'OPERATOR'
    
    def is_paranthesis(self):
        return self.className == 'PARANTHESIS' and self.ruleName == 'OPEN_PARAN'
