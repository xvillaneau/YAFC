
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


class Assembler(Machine):
    """
    Assembling machines.
    """

    name = "assembling"

    def __init__(self, item, speed, inputs):
        super().__init__(item)
        self.speed = speed
        self.inputs = inputs

    @classmethod
    def serialize(cls, item, serial_data):
        return cls(item, serial_data['speed'], serial_data['inputs'])


class Furnace(Machine):
    """
    Furnaces.
    """

    name = "smelting"

    def __init__(self, item, speed):
        super().__init__(item)
        self.speed = speed

    @classmethod
    def serialize(cls, item, serial_data):
        return cls(item, serial_data['speed'])


class ChemicalPlant(Machine):
    """
    Chemical Plants.
    """

    name = "chemistry"

    def __init__(self, item, speed):
        super().__init__(item)
        self.speed = speed

    @classmethod
    def serialize(cls, item, serial_data):
        return cls(item, serial_data['speed'])
