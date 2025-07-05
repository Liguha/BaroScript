from .token import Token, TokenBase
from .state_machine import StateMachine

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
    
    def __iter__(self) -> tuple[Token, TokenBase]:
        return (self.target, self.definition)

    def __repr__(self) -> str:
        return f"{self.target} ::= {self.definition}"
    
class Grammar:
    def __init__(self, *rules: GrammarRule) -> None:
        self._rules: dict[Token, GrammarRule] = {}
        for rule in rules:
            if rule in self._rules:
                raise KeyError(f"Token {rule.target} has multiple definitions.")
            self._rules[rule] = rule

    def __repr__(self) -> str:
        return "\n".join([str(r) for r in self._rules.values()])
    
    # TODO: match and tokenize