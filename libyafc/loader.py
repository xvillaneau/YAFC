import decimal
from pathlib import Path
import re

import marshmallow as mllw
import yaml

from .models import Recipe, Definitions, Ingredient

__all__ = (
    "DEFINITIONS_DIR",
    "list_builtin_definitions",
    "load_builtin_definition",
    "parse_definition",
)

DEFINITIONS_DIR: Path = Path(__file__).parent / "definitions"


def list_builtin_definitions():
    return [path.name for path in DEFINITIONS_DIR.iterdir()]


def load_builtin_definition(name: str):
    def_path = DEFINITIONS_DIR / name
    with open(def_path) as def_file:
        return parse_definition(def_file)


def parse_definition(stream):
    data = yaml.safe_load(stream)
    schema = DefinitionsSchema()
    return schema.load(data)


RE_DURATION = re.compile(r"^([0-9.]+)\s*(s|ms|ticks?)$")
UNIT_FACTORS = {"s": 1, "ms": 1000, "tick": 60, "ticks": 60}


class DurationField(mllw.fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return f"{value}s"

    def _deserialize(self, value, attr, data, **kwargs):
        value, unit = RE_DURATION.match(value).groups()
        return decimal.Decimal(value) / UNIT_FACTORS[unit]


class IngredientField(mllw.fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return Ingredient(value)


class RecipeIOField(mllw.fields.Mapping):
    def __init__(self, **kwargs):
        super().__init__(IngredientField, mllw.fields.Integer, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            value = {value: 1}
        return super()._deserialize(value, attr, data, **kwargs)


class RecipeSchema(mllw.Schema):
    class Meta:
        unknown = "EXCLUDE"

    Time = DurationField(required=True, attribute="time")
    Input = RecipeIOField(default={}, attribute="input")
    Output = RecipeIOField(default={}, attribute="output")
    Name = mllw.fields.String(attribute="name")

    @mllw.post_load
    def make_recipe(self, data, **_):
        return Recipe(**data)


class DefinitionsSchema(mllw.Schema):
    class Meta:
        unknown = "EXCLUDE"

    Recipes = mllw.fields.Nested(RecipeSchema, many=True, attribute="recipes")

    @mllw.post_load
    def make_definitions(self, data, **_):
        return Definitions(**data)
