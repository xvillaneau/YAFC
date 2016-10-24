
import unittest
from yafc.loader import GameSet

from yafc.item import Mineral, Manufactured, Item
from yafc.machine import Assembler


BASIC_YAML = """
Item1:
  type: null
"""


class TestLoader(unittest.TestCase):

    def test_load_str(self):
        # Test reading YAML String
        gs = GameSet(BASIC_YAML)
        self.assertEqual(1, len(gs.items))
        self.assertIn("Item1", gs.items)

    def test_non_yaml_fail(self):
        with self.assertRaises(ValueError):
            GameSet("""
            nonsense:
              - Inconsistent: data
              Some: more
            """)

    def test_non_dict_fail(self):
        with self.assertRaises(ValueError):
            GameSet("""
            - Item1
            - Item2
            """)

        with self.assertRaises(ValueError):
            GameSet("I am a Scalar!")

    def test_load_mineral(self):
        gs = GameSet("""
        Mineral:
          type: mining
          hardness: 0.9
          mining time: 2.0
        """)
        self.assertIn("Mineral", gs.items)
        mineral = gs.items.get("Mineral")
        self.assertIsInstance(mineral, Mineral)
        self.assertEqual(0.9, mineral.hardness)
        self.assertEqual(2.0, mineral.time)

    def test_load_manufactured(self):
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
        self.assertIsInstance(item, Manufactured)
        self.assertEqual(0.5, item.time)
        self.assertEqual(2.0, item.produced)
        self.assertIn(mineral, item.ingredients)

    def test_load_machine(self):
        gs = GameSet("""
        Machine:
          type: null
          machine:
            type: assembling
            speed: 1.25
        """)
        machine = gs.machines.get("Machine")
        self.assertIsInstance(machine, Assembler)
        self.assertEqual("Machine", machine.item.name)
        self.assertEqual(1.25, machine.speed)
