
class Item:
    """
    Any enumerable object that can exist. Basic items have no recipe.
    e.g.: Water, Oil, Alien Artifacts
    """
    pass


class Mineral(Item):
    """
    Items that are mined.
    e.g.: Iron Ore, Coal
    """
    pass


class Manufactured(Item):
    """
    Items that have to be made from other items.
    e.g.: nearly everything
    """
    pass
