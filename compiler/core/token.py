from __future__ import annotations
import re
from re import Pattern
from abc import ABC, abstractmethod
from typing import Self, Generator, TYPE_CHECKING
if TYPE_CHECKING: from .grammar import GrammarRule

__all__ = ["TokenBase", "Token", "TokenString", "TokenExpr", "TokenOr", "TokenAnd", "TokenTree"]

class TokenBase(ABC):
    def __or__(self, other: Self | str) -> 'TokenOr':
        if isinstance(other, str):
            other = TokenString(other)
        return TokenOr(self, other)
    
    def __ror__(self, other: Self | str) -> 'TokenOr':
        if isinstance(other, str):
            other = TokenString(other)
        return TokenOr(other, self)
    
    def __and__(self, other: Self | str) -> 'TokenAnd':
        if isinstance(other, str):
            other = TokenString(other)
        return TokenAnd(self, other)
    
    def __rand__(self, other: Self | str) -> 'TokenAnd':
        if isinstance(other, str):
            other = TokenString(other)
        return TokenAnd(other, self)
    
    @abstractmethod
    def __repr__(self) -> str:
        pass
    
    @abstractmethod
    def __iter__(self) -> Generator[Self, None, None]:
        pass
    
class Token(TokenBase):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def __eq__(self, other: Self) -> bool:
        return str(self) == str(other)
    
    def eq(self, definition: TokenBase | str) -> GrammarRule:
        from .grammar import GrammarRule
        if isinstance(definition, str):
            definition = TokenString(definition)
        return GrammarRule(self, definition)
    
    def __repr__(self) -> str:
        return f"<{self.name}>"
    
    def __iter__(self) -> Generator['Token', None, None]:
        yield self
    
class TokenString(TokenBase):
    def __init__(self, pattern: str) -> None:
        self._pattern = pattern
        self._regexp: Pattern = re.compile(pattern)

    @property
    def regexp(self) -> Pattern:
        return self._regexp
    
    def __repr__(self) -> str:
        return f'"{self._pattern}"'
    
    def __iter__(self) -> Generator['TokenString', None, None]:
        yield self
    
class TokenExpr(TokenBase):
    def __init__(self, lhs: TokenBase, rhs: TokenBase) -> None:
        self._parts: tuple[TokenBase, TokenBase] = (lhs, rhs)

    def __iter__(self) -> Generator['TokenExpr', None, None]:
        for part in self._parts:
            if isinstance(part, type(self)):
                for t in part:
                    yield t
            else:
                yield part

class TokenOr(TokenExpr):
    def __repr__(self) -> str:
        childs = [f"({t})" if isinstance(t, TokenExpr) else str(t) for t in self]
        return f"{" | ".join(childs)}"
    
class TokenAnd(TokenExpr):
    def __repr__(self) -> str:
        childs = [f"({t})" if isinstance(t, TokenExpr) else str(t) for t in self]
        return f"{" ".join(childs)}"
    
class TokenTree:
    def __init__(self, root: Token) -> None:
        self.value: str = ""
        self._root = root
        self._childs = []

    def add_child(self, child: Token | Self) -> None:
        if isinstance(child, Token):
            child = TokenTree(child)
        self._childs.append(child)

    @property
    def root(self) -> Token:
        return self._root

    @property
    def childs(self) -> tuple[Self, ...]:
        return tuple(self._childs)
    
    def __repr__(self) -> str:
        childs: str = ""
        for child in self.childs:
            if len(childs) == 0:
                childs = "\n"
            child_str = str(child).removesuffix("\n").replace("\n", "\n\t")
            childs = f"{childs}\t{child_str}\n"
        return f"{self.root} ({self.value}){childs}"