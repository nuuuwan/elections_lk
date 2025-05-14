import unittest
from elections_lk import Party


class TestCase(unittest.TestCase):
    def test_party(self):
        party = Party.from_code("NPP")
        self.assertEqual(party.color, "#f00")
