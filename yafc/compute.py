
from collections import defaultdict
from .item import Item, Manufactured
from .machine import Machine


def compute_flows(inputs, limits=set([])):
    """
    Compute the entire set of operations and quantities/flows
    to get from raw ingredients to

    :param inputs: What items to produce
    :type inputs: dict[Item, float]

    :return: Complete list of intermediate quantities
    :rtype: dict[Item, float]
    """

    head = defaultdict(float)
    head.update(inputs)

    prod_plan = defaultdict(float)

    while any(isinstance(i, Manufactured) for i in head
              if i.name not in limits):

        # Remove the next manufactured item from the
        item = next(i for i in head if isinstance(i, Manufactured)
                    if i.name not in limits)
        """:type: Manufactured"""
        qty = head.pop(item)

        prod_plan[item] += qty

        for i, q in item.ingredients.items():
            head[i] += qty * q / item.produced

    prod_plan.update(head)

    return dict(prod_plan)


def compute_machines(flows, machines):
    """
    From a map of manufacturing flows, compute the number of
    machines required to handle that flow.

    *Note:* Flows are assumed to be in units/minute

    :param flows: List of manufacturing operations
    :type flows: dict[Item, float]

    :param machines: List of available machines
    :type machines: dict[str, Machine]

    :return: list[(Item, Real, Machine, int)]
    """

    def compute_one(item, qty):
        """
        :type item: Item
        :type qty: float
        :rtype: (Machine, float)
        """
        if item.machine_cls is None:
            return None, 0
        machine = machines[item.machine_cls]
        return machine, machine.how_many(item, qty)

    return [(i, q) + compute_one(i, q) for i, q in flows.items()]
