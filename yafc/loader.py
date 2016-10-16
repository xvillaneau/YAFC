
import yaml
from .item import Item, Mineral, Manufactured
from .machine import Assembler, ChemicalPlant, Furnace, Miner

ITEM_MACHINE_CLS = {
    "manufactured": Assembler,
    "chemical": ChemicalPlant,
    "smelted": Furnace
}

MACHINE_CLS = {
    "assembly": Assembler,
    "chemistry": ChemicalPlant,
    "furnace": Furnace,
    "mining": Miner
}


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
        item_type = props.get('type', 'manufactured')

        if item_type == 'basic':
            obj = Item(name)

        elif item_type == 'mineral':
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
                ITEM_MACHINE_CLS[item_type],
                props.get('produced', 1)
            )

        if props.get('machine'):
            self._load_machine(obj, props['machine'])

        self.items[name] = obj

    def _load_machine(self, item, props):
        speed = props['speed']
        machine_type = props['type']

        if machine_type == 'assembly':
            obj = Assembler(item, speed, props['inputs'])
        elif machine_type == 'mining':
            obj = Miner(item, speed, props['power'])
        elif machine_type == 'chemistry':
            obj = ChemicalPlant(item, speed)
        elif machine_type == 'furnace':
            obj = Furnace(item, speed)
        else:
            raise ValueError(
                "Unrecognized machine type {}".format(machine_type))

        self.machines[item.name] = obj
