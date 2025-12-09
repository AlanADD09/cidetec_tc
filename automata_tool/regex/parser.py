
from .tokens import TokenType, Token
from .lexer import Lexer
from .ast import RegexNode, Literal, Concat, Union, Star, Plus, Optional

class Parser:
    """Recursive-descent parser for regular expressions.

    Grammar:

        regex   ::= union
        union   ::= concat ('|' concat)*
        concat  ::= repeat+
        repeat  ::= atom ('*' | '+' | '?')*
        atom    ::= CHAR | '(' regex ')'
    """

    def __init__(self, text: str) -> None:
        self.lexer = Lexer(text)
        self.current: Token = self.lexer.next_token()

    def _eat(self, token_type: TokenType) -> None:
        if self.current.type == token_type:
            self.current = self.lexer.next_token()
        else:
            raise SyntaxError(f"Se esperaba token {token_type}, se encontró {self.current.type}")

    def parse(self) -> RegexNode:
        node = self._regex()
        if self.current.type != TokenType.EOF:
            raise SyntaxError("Expresión regular inválida: tokens restantes inesperados.")
        return node

    def _regex(self) -> RegexNode:
        return self._union()

    def _union(self) -> RegexNode:
        node = self._concat()
        while self.current.type == TokenType.UNION:
            self._eat(TokenType.UNION)
            right = self._concat()
            node = Union(node, right)
        return node

    def _concat(self) -> RegexNode:
        node = self._repeat()
        # concatenation is implicit: if next token starts an atom, it's concatenation
        while self.current.type in (TokenType.CHAR, TokenType.LPAREN):
            right = self._repeat()
            node = Concat(node, right)
        return node

    def _repeat(self) -> RegexNode:
        node = self._atom()
        while self.current.type in (TokenType.STAR, TokenType.PLUS, TokenType.QUESTION):
            if self.current.type == TokenType.STAR:
                self._eat(TokenType.STAR)
                node = Star(node)
            elif self.current.type == TokenType.PLUS:
                self._eat(TokenType.PLUS)
                node = Plus(node)
            elif self.current.type == TokenType.QUESTION:
                self._eat(TokenType.QUESTION)
                node = Optional(node)
        return node

    def _atom(self) -> RegexNode:
        if self.current.type == TokenType.CHAR:
            tok = self.current
            self._eat(TokenType.CHAR)
            return Literal(tok.value)
        if self.current.type == TokenType.LPAREN:
            self._eat(TokenType.LPAREN)
            node = self._regex()
            self._eat(TokenType.RPAREN)
            return node
        raise SyntaxError(f"Token inesperado en átomo: {self.current.type}")
