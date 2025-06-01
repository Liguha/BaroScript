from dataclasses import dataclass

__all__ = ["Signal", "SignalIn", "SignalOut"]

@dataclass(frozen=True)
class Signal:
    name: str | None = None

@dataclass(frozen=True)
class SignalIn(Signal):
    pass

@dataclass(frozen=True)
class SignalOut(Signal):
    pass