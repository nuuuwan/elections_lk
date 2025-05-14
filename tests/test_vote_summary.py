import unittest

from elections_lk import VoteSummary


class TestCase(unittest.TestCase):
    def test_vote_summary(self):
        vote_summary = VoteSummary(
            electors=100,
            polled=70,
            valid=63,
            rejected=7,
        )
        self.assertEqual(vote_summary.electors, 100)
        self.assertEqual(vote_summary.polled, 70)
        self.assertEqual(vote_summary.valid, 63)
        self.assertEqual(vote_summary.rejected, 7)

        self.assertAlmostEqual(vote_summary.p_turnout, 0.7)
        self.assertAlmostEqual(vote_summary.p_valid, 0.9)
        self.assertAlmostEqual(vote_summary.p_rejected, 0.1)
