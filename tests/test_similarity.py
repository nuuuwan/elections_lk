import unittest

from elections_lk import Similarity


class TestSimilarity(unittest.TestCase):
    def test_results_matrix(self):
        similarity = Similarity()
        R = similarity.results_matrix
        self.assertEqual(R.shape, (160, 117))

        self.assertAlmostEqual(R[0, 0], 0.0112, places=4)
