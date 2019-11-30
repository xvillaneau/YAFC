from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List


@dataclass(frozen=True)
class Ingredient:
    # This makes ingredients case-insensitive, hashable, and nicely formatted
    # Quite a lot of effort just to wrap a str. Totally over-engineered.
    name: str

    def __init__(self, name: str):
        # Because the class is "frozen", work around it with this:
        object.__setattr__(self, "name", name.casefold())

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return f"{type(self).__name__}({str(self)!r})"


@dataclass
class Recipe:
    input: Dict[Ingredient, int]
    output: Dict[Ingredient, int]
    time: Decimal
    name: str = ""

    @property
    def auto_name(self):
        if self.name:
            return self.name
        return ", ".join(map(str, self.output))

    def __repr__(self):
        return f"Recipe({self.auto_name})"


@dataclass
class Definitions:
    recipes: List[Recipe]
