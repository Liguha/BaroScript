from typing import Any, Callable
from ..utils import Stringifier

__all__ = ["Tag"]

class Tag:
    def __init__(self, tag_name: str, 
                 stringify_rules: dict[type, Callable[[Any], str]] | None = None, 
                 /, **kwds: dict[str, Any]) -> None:
        self._name: str = tag_name
        self._attributes: dict[str, Any] = kwds
        self._childs: list[Tag] = []
        self._stringifier: Stringifier = Stringifier(stringify_rules)
        for key, value in self.attributes:
            setattr(self, key, value)
    
    def add_childs(self, *child: list['Tag']) -> None:
        self._childs.extend(child)

    @property
    def childs(self) -> tuple['Tag', ...]:
        return tuple(self._childs)
    
    @property
    def tagname(self) -> str:
        return self._name
    
    @property
    def attributes(self) -> tuple[tuple[str, Any], ...]:
        return tuple(self._attributes.items())
    
    @property
    def stringifier(self) -> Stringifier:
        return self._stringifier
    
    def __getiitem__(self, attribute: str) -> Any:
        return self._attributes.get(attribute)
    
    def __setitem__(self, attribute: str, value: Any) -> None:
        if attribute not in self._attributes:
            setattr(self, attribute, value)
        self._attributes[attribute] = value

    def __call__(self, *childs: tuple['Tag']) -> 'Tag':
        """Add child tags ~ `add_childs` method."""
        self.add_childs(*childs)
        return self
    
    def __repr__(self) -> str:
        attrs: str = ""
        for key, value in self.attributes:
            attrs = f'{attrs} {key}="{self.stringifier(value)}"'
        childs: str = ""
        for child in self.childs:
            if len(childs) == 0:
                childs = "\n"
            child_str = str(child).replace("\n", "\n\t")
            childs = f"{childs}\t{child_str}\n"
        term1: str = " /" if len(childs) == 0 else ""
        term2: str = f"</{self.tagname}>" if len(term1) == 0 else ""
        return f"<{self.tagname}{attrs}{term1}>{childs}{term2}"
