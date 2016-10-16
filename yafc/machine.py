
class Machine:
    """
    Class for machines that can be used for
    transforming and/or producing other items.

    Note: Machines are also Items, but that's separate
    """

    def __init__(self, item):
        self.item = item


class Miner(Machine):
    """
    Mining machines.
    """

    def __init__(self, item, speed, power):
        super().__init__(item)
        self.speed = speed
        self.power = power


class Assembler(Machine):
    """
    Assembling machines.
    """

    def __init__(self, item, speed, inputs):
        super().__init__(item)
        self.speed = speed
        self.inputs = inputs


class Furnace(Machine):
    """
    Furnaces.
    """

    def __init__(self, item, speed):
        super().__init__(item)
        self.speed = speed


class ChemicalPlant(Machine):
    """
    Chemical Plants.
    """

    def __init__(self, item, speed):
        super().__init__(item)
        self.speed = speed
