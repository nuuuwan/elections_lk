import unittest

from elections_lk import (ElectionLocalGovernment, ElectionParliamentary,
                          ElectionPresidential)


class TestCase(unittest.TestCase):
    @unittest.skip("")
    def test_elections(self):
        for election in [
            ElectionPresidential("2024"),
            ElectionParliamentary("2024"),
            ElectionLocalGovernment("2025"),
        ]:
            print(election.lk_result)

    def test_parliamentary(self):
        election = ElectionParliamentary("2024")
        lk_result = election.lk_result
        print(lk_result.vote_summary)
        print(lk_result.party_to_votes)
        print(election.region_to_seats)
        print(election.region_to_party_to_seats)
        print(election.cum_party_to_seats)
