from typing import Any, Callable
from functools import partialmethod
from itertools import count
from abc import ABC, abstractmethod
from . import Signal, SignalIn, SignalOut

__all__ = ["Module"]

class Module(ABC):
    _ids: count = count(1)
    _need_id: bool = False

    def __init_subclass__(cls) -> None:
        cls.__init__ = partialmethod(cls.__pre_init__, init=cls.__init__)
        if "__pre_init__" in cls.__dict__:
            raise SyntaxError(f"Do not override `__pre_init__` method (in class {cls.__name__}).")
        if "__setattr__" in cls.__dict__:
            raise SyntaxError(f"Do not override `__setattr__` method (in class {cls.__name__}).")
        
    def __pre_init__(self, *args: list[Any], init: Callable, **kwds: dict[str, Any]) -> None:
        if not hasattr(self, "_initilized") or not self._initialized:
            self._inputs: tuple[str] = tuple()
            self._outputs: tuple[str] = tuple()
            inputs: list[str] = []
            outputs: list[str] = []
            for key, value in self.__class__.__dict__.items():
                if isinstance(value, SignalIn):
                    inputs.append(key)
                    setattr(self, key, SignalIn(key))
                if isinstance(value, SignalOut):
                    outputs.append(key)
                    setattr(self, key, SignalOut(key))
            self._inputs = tuple(inputs)
            self._outputs = tuple(outputs)
            self._connections: set[tuple[str, str]] = set()
            self._id: int = -1
            if self._need_id:
                self._id = next(self._ids)
            self._initialized: bool = True
        init(self, *args, **kwds)
        
    def __setattr__(self, name: str, value: Any) -> None:
        if (name not in ["_inputs", "_outputs"] 
            and name in self.inputs + self.outputs):
            raise SyntaxError(f"Do not rewrite input/output value (instanse of the {self.__class__.__name__}).")
        return super().__setattr__(name, value)
        
    def __init__(self) -> None:
        pass

    @property
    def inputs(self) -> tuple[str]:
        return self._inputs
    
    @property
    def outputs(self) -> tuple[str]:
        return self._outputs
    
    @property
    def id(self) -> int:
        return self._id
    
    @abstractmethod
    def _connect_in(self, signal: SignalIn) -> None:
        pass

    @abstractmethod
    def _connect_out(self, signal: SignalOut) -> None:
        pass
    
    def connect(self, signal1: Signal, signal2: Signal) -> None:
        if not hasattr(self, "_initilized") or not self._initialized:
            raise RuntimeError("`connect` is not allowed before initialization.")
        self._connections.add((signal1.name, signal2.name))

    @abstractmethod
    def compile(self) -> str:
        pass
        