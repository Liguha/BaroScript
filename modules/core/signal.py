from dataclasses import dataclass
from weakref import ref

__all__ = ["Signal", "SignalIn", "SignalOut"]

@dataclass(frozen=True)
class Signal:
    name: str = None
    _handler: 'Module' = None

    def __post_init__(self) -> None:
        if self._handler is not None:
            object.__setattr__(self, "_handler", ref(self._handler))    # hack to change frozen :)

    @property
    def handler(self) -> 'Module':
        if self._handler is None:
            return None
        return self._handler()

@dataclass(frozen=True)
class SignalIn(Signal):
    pass

@dataclass(frozen=True)
class SignalOut(Signal):
    pass