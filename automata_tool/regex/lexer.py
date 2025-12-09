
from .tokens import TokenType, Token

class Lexer:
    """Simple lexer for regular expressions.

    Supports:
    - literal characters: a-z, 0-9
    - operators: | * + ?
    - parentheses: ( )
    - ignores whitespace
    """

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0

    def _advance(self) -> str:
        ch = self.text[self.pos]
        self.pos += 1
        return ch

    def _peek(self) -> str:
        if self.pos >= len(self.text):
            return ""
        return self.text[self.pos]

    def next_token(self) -> Token:
        while self.pos < len(self.text):
            ch = self._peek()
            if ch.isspace():
                self._advance()
                continue
            if ch == "|":
                self._advance()
                return Token(TokenType.UNION, ch)
            if ch == "*":
                self._advance()
                return Token(TokenType.STAR, ch)
            if ch == "+":
                self._advance()
                return Token(TokenType.PLUS, ch)
            if ch == "?":
                self._advance()
                return Token(TokenType.QUESTION, ch)
            if ch == "(":
                self._advance()
                return Token(TokenType.LPAREN, ch)
            if ch == ")":
                self._advance()
                return Token(TokenType.RPAREN, ch)

            # Literal character: allow a-z, 0-9 explicitly, and optionally others
            if ch.isalnum():
                self._advance()
                return Token(TokenType.CHAR, ch)

            raise SyntaxError(f"Carácter no válido en expresión regular: {ch!r}")

        return Token(TokenType.EOF, "")
