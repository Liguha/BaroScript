from functools import partial
from typing import Any
from .. import Tag

__all__ = ["ItemTag", "RequiredItemTag", "HoldableTag", "ConnectionPanelTag", "InputTag", "OutputTag",
           "MemoryComponentTag", "ConditionComponentTag", "ArithmeticComponentTag",
           "SignalCheckComponentTag", "GreaterComponentTag", "EqualsComponentTag", "AndComponentTag", "OrComponentTag", "XorComponentTag",
           "AdderComponentTag", "SubstractComponentTag", "MultiplyComponentTag", "DivideComponentTag"]

class ItemTag(Tag):
    """\\<Item> tag, defaults set to logical components."""
    def __init__(self, 
                 name: str, 
                 identifier: str, 
                 ID: int, 
                 rect: tuple[int, int, int, int],
                 markedfordeconstruction: bool = False,
                 NonInteractable: bool = False, 
                 NonPlayerTeamInteractable: bool = False,
                 AllowSwapping: bool = True, 
                 Rotation: float = 0, 
                 Scale: float = 0.5,
                 SpriteColor: tuple[int, int, int, int] = (255, 255, 255, 255), 
                 InventoryIconColor: tuple[int, int, int, int] = (255, 255, 255, 255),
                 ContainerColor: tuple[int, int, int, int] = (255, 255, 255, 255), 
                 InvulnerableToDamage: bool = False,
                 Tags: tuple[str, ...] = ("smallitem", "circuitboxcomponent", "logic"),
                 DisplaySideBySideWhenLinked: bool = False,
                 DisallowedUpgrades: tuple[str, ...] = tuple(),
                 SpriteDepth: float = 0.8,
                 HiddenInGame: bool = False,
                 conditionpercentage: int = 100) -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("Item", **kwargs)

class RequiredItemTag(Tag):
    """\\<requireditem> tag, defaults set to logical components."""
    def __init__(self,
                 items: tuple[str, ...] = ("wrench", "deattachtool"),
                 type: str = "Equipped",
                 characterinventoryslottype: str = "None",
                 optional: bool = False,
                 ignoreineditor: bool = False,
                 excludebroken: bool = True,
                 reuireempty: bool = False,
                 excludefullcondition: bool = False,
                 targetslot: int = -1,
                 allowvariants: bool = True,
                 rotation: int = 0,
                 setactive: bool = False,
                 excludedidentifiers: tuple[str, ...] = ("multitool",)) -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("requireditem", **kwargs)
        self.stringifier[bool] = lambda x: str(x).lower()

class HoldableTag(Tag):
    """\\<Holdable> tag, defaults set to logical components."""
    def __init__(self,
                 Attached: bool = True,
                 SpriteDepthWhenDropped: float = 0.55,
                 MsgWhenDropped: str = "ItemMsgPickupSelect",
                 PickingTime: int = 5,
                 CanBePicked: bool = True,
                 LockGuiFramePosition: bool = False,
                 GuiFrameOffset: tuple[int, int] = (0, 0),
                 AllowInGameEditing: bool = True,
                 Msg: str = "ItemMsgDetachWrench") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("Holdable", **kwargs)

class ConnectionPanelTag(Tag):
    """\\<ConnectionPanel> tag, defaults set to logical components."""
    def __init__(self,
                 Locked: bool = False,
                 PickingTime: int = 0,
                 CanBePicked: bool = False,
                 LockGuiFramePosition: bool = False,
                 GuiFrameOffset: tuple[int, int] = (0, 0),
                 AllowInGameEditing: bool = True,
                 Msg: str = "ItemMsgRewireScrewdriver") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("ConnectionPanel", **kwargs)

class InputTag(Tag):
    """\\<input> tag."""
    def __init__(self, name: str) -> None:
        super().__init__("input", name=name)

class OutputTag(Tag):
    """\\<output> tag."""
    def __init__(self, name: str) -> None:
        super().__init__("output", name=name)

#################################################################################
#
#                           LOGICAL ELEMENTS TAGS
#
#################################################################################

class MemoryComponentTag(Tag):
    def __init__(self,
                 MaxValueLength: int = 200,
                 Value: Any = None,
                 Writable: bool = True,
                 PickingTime: int = 0,
                 CanBePicked: bool = False,
                 LockGuiFramePosition: bool = False,
                 GuiFrameOffset: tuple[int, int] = (0, 0),
                 AllowInGameEditing: bool = True,
                 Msg: str = "") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("MemoryComponent", **kwargs)

class ConditionComponentTag(Tag):
    """Some generalization - not real tag."""
    _tagname: str | None = None
    def __init__(self,
                 MaxOutputLength: int = 200,
                 Output: Any = 1,
                 FalseOutput: Any = None,
                 TimeFrame: int = 0,
                 PickingTime: int = 0,
                 CanBePicked: bool = False,
                 LockGuiFramePosition: bool = False,
                 GuiFrameOffset: tuple[int, int] = (0, 0),
                 AllowInGameEditing: bool = True,
                 Msg: str = "") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__(self._tagname, **kwargs)

class SignalCheckComponentTag(ConditionComponentTag):
    _tagname: str = "SignalCheckComponent"

class GreaterComponentTag(ConditionComponentTag):
    _tagname: str = "GreaterComponent"

class EqualsComponentTag(ConditionComponentTag):
    _tagname: str = "EqualsComponent"

class AndComponentTag(ConditionComponentTag):
    _tagname: str = "AndComponent"

class OrComponentTag(ConditionComponentTag):
    _tagname: str = "OrComponent"

class XorComponentTag(ConditionComponentTag):
    _tagname: str = "XorComponent"

class ArithmeticComponentTag(Tag):
    """Some generalization - not real tag."""
    _tagname: str | None = None
    def __init__(self,
                 ClampMax: int = 999999,
                 ClampMin: int = -999999,
                 TimeFrame: int = 0,
                 PickingTime: int = 0,
                 CanBePicked: bool = False,
                 LockGuiFramePosition: bool = False,
                 GuiFrameOffset: tuple[int, int] = (0, 0),
                 AllowInGameEditing: bool = True,
                 Msg: str = "") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__(self._tagname, **kwargs)

class AdderComponentTag(ArithmeticComponentTag):
    _tagname: str = "AdderComponent"

class SubstractComponentTag(ArithmeticComponentTag):
    _tagname: str = "SubstractComponent"

class MultiplyComponentTag(ArithmeticComponentTag):
    _tagname: str = "MultiplyComponent"

class DivideComponentTag(ArithmeticComponentTag):
    _tagname: str = "DivideComponent"

# TODO: add another