from typing import Self, Any

__all__ = ["TokenBase", "Token", "TokenOr", "TokenTree"]

class TokenBase:
    def __or__(self, other: 'TokenBase') -> 'TokenOr':
        return TokenOr(self, other)

class Token(TokenBase):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"<{self._name}>"
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def __eq__(self, other: Self) -> bool:
        return str(self) == str(other)
    
    def eq(self, *definition: list) -> 'GrammarRule':
        from .grammar import GrammarRule
        return GrammarRule(self, definition)

class TokenOr(TokenBase):
    def __init__(self, lhs: Token | Self, rhs: Token | Self) -> None:
        self._lhs = lhs
        self._rhs = rhs
    
    @property
    def tokens(self) -> tuple[Token, ...]:
        lhs: tuple[Token, ...] = (self._lhs,) if isinstance(self._lhs, Token) else self._lhs.tokens
        rhs: tuple[Token, ...] = (self._rhs,) if isinstance(self._rhs, Token) else self._rhs.tokens
        return lhs + rhs

    def __repr__(self) -> str:
        return " | ".join([str(t) for t in self.tokens])
    
class TokenTree:
    def __init__(self, root: Token) -> None:
        self.value: Any = None
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
            child_str = str(child).replace("\n", "\n\t")
            childs = f"{childs}\t{child_str}\n"
        return f"{self.root} ({self.value}){childs}"