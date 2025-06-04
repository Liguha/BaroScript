from typing import Any, Callable, Type, override
from functools import partialmethod, partial
from itertools import count
from uuid import uuid4
from abc import ABC, abstractmethod
from . import Tag, Signal, SignalIn, SignalOut

__all__ = ["Module", "SchemeModule", "create_scheme"]

class Module(ABC):
    _ids: count = count(1)
    _int_id: bool = False

    def __init_subclass__(cls) -> None:
        for key, value in cls.__base__.__dict__.items():
            if not isinstance(value, Signal):
                continue
            setattr(cls, key, value)
        if "__init__" in cls.__dict__:
            cls.__init__ = partialmethod(cls.__configure__, init=cls.__init__)
        if "__configure__" in cls.__dict__:
            raise SyntaxError(f"Do not override `__configure__` method (in class {cls.__name__}).")
        if "__setattr__" in cls.__dict__:
            raise SyntaxError(f"Do not override `__setattr__` method (in class {cls.__name__}).")
        
    def __configure__(self, *args: list[Any], init: Callable, **kwds: dict[str, Any]) -> None:
        self._inputs: tuple[Signal] = tuple()
        self._outputs: tuple[Signal] = tuple()
        inputs: list[str] = []
        outputs: list[str] = []
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, SignalIn):
                inputs.append(SignalIn(key, self))
                setattr(self, key, inputs[-1])
            if isinstance(value, SignalOut):
                outputs.append(SignalOut(key, self))
                setattr(self, key, outputs[-1])
        self._inputs = tuple(inputs)
        self._outputs = tuple(outputs)
        self._id: int | str = str(uuid4())
        if self._int_id:
            self._id = next(self._ids)
        self._submodules: set[Module] = set()
        self.__pre_init__()
        self._initialized: bool = True
        init(self, *args, **kwds)
        def raise_error(*args: list[Any], error: str, **kwds: dict[str, Any]) -> None:
            raise SyntaxError(error)
        self.connect = partial(raise_error, self=self, error="Do not use `connect` outside __init__.")
        
    def __setattr__(self, name: str, value: Any) -> None:
        if (name not in ["_inputs", "_outputs"] 
            and name in self.input_names + self.output_names):
            raise SyntaxError(f"Do not rewrite input/output value (instanse of the {self.__class__.__name__}).")
        return super().__setattr__(name, value)
    
    def __pre_init__(self) -> None:
        pass
        
    def __init__(self) -> None:
        def pass_func(*args, **kwds) -> None:
            pass
        self.__configure__(init=pass_func)

    def __hash__(self) -> None:
        return hash((self.__class__, self.id))

    @property
    def inputs(self) -> tuple[SignalIn]:
        return self._inputs
    
    @property
    def n_inputs(self) -> int:
        return len(self.inputs)
    
    @property
    def input_names(self) -> tuple[str]:
        return tuple([s.name for s in self.inputs])
    
    @property
    def outputs(self) -> tuple[SignalOut]:
        return self._outputs
    
    @property
    def n_outputs(self) -> int:
        return len(self.outputs)
    
    @property
    def output_names(self) -> tuple[str]:
        return tuple([s.name for s in self.outputs])
    
    @property
    def id(self) -> int | str:
        return self._id
    
    @abstractmethod
    def _connect_in(self, called_from: 'Module', signal: Signal) -> None:
        pass

    @abstractmethod
    def _connect_out(self, called_from: 'Module', signal: Signal,
                     *args: list[Any], **kwds: dict[str, Any]) -> None:
        pass
    
    def connect(self, signal1: Signal, signal2: Signal) -> None:
        if not hasattr(self, "_initialized") or not self._initialized:
            raise RuntimeError("`connect` is not allowed before initialization.")
        signals: tuple[Signal] = (signal1, signal2)
        if isinstance(signal1, SignalOut):
            signals = (signal2, signal1)
        if signals[1].handler == self:
            signals = signals[::-1]
        if signal1.handler != self:
            self._submodules.add(signal1.handler)
        if signal2.handler != self:
            self._submodules.add(signal2.handler)
        self._connect_out(self, signals[1], self._connect_in(self, signals[0]))

    @abstractmethod
    def compile(self) -> list[Tag]:
        pass

# ComponentModule in barotrauma folder because it contains game based logic
        
class SchemeModule(Module):
    def __pre_init__(self) -> None:
        self._lookup_table: dict[str, list[Signal]] = {}
        for name in self.input_names + self.output_names:
            self._lookup_table[name] = []

    @override
    def _connect_in(self, called_from: Module, signal: Signal) -> Signal | list:
        if signal.handler == self:
            if called_from == self:
                return signal
            arg_list: list = []
            for s in self._lookup_table[signal.name]:
                arg_list.extend(s.handler._connect_in(called_from, s))
            return arg_list
        return signal.handler._connect_in(called_from, signal)
            
    @override
    def _connect_out(self, called_from: Module, signal: Signal, connect_in: Signal | list) -> None:
        if isinstance(connect_in, Signal):
            if signal.handler == connect_in.handler:
                raise ValueError(f"Connection of the inputs/outputs signals from one module is disallowed (attempt to connect '{signal.name}' and '{connect_in.name}').")
            self._lookup_table[connect_in.name].append(signal)
            return
        if signal.handler == self:
            for s in self._lookup_table[signal.name]:
                s.handler._connect_out(called_from, s, connect_in)
            return
        return signal.handler._connect_out(called_from, signal, connect_in)

    @override
    def compile(self) -> str:
        compiled: list[Tag] = []
        for submodule in self._submodules:
            compiled.extend(submodule.compile())
        return compiled

def create_scheme(n_inputs: int, n_outputs: int, 
                  submodules: list[Module],
                  connections: list[tuple[tuple[int, int], tuple[int, int]]],
                  self_in_connection: list[list[tuple[int, int]]],
                  self_out_connection: list[list[tuple[int, int]]]) -> Type[SchemeModule]:
    """Simple scheme fabric.
    
    Args:
        n_inputs: Number of input signals.
        n_outputs: number of output signals.
        submodules: Used submodules - parts of the genereated module.
        connections: List with connections between submodules.
            connections = [((module1_idx, out_idx), (module2_idx, in_idx)), ...]
        self_in_connections: List of signals associated with self.inputs.
            self_in_connections = [[(module_idx, in_idx), ...], ...]
        self_out_connections: List of signals associated with self.outputs.
            self_out_connections = [[(module_idx, out_idx), ...], ...]

    Returns:
        New class with defined scheme.
    """
    def add_inputs_outputs(cls) -> type:
        for i in range(n_inputs):
            setattr(cls, f"in{i + 1}", SignalIn())
        for i in range(n_outputs):
            setattr(cls, f"out{i + 1}", SignalOut())
        return cls
    
    @add_inputs_outputs
    class CustomSchemeModule(SchemeModule):
        def __init__(self) -> None:
            for node1, node2 in connections:
                mod1_idx, signal_out = node1
                mod2_idx, signal_in = node2
                module1 = submodules[mod1_idx]
                module2 = submodules[mod2_idx]
                self.connect(module1.outputs[signal_out], module2.inputs[signal_in])
            for i, nodes in enumerate(self_in_connection):
                for mod_idx, signal_in in nodes:
                    module = submodules[mod_idx]
                    self.connect(self.inputs[i], module.inputs[signal_in])
            for i, nodes in enumerate(self_out_connection):
                for mod_idx, signal_out in nodes:
                    module = submodules[mod_idx]
                    self.connect(self.outputs[i], module.outputs[signal_out])

    return CustomSchemeModule
