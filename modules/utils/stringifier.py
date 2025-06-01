from typing import Any, Callable
from copy import deepcopy

__all__ = ["Stringifier", "DEFAULT_RULES"]

DEFAULT_RULES: dict[type, Callable[[Any], str]] = {
    tuple: lambda x: ",".join([str(xi) for xi in x]),
    list: lambda x: ",".join([str(xi) for xi in x]),
    None: lambda _: ""
}

class Stringifier:
    """Class to correctly stringify some types."""
    def __init__(self, rules: dict[type, Callable[[Any], str]] | None = None) -> None:
        if rules is None:
            rules = deepcopy(DEFAULT_RULES)
        self._rules = rules

    def __getitem__(self, dtype: type) -> Callable[[Any], str]:
        return self._rules.get(dtype, str)
    
    def __setitem__(self, dtype: type, rule: Callable[[Any], str]) -> None:
        self._rules[dtype] = rule

    def __call__(self, element: Any) -> str:
        return self[type(element)](element)