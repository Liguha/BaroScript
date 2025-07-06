import operator
from typing import Iterator, Self
from itertools import product
from functools import cached_property, reduce
from .token import TokenBase, Token, TokenExpr, TokenOr, TokenAnd, TokenTree
from .tokenizer import Tokenizer

__all__ = ["GrammarRule", "Grammar"]

class GrammarRule:
    def __init__(self, target: Token, definition: TokenBase) -> None:
        self._target: Token = target
        self._definition: TokenBase = definition

    @property
    def target(self) -> Token:
        return self._target
    
    @property
    def definition(self) -> TokenBase:
        return self._definition
    
    def __iter__(self) -> Iterator:
        return (self.target, self.definition).__iter__()

    def __repr__(self) -> str:
        return f"{self.target} ::= {self.definition}"
    
class Grammar:
    def __init__(self, *rules: GrammarRule) -> None:
        self._rules: dict[Token, GrammarRule] = {}
        for rule in rules:
            if rule in self._rules:
                raise KeyError(f"Token {rule.target} has multiple definitions.")
            self._rules[rule] = rule
        self._cache: dict[tuple[Token, str], tuple[bool, TokenTree]] = {}

    @property
    def rules(self) -> list[GrammarRule]:
        return list(self._rules.values())
    
    def __repr__(self) -> str:
        return "\n".join([str(r) for r in self._rules.values()])
    
    def _match_tokenize(self, token: Token, content: str) -> None:
        key = (token, content)
        tokenizer = Tokenizer([tuple(r) for r in self.rules], token, content)
        self._cache[key] = (tokenizer.match(), tokenizer.tokenize())
    
    def match(self, token: TokenBase | str, content: str) -> bool:
        if isinstance(token, str):
            token = Token(token)
        key = (token, content)
        if key not in self._cache:
            self._match_tokenize(token, content)
        return self._cache[key][0]
    
    def tokenize(self, token: TokenBase | str, content: str) -> TokenTree:
        if isinstance(token, str):
            token = Token(token)
        if not self.match(token, content):
            part = content[:10]
            if len(content) > 10:
                part = f"{part}..."
            raise ValueError(f"String '{part}' doesn't match with pattern of {token}.")
        return self._cache[(token, content)][1]