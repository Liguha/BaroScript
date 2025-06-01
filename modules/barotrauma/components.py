from typing import Any, override
from itertools import count
from abc import abstractmethod
from .. import Module, Tag, SignalIn, SignalOut
from . import (ItemTag, 
               HoldableTag, 
               RequiredItemTag,
               ConnectionPanelTag, 
               InputTag,
               OutputTag,
               AdderComponentTag,
               SubstractComponentTag,
               MultiplyComponentTag,
               DivideComponentTag,
               GreaterComponentTag,
               EqualsComponentTag,
               AndComponentTag,
               OrComponentTag,
               XorComponentTag)

__all__ = ["RealModule", "Addition", "Substract", "Multiply", "Divide"]

class RealModule(Module):
    """Abstarction on Barotrauma logical component."""
    _need_id = True
    name: str | None = None
    component_tag: Tag | None = None

    @property
    @abstractmethod
    def tag_args(self) -> dict[str, Any]:
        pass

    @override
    def compile(self) -> str:
        inputs = [InputTag(name) for name in self.inputs]
        outputs = [OutputTag(name) for name in self.outputs]
        tag = ItemTag(name="", identifier=self.name, ID=self.id, rect=(0, 0, 16, 16))(
            self.component_tag(**self.tag_args),
            HoldableTag()(
                RequiredItemTag()
            ),
            ConnectionPanelTag()(
                RequiredItemTag(items=("scredriver",), excludedidentifiers=tuple()),
                *inputs,
                *outputs
            )
        )
        return str(tag)

#################################################################################
#
#                           LOGICAL ELEMENTS MODULES
#
#################################################################################

class ArithmeticModule(RealModule):
    signal_in1 = SignalIn()
    signal_in2 = SignalIn()
    signal_out = SignalOut()

    def __init__(self, min: int = -999999, max: int = 999999) -> None:
        self._min = min
        self._max = max

    @override
    @property
    def tag_args(self) -> dict[str, Any]:
        return {
            "ClampMax": self._max,
            "ClampMin": self._min,
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

class ConditionModule(RealModule):
    signal_in1 = SignalIn()
    signal_in2 = SignalIn()
    set_output = SignalIn()
    signal_out = SignalOut()

    def __init__(self, true_out: Any = 1, false_out: Any = 0, max_out_len: int = 200) -> None:
        self._true_out = true_out
        self._false_out = false_out
        self._max_out_len = max_out_len

    @override
    @property
    def tag_args(self) -> dict[str, Any]:
        return {
            "MaxOutputLength": self._max_out_len,
            "Output": self._true_out,
            "FalseOutput": self._false_out
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