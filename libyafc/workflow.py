from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Dict, List, Set

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
    from_node: int
    to_node: int

    def __repr__(self):
        return f"Flow({self.ingredient}, {self.from_node} -> {self.to_node})"


class Workflow:
    def __init__(self):
        self.nodes: List[WorkflowNode] = []
        self.flows_to: List[List[ResourceFlow]] = []
        self.flows_from: List[List[ResourceFlow]] = []
        self._free_input: Dict[int, Set[Ingredient]] = defaultdict(set)
        self._free_output: Dict[int, Set[Ingredient]] = defaultdict(set)

    def __len__(self):
        return len(self.nodes)

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

    def add_node(self, node: WorkflowNode) -> int:
        node_id = len(self)
        self.nodes.append(node)
        self.flows_from.append([])
        self.flows_to.append([])
        self._free_input[node_id] = set(node.input)
        self._free_output[node_id] = set(node.output)
        return node_id

    def link(self, ingredient: Ingredient, from_node: int, to_node: int):
        try:
            _from = self.nodes[from_node]
            _to = self.nodes[to_node]
        except (LookupError, TypeError):
            raise ValueError("Invalid indices")
        if ingredient not in _from.output:
            raise ValueError(f"{ingredient} not in output of {_from}")
        if ingredient not in _to.input:
            raise ValueError(f"{ingredient} not in input of {_to}")

        flow = ResourceFlow(ingredient, from_node, to_node)
        self.flows_from[from_node].append(flow)
        self.flows_to[to_node].append(flow)
        self._free_output[from_node].discard(ingredient)
        self._free_input[to_node].discard(ingredient)

    def downstream_of(self, node: int, ingredient: Ingredient = None):
        return [
            flow.to_node
            for flow in self.flows_from[node]
            if ingredient is None or flow.ingredient == ingredient
        ]

    def upstream_of(self, node: int, ingredient: Ingredient = None):
        return [
            flow.from_node
            for flow in self.flows_to[node]
            if ingredient is None or flow.ingredient == ingredient
        ]
