from .token import Token, TokenBase

__all__ = ["StateMachine"]

# TODO: grammar traversing with caching
class StateMachine:
    def __init__(self, rules: dict[Token, TokenBase], content: str) -> None:
        pass

    def forward(self) -> Token | None:
        pass

    def backward(self) -> None:
        pass