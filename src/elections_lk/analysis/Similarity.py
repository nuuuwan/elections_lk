from functools import cached_property

import numpy as np
from scipy.spatial.distance import cosine
from elections_lk.core import ElectionPresidential

'''
p = number of polling divisions
q = number of elections x parties
'''


class Similarity:
    @cached_property
    def year_party_list(self) -> list:
        year_party_set = set()
        for election in ElectionPresidential.list_all():
            year = election.year
            for pd_result in election.pd_results:
                for party in pd_result.party_to_votes.parties:
                    year_party_set.add(f'{year}_{party}')
        return list(sorted(year_party_set))

    @cached_property
    def pd_id_list(self) -> list:
        pd_id_set = set()
        for election in ElectionPresidential.list_all():
            for pd_result in election.pd_results:
                pd_id_set.add(pd_result.id)
        return list(sorted(pd_id_set))

    @cached_property
    def results_matrix_idx(self) -> dict:
        idx = {}

        for election in ElectionPresidential.list_all():
            year = election.year
            for pd_result in election.pd_results:
                pd_id = pd_result.id
                if pd_id not in idx:
                    idx[pd_id] = {}
                for party, p_votes in pd_result.party_to_votes.p_items():
                    year_party = f'{year}_{party}'

                    idx[pd_id][year_party] = p_votes

        return idx

    @cached_property
    def results_matrix(self) -> np.ndarray:
        idx = self.results_matrix_idx
        year_party_list = self.year_party_list
        pd_id_list = self.pd_id_list

        matrix = np.zeros((len(pd_id_list), len(year_party_list)))
        pd_idx = {pd_id: i for i, pd_id in enumerate(sorted(idx.keys()))}
        year_party_idx = {
            year_party: i for i, year_party in enumerate(year_party_list)
        }
        for pd_id in pd_id_list:
            year_party_votes = idx[pd_id]
            for year_party, p_votes in year_party_votes.items():
                matrix[pd_idx[pd_id], year_party_idx[year_party]] = p_votes

        return matrix

    @cached_property
    def similarity_matrix(self) -> np.ndarray:
        R = self.results_matrix
        p = R.shape[0]
        S = np.zeros((p, p))
        for i in range(p):
            for j in range(i, p):
                similarity = 1 - cosine(R[i, :], R[j, :])
                S[i, j] = similarity
                S[j, i] = similarity
        return S

    @cached_property
    def similarity_idx(self) -> dict:
        idx = {}
        S = self.similarity_matrix
        for i in range(160):
            for j in range(i + 1, 160):
                S_i_j = S[i, j]
                idx[(i, j)] = S_i_j
        return dict(sorted(idx.items(), key=lambda x: x[1]))
