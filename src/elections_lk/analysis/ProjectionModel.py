from functools import cache, cached_property

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

    @cache
    def get_weights(self) -> tuple[float]:
        election = self.test_elections[-1]
        election.country_result.vote_summary.electors

        x_total_electors = 0
        x_total_valid = 0
        for pd_id in self.x_pd_ids:
            pd_result = election.get_result(pd_id)
            vote_summary = pd_result.vote_summary
            x_total_electors += vote_summary.electors
            x_total_valid += vote_summary.valid

        not_x_total_electors = 0
        for pd_id in self.y_minus_x_pd_ids:
            pd_result = election.get_result(pd_id)
            not_x_total_electors += pd_result.vote_summary.electors

        x_p_turnout2 = x_total_valid / x_total_electors
        not_x_total_valid_est = not_x_total_electors * x_p_turnout2
        total_valid_est = x_total_valid + not_x_total_valid_est

        w_x = x_total_valid / total_valid_est
        w_not_x = not_x_total_valid_est / total_valid_est
        return w_x, w_not_x

    @cached_property
    def y_minus_x_pd_ids(self) -> list[str]:
        return list(set(self.y_pd_ids) - set(self.x_pd_ids))

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
                zi = []
                for pd_id in z_pd_ids:
                    pd_result = election.get_result(pd_id)
                    total_votes_for_party += (
                        pd_result.party_to_votes.dict.get(party, 0)
                    )

                    zij = pd_result.party_to_votes.p_dict.get(party, 0)
                    zi.append(zij)

                zij = total_votes_for_party / total_votes
                zi.append(zij)
                z.append(zi)
        return np.array(z)

    @cached_property
    def X_train(self) -> np.ndarray:
        return self.get_z(self.train_elections, self.x_pd_ids)

    @cached_property
    def Y_train(self) -> np.ndarray:
        return self.get_z(self.train_elections, self.y_minus_x_pd_ids)

    @cached_property
    def X_test(self) -> np.ndarray:
        return self.get_z(self.test_elections, self.x_pd_ids)

    @cached_property
    def Y_test(self) -> np.ndarray:
        return self.get_z(self.test_elections, self.y_minus_x_pd_ids)

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
        # log.debug(f'{mse=}, {p90=}, {p95=}')
        return dict(
            mse=mse,
            p90=p90,
            p95=p95,
        )

    def evaluate(self, X):
        assert self.model is not None
        Y_hat = self.model.predict(X)
        error = self.get_errors(self.model, self.X_test, self.Y_test)['p95']
        w_x, w_not_x = self.get_weights()

        Y_hat2 = []
        for i, yi in enumerate(Y_hat):
            yi = yi[-1]
            yi_min = yi - error
            yi_max = yi + error
            xi = X[i][-1]
            yi2 = xi * w_x + yi * w_not_x
            yi2_min = xi * w_x + yi_min * w_not_x
            yi2_max = xi * w_x + yi_max * w_not_x
            Y_hat2.append([yi2, yi2_min, yi2_max])

        return np.array(Y_hat2).reshape(len(Y_hat2), 3)
