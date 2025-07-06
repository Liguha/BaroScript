from dataclasses import dataclass
from .token import TokenBase, Token, TokenString, TokenAnd, TokenOr, TokenTree

__all__ = ["Tokenizer"]

@dataclass(frozen=True)
class State:
    token: Token
    str_pos: int

class Tokenizer:
    """Works only with LL-grammar"""
    def __init__(self, rules: list[tuple[Token, TokenBase]], token: TokenBase, content: str) -> None:
        self._rules: dict[Token, TokenBase] = {k: v for k, v in rules}
        self._token: TokenBase = token
        self._content: str = content
        self._cache: dict[State, int] = {}
        self._match: bool | None = None
        self._trace: TokenTree | None = None

    def _dfs(self, cur_state: State, node: TokenTree) -> int:
        if cur_state in self._cache:
            return self._cache[cur_state]
        self._cache[cur_state] = -1
        token: TokenBase = cur_state.token
        if isinstance(token, TokenString):
            match_res = token.regexp.match(self._content, cur_state.str_pos)
            if not match_res:
                self._cache[cur_state] = -1
            else:
                node.value += match_res[0]
                self._cache[cur_state] = cur_state.str_pos + len(match_res[0])
        if isinstance(token, Token):
            child = TokenTree(token)
            shift = self._dfs(State(self._rules[token], cur_state.str_pos), child)
            if shift >= 0:
                node.add_child(child)
            self._cache[cur_state] = shift
        if isinstance(token, TokenAnd):
            shift = cur_state.str_pos
            for t in token:
                shift = self._dfs(State(t, shift), node)
                if shift < 0:
                    break
            self._cache[cur_state] = shift
        if isinstance(token, TokenOr):
            for t in token:
                shift = self._dfs(State(t, cur_state.str_pos), node)
                if shift >= 0:
                    self._cache[cur_state] = shift
                    break
        return self._cache[cur_state]
        
    def _match_tokenize(self) -> None:
        self._trace = TokenTree(Token("MAIN ROOT"))
        k = self._dfs(State(self._token, 0), self._trace)
        self._match = bool(k == len(self._content))

    def match(self) -> bool:
        if self._match is None:
            self._match_tokenize()
        return self._match
    
    def tokenize(self) -> TokenTree | None:
        if self._match is None:
            self._match_tokenize()
        return self._trace