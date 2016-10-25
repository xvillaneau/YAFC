
import unittest

from yafc.machine import Machine, Miner, Assembler
from yafc.item import Item, Mineral, Manufactured


class TestMachine(unittest.TestCase):

    def setUp(self):
        self.m_item = Item("Machine")

    def test_base_machine(self):
        m = Machine(self.m_item)

        with self.assertRaises(NotImplementedError):
            m.how_many(self.m_item, 1)
        with self.assertRaises(NotImplementedError):
            m.serialize(self.m_item, {})

    def test_miner_base(self):
        m = Miner(self.m_item, 1.0, 2.0)
        self.assertEqual(1.0, m.speed)
        self.assertEqual(2.0, m.power)
        self.assertIs(self.m_item, m.item)

        m = Miner.serialize(self.m_item, dict(speed=1.0, power=2.0))
        self.assertIsInstance(m, Miner)
        self.assertEqual(1.0, m.speed)
        self.assertEqual(2.0, m.power)
        self.assertIs(self.m_item, m.item)

    def test_miner_compute(self):
        iron = Mineral("Iron Ore", 2.0, 0.9)
        stone = Mineral("Stone", 2.0, 0.4)
        toaster = Item("Toaster")
        hard_thing = Mineral("I am hard", 2.0, 5.0)

        drill = Miner(self.m_item, 0.5, 3.0)

        self.assertEqual(31.5, drill.max_production(iron))
        self.assertEqual(39.0, drill.max_production(stone))

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            drill.max_production(toaster)
        with self.assertRaises(ValueError):
            drill.max_production(hard_thing)

        self.assertEqual(1, drill.how_many(iron, 30))
        self.assertEqual(2, drill.how_many(iron, 32))

    def test_manufacture_base(self):

        m = Assembler(self.m_item, 1.25)
        self.assertIs(self.m_item, m.item)
        self.assertEqual(1.25, m.speed)

        m = Assembler.serialize(self.m_item, dict(speed=1.25))
        self.assertIsInstance(m, Assembler)
        self.assertIs(self.m_item, m.item)
        self.assertEqual(1.25, m.speed)

    def test_manufacture_compute(self):
        iron = Item("Iron Plates")
        gear = Manufactured("Iron Gear Wheel", {iron: 2}, 0.5, "assembling")
        belt = Manufactured("Transport Belt", {iron: 1, gear: 1}, 0.5,
                            "assembling", produced=2)

        machine = Assembler(self.m_item, 1.25)

        self.assertEqual(150.0, machine.max_production(gear))
        self.assertEqual(300.0, machine.max_production(belt))
