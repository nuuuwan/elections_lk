from functools import cached_property

import numpy as np

from elections_lk.core import ElectionPresidential

'''
p = number of polling divisions
q = number of elections x parties
'''


class Similarity:
    @cached_property
    def results_matrix(self) -> np.ndarray:
        # p x q matrix of polling division x vote percentages for each
        # election/party combination
        idx = {}
        year_party_set = set()
        for election in ElectionPresidential.list_all():
            year = election.year
            for pd_result in election.pd_results:
                pd_id = pd_result.id
                if pd_id not in idx:
                    idx[pd_id] = {}
                for party, p_votes in pd_result.party_to_votes.p_items():
                    year_party = f'{year}_{party}'
                    year_party_set.add(year_party)
                    idx[pd_id][year_party] = p_votes

        matrix = np.zeros((len(idx), len(year_party_set)))
        pd_idx = {pd_id: i for i, pd_id in enumerate(sorted(idx.keys()))}
        year_party_idx = {
            year_party: i
            for i, year_party in enumerate(sorted(year_party_set))
        }
        for pd_id, year_party_votes in idx.items():
            for year_party, p_votes in year_party_votes.items():
                matrix[pd_idx[pd_id], year_party_idx[year_party]] = p_votes

        return matrix

    @property
    def similarity_matrix(self) -> np.ndarray:
        R = self.results_matrix
        mag_squared = np.sum(R**2, axis=1)[:, np.newaxis]
        distances_squared = mag_squared + mag_squared.T - 2 * np.dot(R, R.T)
        similarities = -distances_squared
        np.fill_diagonal(similarities, np.max(similarities))
        return similarities
