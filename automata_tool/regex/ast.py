
from abc import ABC

class RegexNode(ABC):
    pass

class Literal(RegexNode):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def __repr__(self) -> str:
        return f"Literal({self.symbol!r})"

class Concat(RegexNode):
    def __init__(self, left: 'RegexNode', right: 'RegexNode') -> None:
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Concat({self.left!r}, {self.right!r})"

class Union(RegexNode):
    def __init__(self, left: 'RegexNode', right: 'RegexNode') -> None:
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Union({self.left!r}, {self.right!r})"

class Star(RegexNode):
    def __init__(self, child: 'RegexNode') -> None:
        self.child = child

    def __repr__(self) -> str:
        return f"Star({self.child!r})"

class Plus(RegexNode):
    def __init__(self, child: 'RegexNode') -> None:
        self.child = child

    def __repr__(self) -> str:
        return f"Plus({self.child!r})"

class Optional(RegexNode):
    def __init__(self, child: 'RegexNode') -> None:
        self.child = child

    def __repr__(self) -> str:
        return f"Optional({self.child!r})"
