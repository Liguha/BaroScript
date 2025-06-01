from functools import partial
from typing import Any
from .. import Tag

__all__ = ["ItemTag", "RequiredItemTag", "HoldableTag", "ConnectionPanelTag", "InputTag", "OutputTag",
           "MemoryComponentTag", "GreaterComponentTag",
           "AdderComponentTag", "SubstractComponentTag", "MultiplyComponentTag"]

class ItemTag(Tag):
    """\\<Item> tag, defaults set to logical components."""
    def __init__(self, 
                 name: str, 
                 identifier: str, 
                 ID: int, 
                 rect: tuple[int, int, int, int],
                 NonInteractable: bool = False, 
                 NonPlayerTeamInteractable: bool = False,
                 AllowSwapping: bool = True, 
                 Rotation: float = 0, 
                 Scale: float = 0.5,
                 SpriteColor: tuple[int, int, int, int] = (255, 255, 255, 255), 
                 InventoryIconColor: tuple[int, int, int, int] = (255, 255, 255, 255),
                 ContainerColor: tuple[int, int, int, int] = (255, 255, 255, 255), 
                 InvulnerableToDamage: bool = False,
                 Tags: tuple[str, ...] = ("smallitem", "logic"),
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
                 items: str = "wrench",
                 type: str = "Equipped",
                 optional: bool = False,
                 ignoreineditor: bool = False,
                 excludebroken: bool = True,
                 reuireempty: bool = False,
                 excludefullcondition: bool = False,
                 targetslot: int = -1,
                 allowvariants: bool = True,
                 rotation: int = 0,
                 setactive: bool = False) -> None:
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
                 PickingTime: int = 5,
                 CanBePicked: bool = True,
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
                 AllowInGameEditing: bool = True,
                 Msg: str = "") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("MemoryComponent", **kwargs)

class GreaterComponentTag(Tag):
    def __init__(self,
                 MaxOutputLength: int = 200,
                 Output: Any = 1,
                 FalseOutput: Any = None,
                 TimeFrame: int = 0,
                 PickingTime: int = 0,
                 CanBePicked: bool = False,
                 AllowInGameEditing: bool = True,
                 Msg: str = "") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("GreaterComponent", **kwargs)

class AdderComponentTag(Tag):
    def __init__(self,
                 ClampMax: int = 999999,
                 ClampMin: int = -999999,
                 TimeFrame: int = 0,
                 PickingTime: int = 0,
                 CanBePicked: bool = False,
                 AllowInGameEditing: bool = True,
                 Msg: str = "") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("AdderComponent", **kwargs)

# some ctrl+c ctrl+v - there is no better way :(
class SubstractComponentTag(Tag):
    def __init__(self,
                 ClampMax: int = 999999,
                 ClampMin: int = -999999,
                 TimeFrame: int = 0,
                 PickingTime: int = 0,
                 CanBePicked: bool = False,
                 AllowInGameEditing: bool = True,
                 Msg: str = "") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("SubstractComponent", **kwargs)

# some ctrl+c ctrl+v - there is no better way :(
class MultiplyComponentTag(Tag):
    def __init__(self,
                 ClampMax: int = 999999,
                 ClampMin: int = -999999,
                 TimeFrame: int = 0,
                 PickingTime: int = 0,
                 CanBePicked: bool = False,
                 AllowInGameEditing: bool = True,
                 Msg: str = "") -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("MultiplyComponent", **kwargs)
