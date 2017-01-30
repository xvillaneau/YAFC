
import pytest
from yafc.loader import GameSet

from yafc.item import Mineral, Manufactured
from yafc.machine import Assembler


BASIC_YAML = """
Item1:
  type: null
"""


def test_load_str():
        # Test reading YAML String
        gs = GameSet(BASIC_YAML)
        assert len(gs.items) == 1
        assert "Item1" in gs.items


def test_non_yaml_fail():
    with pytest.raises(ValueError):
        GameSet("""
        nonsense:
          - Inconsistent: data
          Some: more
        """)


def test_non_dict_fail():
    with pytest.raises(ValueError):
        GameSet("""
        - Item1
        - Item2
        """)

    with pytest.raises(ValueError):
        GameSet("I am a Scalar!")


def test_load_mineral():
    gs = GameSet("""
    Mineral:
      type: mining
      hardness: 0.9
      mining time: 2.0
    """)
    assert "Mineral" in gs.items
    mineral = gs.items.get("Mineral")
    assert isinstance(mineral, Mineral)
    assert mineral.hardness == 0.9
    assert mineral.time == 2.0


def test_load_manufactured():
    gs = GameSet("""
    Mineral:
      type: mining
      hardness: 0.9
      mining time: 2.0
    Item:
      ingredients:
        Mineral: 2
        Item 2: 1
      time: 0.5
      produced: 2
    Item 2:
      type: null
    """)
    item = gs.items.get("Item")
    mineral = gs.items.get("Mineral")
    assert isinstance(item, Manufactured)
    assert item.time == 0.5
    assert item.produced == 2.0
    assert mineral in item.ingredients


def test_load_machine():
    gs = GameSet("""
    Machine:
      type: null
      machine:
        type: assembling
        speed: 1.25
    """)
    machine = gs.machines.get("Machine")
    assert isinstance(machine, Assembler)
    assert machine.item.name == "Machine"
    assert machine.speed == 1.25


def test_vanilla():
    gs = GameSet.vanilla()
    assert isinstance(gs, GameSet)
