import unittest
from elections_lk import ElectionPresidential


class TestElectionPresidential(unittest.TestCase):
    def test_list_all(self):
        elections = ElectionPresidential.list_all()
        self.assertEqual(len(elections), 8)
        first_election = elections[0]
        self.assertEqual(first_election.year, '1982')
        self.assertEqual(first_election.category, 'presidential')
