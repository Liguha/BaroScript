from typing import Any, Literal, override
from itertools import count
from abc import abstractmethod
from .tags import *
from .. import Module, Tag, SignalIn, SignalOut

__all__ = ["ComponentModule", "Addition", "Substract", "Multiply", "Divide"]

class _WireModule(Module):
    """Not module - used only to get wire ID."""
    _int_id = True

    @override
    def _connect_in(self) -> None:
        raise NotImplementedError("This `Module` is used only for ID generating and wire tagging.")
    
    @override
    def _connect_out(self) -> None:
        raise NotImplementedError("This `Module` is used only for ID generating and wire tagging.")
    
    @override
    def compile(self) -> list[Tag]:
        tag = ItemTag("", identifier="redwire", 
                      ID=self.id, 
                      rect=(0, 0, 42, 16), 
                      Tags=("wire", "smallitem"),
                      SpriteColor=(254, 23, 17, 255),
                      InventoryIconColor=(254, 23, 17, 255))(
            HoldableTag(Attached=False, MsgWhenDropped=""),
            WireTag(nodes=[8, -8, 8, -8])
        )
        return [tag]

class ComponentModule(Module):
    """Abstarction on Barotrauma logical component."""
    _int_id = True
    name: str | None = None
    component_tag: Tag | None = None

    def __pre_init__(self) -> None:
        self._connections: dict[str, list[int]] = {}
        for name in self.input_names + self.output_names:
            self._connections[name] = []

    @property
    @abstractmethod
    def tag_args(self) -> dict[str, Any]:
        pass

    @override
    def _connect_in(self, called_from: Module, signal: SignalIn) -> list[_WireModule]:
        if signal.handler != self:
            return []
        wire: Module = _WireModule()
        self._submodules.add(wire)
        self._connections[signal.name].append(wire.id)
        return [wire]
    
    @override
    def _connect_out(self, called_from: Module, signal: SignalOut, connect_in: list[_WireModule]) -> None:
        if signal.handler != self:
            return
        self._connections[signal.name].extend([w.id for w in connect_in])

    @override
    def compile(self) -> list[Tag]:
        inputs = [InputTag(name)(*[LinkTag(w=wid, i=0) for wid in self._connections[name]]) 
                  for name in self.input_names]
        outputs = [OutputTag(name)(*[LinkTag(w=wid, i=1) for wid in self._connections[name]]) 
                   for name in self.output_names]
        tag = ItemTag(name="", identifier=self.name, ID=self.id, rect=(0, 0, 16, 16))(
            self.component_tag(**self.tag_args),
            HoldableTag()(
                RequiredItemTag()
            ),
            ConnectionPanelTag()(
                RequiredItemTag(items=("screwdriver",), excludedidentifiers=tuple()),
                *inputs,
                *outputs
            )
        )
        tags: list[Tag] = [tag]
        for submodule in self._submodules:
            tags.extend(submodule.compile())
        return tags

#################################################################################
#
#                           LOGICAL ELEMENTS MODULES
#
#################################################################################

class ArithmeticModule(ComponentModule):
    signal_in1 = SignalIn()
    signal_in2 = SignalIn()
    signal_out = SignalOut()

    def __init__(self, min: int = -999999, max: int = 999999, tag_args: dict[str, Any] = {}) -> None:
        self._min = min
        self._max = max
        self._kwargs = tag_args

    @override
    @property
    def tag_args(self) -> dict[str, Any]:
        return {
            "ClampMax": self._max,
            "ClampMin": self._min,
            **self._kwargs
        }

class Addition(ArithmeticModule):
    name = "addercomponent"
    component_tag = AdderComponentTag

class Substract(ArithmeticModule):
    name = "subtractcomponent"
    component_tag = SubstractComponentTag
    
class Multiply(ArithmeticModule):
    name = "multiplycomponent"
    component_tag = MultiplyComponentTag

class Divide(ArithmeticModule):
    name = "dividecomponent"
    component_tag = DivideComponentTag

class ConditionModule(ComponentModule):
    signal_in1 = SignalIn()
    signal_in2 = SignalIn()
    set_output = SignalIn()
    signal_out = SignalOut()

    def __init__(self, true_out: Any = 1, false_out: Any = 0, max_out_len: int = 200, tag_args: dict[str, Any] = {}) -> None:
        self._true_out = true_out
        self._false_out = false_out
        self._max_out_len = max_out_len
        self._kwargs = tag_args

    @override
    @property
    def tag_args(self) -> dict[str, Any]:
        return {
            "MaxOutputLength": self._max_out_len,
            "Output": self._true_out,
            "FalseOutput": self._false_out,
            **self._kwargs
        }
    
class Greater(ConditionModule):
    name = "greatercomponent"
    component_tag = GreaterComponentTag

class Equal(ConditionModule):
    name = "equalscomponent"
    component_tag = EqualsComponentTag

class And(ConditionModule):
    name = "andcomponent"
    component_tag = AndComponentTag

class Or(ConditionModule):
    name = "orcomponent"
    component_tag = OrComponentTag

class Xor(ConditionModule):
    name = "xorcomponent"
    component_tag = XorComponentTag