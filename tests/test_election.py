import unittest

from elections_lk import (
    ElectionLocalGovernment,
    ElectionParliamentary,
    ElectionPresidential,
)


class TestCase(unittest.TestCase):
    def test_elections(self):
        for election in [
            ElectionPresidential("2024"),
            ElectionParliamentary("2024"),
            ElectionLocalGovernment("2025"),
        ]:
            print(election.lk_result)
