import unittest

from elections_lk import ElectionPresidential


class TestElectionGIGData(unittest.TestCase):
    TEST_ELECTION = ElectionPresidential('2019')

    def test_gig_table_name(self):
        self.assertEqual(
            self.TEST_ELECTION.gig_table.table_id,
            'government-elections-presidential.regions-ec.2019',
        )

    def test_pd_results(self):
        pd_results = self.TEST_ELECTION.pd_results
        self.assertEqual(len(pd_results), 160)

        first_pd_result = pd_results[0]
        self.assertEqual(first_pd_result.id, 'EC-01A')

        vote_summary = first_pd_result.vote_summary
        self.assertEqual(vote_summary.electors, 93_705)
        self.assertEqual(vote_summary.polled, 73_998)
        self.assertEqual(vote_summary.valid, 72_643)
        self.assertEqual(vote_summary.rejected, 1_355)

        self.assertAlmostEqual(vote_summary.p_turnout, 0.7897, places=4)
        self.assertAlmostEqual(vote_summary.p_valid, 0.9817, places=4)
        self.assertAlmostEqual(vote_summary.p_rejected, 0.0183, places=4)

        party_to_votes = first_pd_result.party_to_votes
        self.assertEqual(len(party_to_votes.idx), 35)
        self.assertEqual(party_to_votes.total, 72_643)
        self.assertEqual(party_to_votes.SLPP, 16_986)
        self.assertAlmostEqual(party_to_votes.get_p('SLPP'), 0.2338, places=4)
