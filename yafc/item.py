
from numbers import Real


class Item:
    """
    Any enumerable object that can exist. Basic items have no recipe.
    e.g.: Water, Oil, Alien Artifacts
    """

    machine_cls = None

    def __init__(self, name):
        """
        Constructor for basic items

        :param name: Unique name of the item
        :type name: str
        """
        self.name = name

    def __repr__(self):
        return self.name  # pragma: no cover


class Mineral(Item):
    """
    Items that are mined.
    e.g.: Iron Ore, Coal
    """

    machine_cls = "mining"

    def __init__(self, name, time, hardness):
        """
        Constructor for mined items

        :param name: Unique name of the item
        :type name: str

        :param time: Mining time for this mineral
        :type time: Real

        :param hardness: Mining hardness for this mineral
        :type hardness: Real
        """
        super().__init__(name)
        self.time = time
        self.hardness = hardness


class Manufactured(Item):
    """
    Items that have to be made from other items.
    e.g.: nearly everything
    """

    def __init__(self, name, ingredients, time, machine_cls, produced=1):
        """
        Constructor for manufactured items

        :param name: Unique name of the item
        :type name: str

        :param ingredients: Map from required ingredients to their amount
        :type ingredients: dict[Item, Real]

        :param time: Base time for completion of this recipe
        :type time: Real

        :param machine_cls: Class of Machine that this recipe requires
        :type machine_cls: str

        :param produced: Amount of the item produced by the recipe
        :type produced: Real
        """
        super().__init__(name)
        self.ingredients = ingredients
        self.time = time
        self.machine_cls = machine_cls
        self.produced = produced
