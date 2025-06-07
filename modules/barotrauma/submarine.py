import gzip
from pathlib import Path
from functools import cached_property
from ..core import Module, Tag

__all__ = ["SubmarineBuilder", "GAME_VERSION"]

GAME_VERSION: str = "1.8.8.1"

# <class="Undefined">
class SubmarineMainTag(Tag):
    def __init__(self,
                 name: str,
                 description: str = "",
                 checkval: int = 0,
                 price: int = 1000,
                 tier: int = 1,
                 initialsuppliesspawned: bool = False,
                 noitems: bool = False,
                 lowfuel: bool = True,
                 type: str = "Player",
                 ismanuallyoutfitted: bool = False,
                 tags: tuple[str, ...] = (0,),
                 outposttags: tuple[str, ...] = tuple(),
                 triggeroutpostmissionevents: str = None,
                 gameversion: str = GAME_VERSION,
                 dimensions: tuple[int, int] = (0, 0),
                 cargocapacity: int = 0,
                 recommendedcrewsizemin: int = 1,
                 recommendedcrewsizemax: int = 2,
                 recommendedcrewexperience: str = "CrewExperienceLow",
                 requiredcontentpackages: tuple[str, ...] = tuple()) -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("Submarine", **kwargs)
        self.stringifier[bool] = lambda x: str(x).lower()

class SubmarineAdditionalTag(Tag):
    def __init__(self, name: str) -> None:
        super().__init__("Submarine", file=f"%ModDir%/{name}.sub")
    
class ContentPackageTag(Tag):
    def __init__(self,
                 name: str,
                 modversion: str = "1.0.0",
                 corepackage: bool = "False",
                 gameversion: str = GAME_VERSION) -> None:
        kwargs: dict = locals().copy()
        kwargs.pop("self")
        kwargs.pop("__class__")
        super().__init__("contentpackage", **kwargs)

class SubmarineBuilder:
    def __init__(self, name: str, modules: list[Module]) -> None:
        self._name = name
        self._modules = tuple(modules)

    @cached_property
    def tags(self) -> list[Tag]:
        tags: list[Tag] = []
        for module in self._modules:
            tags.extend(module.compile())
        return tags

    def save(self, save_dir: Path | str) -> None:
        if isinstance(save_dir, str):
            save_dir = Path(save_dir)
        save_dir = save_dir / self._name
        save_dir.mkdir(parents=True, exist_ok=True)
        meta_tag = ContentPackageTag(self._name)(SubmarineAdditionalTag(self._name))
        data_tag = SubmarineMainTag(self._name)(*self.tags)
        with (save_dir / "filelist.xml").open("w") as file:
            file.write(str(meta_tag))
        sub_path = save_dir / self._name
        with gzip.open(sub_path, "wt") as file:
            file.write(str(data_tag))
            sub_path.rename(save_dir / f"{self._name}.sub")