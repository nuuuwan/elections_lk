import os
import random
from functools import cached_property

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from gig import Ent
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
            model = ProjectionModel(
                self.train_elections, self.test_elections, x_pd_ids, pd_ids
            )
            model.train()
            inner = model.evaluate(model.X_test)
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
        n_results = len(self.test_election.results)
        ax.set_xlim([0, n_results])
        ax.set_ylim([0.35, 0.65])

        def get_label(xi):
            pd_ids = self.test_election.pd_ids
            pd_id = pd_ids[xi]
            pd_ent = Ent.from_id(pd_id)
            return pd_ent.name

        MIN_ABS_DY = 0.5
        for i_party in range(m):
            party = Party.from_code(parties[i_party])
            y = [inner[i_party][0] for inner in outer]
            y_min = [inner[i_party][1] for inner in outer]
            y_max = [inner[i_party][2] for inner in outer]

            plt.plot(x, y, label=party.code, color=party.color)
            plt.fill_between(x, y_min, y_max, color=party.color, alpha=0.1)

            prev_yi = None
            for xi, yi in zip(x, y):
                if prev_yi is not None:
                    dy = yi - prev_yi
                    if abs(dy) > MIN_ABS_DY:
                        ax.text(
                            xi,
                            yi + 0.005 * (1 if dy > 0 else -1),
                            f'{dy * 100:+.1f}pp',
                            color=party.color,
                            fontsize=12,
                            ha='center',
                            va='center',
                        )
                        ax.text(
                            xi,
                            yi,
                            get_label(xi),
                            color=party.color,
                            fontsize=8,
                            ha='center',
                            va='center',
                        )

                prev_yi = yi

            n = len(y)
            x_j = None
            y_min_j = None
            has_won = False
            for minus_i_result in range(n):
                i_result = n - minus_i_result - 1
                outer_result = list(outer[i_result])
                inner_other = (
                    outer_result[:i_party] + outer_result[i_party + 1:]
                )
                y_min_j = y_min[i_result]
                x_j = x[i_result]
                other_y_maxes = [inner[2] for inner in inner_other]
                if y_min_j < max(other_y_maxes):
                    break
                has_won = True

            if has_won:
                plt.axvline(
                    x=x_j,
                    linestyle=':',
                    color=party.color,
                    label=f'{party.code} Wins 1st Prefs. ({x_j}/{n_results})',
                )

            x_j = None
            y_min_j = None
            has_won = False
            for minus_i_result in range(n):
                i_result = n - minus_i_result - 1
                outer_result = list(outer[i_result])
                inner_other = (
                    outer_result[:i_party] + outer_result[i_party + 1:]
                )
                y_min_j = y_min[i_result]
                x_j = x[i_result]
                other_y_maxes = [inner[2] for inner in inner_other]
                if y_min_j < max(other_y_maxes) or y_min_j < 0.5:
                    break
                has_won = True

            if has_won:
                plt.axvline(
                    x=x_j,
                    linestyle='--',
                    color=party.color,
                    label=f'{party.code} Wins Election ({x_j}/{n_results})',
                )

        ax.axhline(
            y=0.5,
            color='gray',
            linestyle='--',
            linewidth=1,
            label='50% (to Win)',
        )

        plt.legend()
        title = self.test_election.title
        plt.title(title)
        width = 12
        height = width * 9 / 16
        fig.set_size_inches(width, height)

        image_path = os.path.join(
            'images', f'projection-series-{self.test_election.year}.png'
        )
        plt.savefig(image_path)
        log.info(f'📊 Saved {image_path}')
