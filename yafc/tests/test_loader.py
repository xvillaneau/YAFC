
import unittest
from yafc.loader import GameSet

from yafc.item import Mineral


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
