
from .item import Manufactured, Mineral
from math import ceil


class Machine:
    """
    Class for machines that can be used for
    transforming and/or producing other items.

    Note: Machines are also Items, but that's separate
    """

    name = None

    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return self.item.name  # pragma: no cover

    @classmethod
    def serialize(cls, item, serial_data):
        raise NotImplementedError

    def test_item(self, item):
        """
        Test if an item is valid for this machine

        :param item: Item to test
        :type item: Item
        """
        if item.machine_cls != self.name:
            raise ValueError("Item and machine types do not match!")

    def max_production(self, item):
        raise NotImplementedError

    def how_many(self, item, qty):
        """
        Compute how many mining machines are required to achieve a
        given production target.

        :param item: Item to be produced
        :type item: Item

        :param qty: Flow in units/minute to be produced
        :type qty: float

        :return: How many machines are necessary
        :rtype: int
        """
        return ceil(qty / self.max_production(item))


class Miner(Machine):
    """
    Mining machines.
    """

    name = "mining"

    def __init__(self, item, speed, power):
        super().__init__(item)
        self.speed = speed
        self.power = power

    @classmethod
    def serialize(cls, item, serial_data):
        return cls(item, serial_data['speed'], serial_data['power'])

    def max_production(self, item):
        """
        Compute the maximum rate at which the given item can be mined

        :param item: Mineral to be mined
        :type item: Mineral

        :return: Maximum production rate (items/minute)
        :rtype: float
        """

        self.test_item(item)
        if item.hardness >= self.power:
            raise ValueError("{} is not powerful enough to mine {}"
                             .format(self.item.name, item.name))

        return (self.power - item.hardness) * self.speed * 60 / item.time


class BaseManufacture(Machine):

    name = None

    def __init__(self, item, speed):
        super().__init__(item)
        self.speed = speed

    @classmethod
    def serialize(cls, item, serial_data):
        return cls(item, serial_data['speed'])

    def max_production(self, item):
        """
        Compute the maximum rate at which the given item can be made

        :param item: Item to be produced
        :type item: Manufactured

        :return: Maximum production rate (items/minute)
        :rtype: float
        """
        self.test_item(item)
        return self.speed * item.produced * 60 / item.time


class Assembler(BaseManufacture):
    """
    Assembling machines.
    """
    name = "assembling"


class Furnace(BaseManufacture):
    """
    Furnaces.
    """
    name = "smelting"


class ChemicalPlant(BaseManufacture):
    """
    Chemical Plants.
    """
    name = "chemistry"


class RocketSile(BaseManufacture):
    """
    The rocket Silo
    """
    name = "rocket"
