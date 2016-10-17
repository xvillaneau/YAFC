
from .item import Mineral
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
        return self.item.name

    @classmethod
    def serialize(cls, item, serial_data):
        raise NotImplementedError

    def how_many(self, item, qty):
        raise NotImplementedError


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

    def how_many(self, item, qty):
        """
        :param item: Mineral to be mined
        :type item: Mineral
        :param qty: Flow in units/minute to be mined
        :type qty: float
        :return: How many miners are necessary
        :rtype: int
        """
        if item.machine_cls != self.name:
            raise ValueError("Item and machine types do not match!")
        if item.hardness >= self.power:
            raise ValueError("{} is not powerful enough to mine {}"
                             .format(self.item.name, item.name))

        unit_rate = (self.power - item.hardness) * self.speed * 60 / item.time
        return ceil(qty / unit_rate)


class BaseManufacture(Machine):

    name = None

    def __init__(self, item, speed):
        super().__init__(item)
        self.speed = speed

    @classmethod
    def serialize(cls, item, serial_data):
        return cls(item, serial_data['speed'])

    def how_many(self, item, qty):
        """
        :param item: Mineral to be mined
        :type item: Mineral
        :param qty: Flow in units/minute to be mined
        :type qty: float
        :return: How many miners are necessary
        :rtype: int
        """
        if item.machine_cls != self.name:
            raise ValueError("Item and machine types do not match!")

        unit_rate = self.speed * 60 / item.time
        return ceil(qty / unit_rate)


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
