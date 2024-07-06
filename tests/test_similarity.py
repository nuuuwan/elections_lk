import unittest

from elections_lk import Similarity


class TestSimilarity(unittest.TestCase):
    def test_year_party_list(self):
        similarity = Similarity()
        year_party_list = similarity.year_party_list
        self.assertEqual(len(year_party_list), 117)
        self.assertEqual(year_party_list[0], '1982_ACTC')

    def test_pd_id_list(self):
        similarity = Similarity()
        pd_id_list = similarity.pd_id_list
        self.assertEqual(len(pd_id_list), 187)
        self.assertEqual(pd_id_list[0], 'EC-01A')

    def test_results_matrix(self):
        similarity = Similarity()
        R = similarity.results_matrix
        self.assertEqual(R.shape, (187, 117))

        self.assertAlmostEqual(R[0, 0], 0.0112, places=4)

    def test_similarity_matrix(self):
        similarity = Similarity()
        S = similarity.similarity_matrix
        self.assertEqual(S.shape, (187, 187))

        for i in range(187):
            self.assertAlmostEqual(S[i, i], 1.0, places=4)
