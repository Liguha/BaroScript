from functools import cached_property
from .token import Token, TokenOr, TokenTree

__all__ = ["GrammarRule", "Grammar"]

class GrammarRule:
    def __init__(self, target: Token, definition: list[str | Token | TokenOr]) -> None:
        self._target = target
        self._definition = definition

    @property
    def target(self) -> Token:
        return self._target
    
    @property
    def definition(self) -> list[str | Token | TokenOr]:
        return self._definition

    def __repr__(self) -> str:
        return f"{self._target} ::= {"".join([str(x) for x in self._definition])}"
    
class Grammar:
    def __init__(self, *rules: list[GrammarRule]) -> None:
        self._rules: dict[Token, GrammarRule] = {}
        for rule in rules:
            if rule.target in self._rules:
                raise KeyError(f"Token {rule.target} has multiple definitions.")
            self._rules[rule.target] = rule

    def __repr__(self) -> str:
        return "\n".join([str(r) for r in self._rules.values()])

    def _match(self, rule: list[str | Token | TokenOr], content: str) -> bool:
        if len(content) == 0:
            return True
        if len(rule) == 0:
            return False
        for r in rule:
            if isinstance(r, str):
                if not content.startswith(r):
                    return False
                return self._match(rule[1:], content[(len(r)):]) 
            if isinstance(r, Token):
                return self._match(self._rules[r].definition + rule[1:], content)
            if isinstance(r, TokenOr):
                for t in r.tokens:
                    if self._match(self._rules[t].definition + rule[1:], content):
                        return True
                return False
            
    def match(self, token: str | Token, content: str) -> bool:
        token: Token = Token(token) if isinstance(token, str) else token
        return self._match(self._rules[token].definition, content)
    
    def _tokenize(self, node: TokenTree, rule: list[str | Token | TokenOr], content: str) -> TokenTree:
        if len(content) == 0:
            return None
        if len(rule) == 0:
            raise ValueError("Tokenisation error.")
        
    def tokenize(self, root: Token, content: str) -> TokenTree:
        pass
    