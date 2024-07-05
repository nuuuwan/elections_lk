import os
import random
from functools import cached_property

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from utils import Log

from elections_lk.analysis.ProjectionModel import ProjectionModel
from elections_lk.core import Party

log = Log('ProjectionSeries')
SEED = random.randint(1000, 9999)
log.debug(f'{SEED=}')
random.seed(SEED)


class ProjectionSeries:
    MIN_M = 40

    def __init__(self, train_elections, test_elections):
        self.train_elections = train_elections
        self.test_elections = test_elections

    @cached_property
    def test_election(self):
        assert len(self.test_elections) == 1

        return self.test_elections[0]

    def build(self):
        pd_ids = self.test_election.pd_ids
        random.shuffle(pd_ids)

        y_pd_ids = ['LK']
        n = len(pd_ids)
        Y_test_hat_list = []
        error_list = []
        for i in range(self.MIN_M, n):
            x_pd_ids = pd_ids[:i]

            model = ProjectionModel(
                self.train_elections, self.test_elections, x_pd_ids, y_pd_ids
            )
            model.train()
            Y_test_hat = model.model.predict(model.X_test)
            Y_test_hat_list.append(list(Y_test_hat))

            errors = ProjectionModel.get_errors(
                model.model, model.X_test, model.Y_test
            )
            error = errors['p90']
            error_list.append(error)

        self.plot(Y_test_hat_list, error_list)
        return Y_test_hat_list

    def plot(self, y_test_hat_list, errors):
        n = len(y_test_hat_list)
        m = len(y_test_hat_list[0])
        x = list(range(self.MIN_M, n + self.MIN_M))

        parties = (
            self.test_election.country_result.party_to_votes.get_parties(0.01)
        )

        plt.close()
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

        for i in range(m):
            party = Party.from_code(parties[i])

            y, y_min, y_max = [], [], []
            for j in range(n):
                yi = y_test_hat_list[j][i][0]
                error_i = errors[j]
                y_min.append(max(min(yi - error_i, 1), 0))
                y_max.append(max(min(yi + error_i, 1), 0))
                y.append(max(min(yi, 1), 0))

            plt.plot(x, y, label=party.code, color=party.color)
            plt.fill_between(x, y_min, y_max, color=party.color, alpha=0.1)

        ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=1)

        plt.legend()
        title = self.test_election.title
        plt.title(title)
        fig.set_size_inches(8, 4.5)

        image_path = os.path.join(
            'images', f'projection-series-{self.test_election.year}.png'
        )
        plt.savefig(image_path)
        log.info(f'📊 Saved {image_path}')
