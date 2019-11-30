from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Dict, List

from .models import Definitions, Ingredient, Recipe


class WorkflowNode(ABC):
    @property
    @abstractmethod
    def output(self) -> List[Ingredient]:
        pass

    @property
    @abstractmethod
    def input(self) -> List[Ingredient]:
        pass


@dataclass
class ProductionUnit(WorkflowNode):
    recipe: Recipe

    @property
    def output(self) -> List[Ingredient]:
        return list(self.recipe.output)

    @property
    def input(self) -> List[Ingredient]:
        return list(self.recipe.input)


@dataclass(frozen=True)
class ResourceFlow:
    ingredient: Ingredient
    from_unit: int
    to_unit: int

    def __repr__(self):
        return f"Flow({self.ingredient}, {self.from_unit} -> {self.to_unit})"


class Workflow:
    def __init__(self):
        self.units: List[WorkflowNode] = []
        self.flows_to: List[List[ResourceFlow]] = []
        self.flows_from: List[List[ResourceFlow]] = []

    def __len__(self):
        return len(self.units)

    @classmethod
    def from_definitions(cls, definitions: Definitions, link_all=True):
        producers: Dict[Ingredient, List[int]] = defaultdict(list)
        consumers: Dict[Ingredient, List[int]] = defaultdict(list)

        workflow = cls()
        for recipe in definitions.recipes:
            unit = ProductionUnit(recipe)
            unit_id = workflow.add_node(unit)

            for _input in recipe.input:
                consumers[_input].append(unit_id)
            for _output in recipe.output:
                producers[_output].append(unit_id)

        if not link_all:
            return workflow

        for ingredient in producers.keys() & consumers.keys():
            links = product(producers[ingredient], consumers[ingredient])
            for from_unit, to_unit in links:
                workflow.link(ingredient, from_unit, to_unit)

        return workflow

    def add_node(self, unit: WorkflowNode) -> int:
        self.units.append(unit)
        self.flows_from.append([])
        self.flows_to.append([])
        return len(self) - 1

    def link(self, ingredient: Ingredient, from_unit: int, to_unit: int):
        try:
            _from = self.units[from_unit]
            _to = self.units[to_unit]
        except (LookupError, TypeError):
            raise ValueError("Invalid indices")
        if ingredient not in _from.output:
            raise ValueError(f"{ingredient} not in output of {_from}")
        if ingredient not in _to.input:
            raise ValueError(f"{ingredient} not in input of {_to}")

        flow = ResourceFlow(ingredient, from_unit, to_unit)
        self.flows_from[from_unit].append(flow)
        self.flows_to[to_unit].append(flow)

    def downstream_of(self, unit: int, ingredient: Ingredient = None):
        return [
            flow.to_unit
            for flow in self.flows_from[unit]
            if ingredient is None or flow.ingredient == ingredient
        ]

    def upstream_of(self, unit: int, ingredient: Ingredient = None):
        return [
            flow.from_unit
            for flow in self.flows_to[unit]
            if ingredient is None or flow.ingredient == ingredient
        ]
