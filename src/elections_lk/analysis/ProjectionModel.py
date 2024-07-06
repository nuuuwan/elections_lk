from functools import cached_property

import numpy as np
from sklearn.linear_model import LinearRegression
from utils import Log

from elections_lk.core import Election

log = Log('ProjectionModel')


class ProjectionModel:
    MIN_P_VOTES = 0.1

    def __init__(
        self,
        train_elections: list[Election],
        test_elections: list[Election],
        x_pd_ids: list[str],
        y_pd_ids: list[str],

    ):
        self.train_elections = train_elections
        self.test_elections = test_elections
        self.x_pd_ids = x_pd_ids
        self.y_pd_ids = y_pd_ids

        self.model = None

    @staticmethod
    def get_z(elections, z_pd_ids: list[str]) -> np.ndarray:
        z = []
        for election in elections:
            parties = election.country_result.party_to_votes.get_parties(
                ProjectionModel.MIN_P_VOTES
            )

            total_votes = 0
            for pd_id in z_pd_ids:
                pd_result = election.get_result(pd_id)
                total_votes += pd_result.vote_summary.valid

            for party in parties:
                total_votes_for_party = 0
                for pd_id in z_pd_ids:
                    pd_result = election.get_result(pd_id)
                    total_votes_for_party += (
                        pd_result.party_to_votes.dict.get(party, 0)
                    )
                zi = total_votes_for_party / total_votes
                z.append(zi)
        return np.array(z, dtype=np.float64).reshape(len(z), 1)
    


    @cached_property
    def X_train(self) -> np.ndarray:
        return self.get_z(self.train_elections, self.x_pd_ids)

    @cached_property
    def Y_train(self) -> np.ndarray:
        return self.get_z(self.train_elections, self.y_pd_ids)

    @cached_property
    def X_test(self) -> np.ndarray:
        return self.get_z(self.test_elections, self.x_pd_ids)

    @cached_property
    def Y_test(self) -> np.ndarray:
        return self.get_z(self.test_elections, self.y_pd_ids)

    @cached_property
    def m_x(self) -> int:
        return len(self.x_pd_ids)

    @cached_property
    def m_y(self) -> int:
        return len(self.y_pd_ids)

    @cached_property
    def n_train(self) -> int:
        return len(self.X_train)

    @cached_property
    def n_test(self) -> int:
        return len(self.X_test)

    def __str__(self):
        return (
            'ProjectionModel('
            + f'n_train={self.n_train}, n_test={self.n_test}, '
            + f'm_x={self.m_x}, m_y={self.m_y})'
        )

    def train(self) -> LinearRegression:
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.Y_train)
        return self.model

    @staticmethod
    def get_errors(model, X, Y) -> float:
        Y_hat = model.predict(X)
        Error = Y_hat - Y
        p90 = np.percentile(np.abs(Error), 90)
        p95 = np.percentile(np.abs(Error), 95)

        mse = np.sqrt(np.mean((Error) ** 2))
        return dict(
            mse=mse,
            p90=p90,
            p95=p95,
        )
