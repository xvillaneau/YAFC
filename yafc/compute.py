
from collections import defaultdict
from numbers import Real
from .item import Item, Manufactured


def compute_flows(inputs):
    """
    Compute the entire set of operations and quantities/flows
    to get from raw ingredients to

    :param inputs: What items to produce
    :type inputs: dict[Item, Real]

    :return: Complete list of intermediate quantities
    :rtype: list[(Item, Real)]
    """

    head = defaultdict(float)
    head.update(inputs)

    prod_plan = defaultdict(float)

    while any(isinstance(i, Manufactured) for i in head):

        # Remove the next manufactured item from the
        item = next(i for i in head if isinstance(i, Manufactured))
        """:type: Manufactured"""
        qty = head.pop(item)

        prod_plan[item] += qty

        for i, q in item.ingredients.items():
            head[i] += qty * q / item.produced

    prod_plan.update(head)

    return dict(prod_plan)
