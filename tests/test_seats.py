import unittest

from elections_lk import IntDict, PartyToVotes, Seats


class TestCase(unittest.TestCase):
    def test_get_party_to_seats(self):
        for region_id, n_seats, party_to_votes, expected_party_to_seats in [
            [
                "LK-11",
                18,
                PartyToVotes(
                    idx={
                        "A": 788_636,
                        "B": 208_249,
                    }
                ),
                IntDict({"A": 14, "B": 4}),
            ],
        ]:
            self.assertEqual(
                Seats.get_party_to_seats(
                    region_id, n_seats, party_to_votes
                ).idx,
                expected_party_to_seats.idx,
            )
