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
    MIN_M = 20

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

        n = len(pd_ids)
        outer = []

        for i in range(self.MIN_M, n):
            x_pd_ids = pd_ids[:i]

            x_valid = 0
            x_electors = 0
            for pd_id in x_pd_ids:
                vote_summary = self.test_election.get_result(pd_id).vote_summary
                x_valid += vote_summary.valid
                x_electors += vote_summary.electors
            p_valid2 = x_valid / x_electors

            total_electors = self.test_election.country_result.vote_summary.electors
            not_x_electors = total_electors - x_electors
            not_x_valid = not_x_electors * p_valid2
            total_valid = x_valid + not_x_valid

            model = ProjectionModel(
                self.train_elections, self.test_elections, x_pd_ids, 
            )
            model.train()
            X_test = model.X_test
            Y_test_hat = model.model.predict(X_test)
            errors = ProjectionModel.get_errors(
                model.model, model.X_test, model.Y_test
            )
            error = errors['p95']

            inner = []
            for x, y in zip(X_test, Y_test_hat):
                y = max(min(y[0], 1), 0)
                y_min = max(min(y - error, 1), 0)
                y_max = max(min(y + error, 1), 0)

                x = x[0]

                z = (x * x_valid + y * not_x_valid) / total_valid
                z_min = (x * x_valid + y_min * not_x_valid) / total_valid
                z_max = (x * x_valid + y_max * not_x_valid) / total_valid
                inner.append([z, z_min, z_max])
            outer.append(inner)
                    
        self.plot(outer)
        return outer

    def plot(self, outer):
        n = len(outer)
        m = len(outer[0])
        x = list(range(self.MIN_M, n + self.MIN_M))

        parties = (
            self.test_election.country_result.party_to_votes.get_parties(0.01)
        )

        plt.close()
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

        for i in range(m):
            party = Party.from_code(parties[i])
            y = [inner[i][0] for inner in outer]
            y_min = [inner[i][1] for inner in outer]
            y_max = [inner[i][2] for inner in outer]
            
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
