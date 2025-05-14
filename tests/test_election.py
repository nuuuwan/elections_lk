import unittest

from elections_lk import (ElectionLocalGovernment, ElectionParliamentary,
                          ElectionPresidential, PartyToVotes, VoteSummary)


class TestCase(unittest.TestCase):

    def test_elections(self):
        for election, expected_vote_summary in [
            [
                ElectionPresidential("2024"),
                VoteSummary(
                    electors=17140354,
                    polled=13619916,
                    valid=13319616,
                    rejected=300300,
                ),
            ],
            [
                ElectionLocalGovernment("2025"),
                VoteSummary(
                    electors=17156338,
                    polled=10616087,
                    valid=10410810,
                    rejected=205277,
                ),
            ],
        ]:

            self.assertEqual(
                election.lk_result.vote_summary,
                expected_vote_summary,
            )

    def test_parliamentary(self):
        election = ElectionParliamentary("2024")

        self.assertEqual(
            election.lk_result.vote_summary,
            VoteSummary(
                electors=17140354,
                polled=11815246,
                valid=11148006,
                rejected=667240,
            ),
        )

        self.assertEqual(
            election.cum_party_to_seats,
            PartyToVotes(
                idx={
                    "NPP": 159,
                    "SJB": 40,
                    "ITAK": 8,
                    "NDF": 5,
                    "SLPP": 3,
                    "SLMC": 3,
                    "SB": 1,
                    "UNP": 1,
                    "DTNA": 1,
                    "ACTC": 1,
                    "ACMC": 1,
                    "IND17-10": 1,
                    "SLLP": 1,
                }
            ),
        )
