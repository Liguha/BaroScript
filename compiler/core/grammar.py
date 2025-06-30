from functools import cached_property
from .token import Token, TokenOr, TokenTree

__all__ = ["GrammarRule", "Grammar"]

class GrammarRule:
    def __init__(self, target: Token, definition: list[str | Token | TokenOr]) -> None:
        self._target = target
        self._definition = list(definition)

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

    def _match(self, rule: list[str | Token | TokenOr], content: str) -> tuple[bool, list[str | Token]]:
        if len(content) == 0:
            return True, []
        if len(rule) == 0:
            return False, None
        r = rule[0]
        if isinstance(r, str):
            if not content.startswith(r):
                return False, None
            a, b = self._match(rule[1:], content[(len(r)):]) 
            return a, [r] + b
        if isinstance(r, Token):
            a, b = self._match(self._rules[r].definition + rule[1:], content)
            return a, [r] + b
        if isinstance(r, TokenOr):
            for t in r.tokens:
                a, b = self._match(self._rules[t].definition + rule[1:], content)
                if a:
                    return True, [t] + b
        return False, None
            
    def match(self, token: str | Token, content: str) -> bool:
        token: Token = Token(token) if isinstance(token, str) else token
        res, _ = self._match([token], content)
        return res   
    
    def _tokenize(self, node: TokenTree, rule: list[str | Token | TokenOr], seq: list[str | Token]) -> list[str | Token]:
        if len(rule) == 0:
            return seq
        r = rule[0]
        if isinstance(r, str):
            node.value += r
            return self._tokenize(node, rule[1:], seq[1:])
        if len(seq) == 0:
            return []
        t = seq[0]
        child = TokenTree(t)
        rem_rule = rule[1:]
        rem_seq = self._tokenize(child, self._rules[t].definition, seq[1:])
        node.add_child(child)
        return self._tokenize(node, rem_rule, rem_seq)

    def tokenize(self, root: str | Token, content: str) -> TokenTree:
        root: Token = Token(root) if isinstance(root, str) else root
        state, seq = self._match([root], content)
        print(seq)
        if not state:
            raise ValueError("Tokenization error.")
        node = TokenTree(root)
        self._tokenize(node, self._rules[root].definition, seq[1:])
        return node