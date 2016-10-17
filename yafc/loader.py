
import yaml
from inspect import isclass

from yafc import machine
from .item import Item, Mineral, Manufactured


def _machine_cls():
    """
    Get the Machine subclasses in yafc.machine and map them by their name
    :rtype: dict[str, machine.Machine]
    """
    return dict(
        (cls.name, cls) for _, cls in machine.__dict__.items()
        if cls is not machine.Machine if isclass(cls)
        if issubclass(cls, machine.Machine)
    )

MACHINE_CLS = _machine_cls()


class GameSet:
    """
    Represents a Factorio Game environment.
    At this stage, this is just the list of items and machines in the game.
    """

    def __init__(self, yaml_stream):

        self.machines = {}
        self.items = {}
        """:type : dict[str, Item]"""

        game_set_dict = yaml.load(yaml_stream)

        while game_set_dict:
            item_name = next(k for k in game_set_dict.keys())
            self._load_item(item_name, game_set_dict)

    def _load_item(self, name, gs_dict):
        props = gs_dict.pop(name)
        item_type = props.get('type', 'assembling')

        if item_type is None:
            obj = Item(name)

        elif item_type == 'mining':
            obj = Mineral(name, props['mining time'], props['hardness'])

        else:
            # Otherwise: Manufactured item
            ingredients = {}
            for i_name, i_qty in props['ingredients'].items():

                if i_name not in self.items:
                    # Recursively load ingredient if not loaded yet
                    self._load_item(i_name, gs_dict)
                ingredients[self.items[i_name]] = i_qty

            obj = Manufactured(
                name, ingredients, props['time'],
                MACHINE_CLS[item_type],
                props.get('produced', 1)
            )

        if props.get('machine'):
            self._load_machine(obj, props['machine'])

        self.items[name] = obj

    def _load_machine(self, item, props):
        machine_type = props['type']
        obj = MACHINE_CLS[machine_type].serialize(item, props)
        self.machines[item.name] = obj
