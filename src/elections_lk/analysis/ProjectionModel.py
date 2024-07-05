from functools import cached_property

import numpy as np
from sklearn.linear_model import LinearRegression
from utils import Log

from elections_lk.core import Election

log = Log('ProjectionModel')


class ProjectionModel:
    MIN_P_VOTES = 0.01

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
            for party in parties:
                zi = []
                for pd_id in z_pd_ids:
                    pd_result = election.get_result(pd_id)
                    zij = pd_result.party_to_votes.p_dict.get(party, 0)
                    zi.append(zij)
                z.append(zi)
        return np.array(z)

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

    def train(self, evaluate=True) -> LinearRegression:
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.Y_train)


        if evaluate:
            self.evaluate('train', self.model, self.X_train, self.Y_train)
            self.evaluate('test', self.model, self.X_test, self.Y_test)

        return self.model

    @staticmethod
    def evaluate(label, model, X_test, Y_test, verbose=False) -> float:
        Y_test_hat = model.predict(X_test)

        mse = np.sqrt(np.mean((Y_test - Y_test_hat) ** 2))
        if verbose:
            log.debug(f'🧪 [{label}] MSE: {mse:.6f}')
        return mse
