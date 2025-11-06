import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from gig import Ent, EntType
from utils import Log

from elections_lk import ElectionParliamentary

log = Log(os.path.basename(os.path.dirname(__file__)))


def plot_bars(x_label, x_items, p_rejected):

    mean_p_rejected = np.mean(p_rejected)
    std_p_rejected = np.std(p_rejected)
    dist = stats.norm(loc=mean_p_rejected, scale=std_p_rejected)
    ci_lower, ci_upper = dist.interval(0.95)

    plt.figure(figsize=(16, 9))
    plt.bar(x_items, p_rejected, color="r")
    plt.axhline(y=mean_p_rejected, color="grey", linestyle="--", label="Mean")
    plt.axhline(
        y=ci_lower,
        color="blue",
        linestyle=":",
        label="95% CI Lower",
    )
    plt.axhline(
        y=ci_upper,
        color="red",
        linestyle=":",
        label="95% CI Upper",
    )
    plt.title(
        "Rejected Votes in Sri Lankan Parliamentary Elections (1989 - 2024)"
    )
    plt.xlabel(x_label)
    plt.ylabel("Rejected Votes (%)")
    plt.xticks(rotation=90)
    plt.legend()
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:.1%}")
    )

    image_path = os.path.join(
        os.path.dirname(__file__), f"By-{x_label.replace(' ', '-')}.png"
    )
    plt.savefig(image_path)
    log.info(f"Wrote {image_path}")


def q1(elections):
    # Q1: Were rejected votes higher in some elections?
    years = []
    p_rejected = []
    for election in elections:
        years.append(int(election.year))
        vote_summary = election.lk_result.vote_summary
        p_rejected.append(vote_summary.p_rejected)

    plot_bars(
        "Election Year",
        years,
        p_rejected,
    )


def q2(elections, ent_type):
    # Q2: Were rejected votes significantly higher in particular polling divisions?
    ents = Ent.list_from_type(ent_type)

    p_rejected_for_ents = []
    ent_names = [ent.name for ent in ents]
    for ent in ents:
        p_sum_polled = 0
        p_sum_rejected = 0
        for election in elections:
            vote_summary = election.get_result_for_id(ent.id).vote_summary
            p_sum_polled += vote_summary.polled
            p_sum_rejected += vote_summary.rejected
        mean_p_rejected_for_ent = p_sum_rejected / p_sum_polled
        p_rejected_for_ents.append(mean_p_rejected_for_ent)

    plot_bars(ent_type.name.title(), ent_names, p_rejected_for_ents)


if __name__ == "__main__":
    elections = [
        election
        for election in ElectionParliamentary.list_all()
        if election.year != "2000"
    ]
    q1(elections)
    q2(elections, EntType.DISTRICT)
    q2(elections, EntType.PD)
