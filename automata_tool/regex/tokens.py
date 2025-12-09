
from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    CHAR = auto()
    STAR = auto()
    PLUS = auto()
    QUESTION = auto()
    UNION = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
