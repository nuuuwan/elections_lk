import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from gig import Ent, EntType
from utils import Log

from elections_lk import ElectionParliamentary

log = Log(os.path.basename(os.path.dirname(__file__)))


def plot_bars(elections, x_label, x_items, p_rejected):

    mean_p_rejected = np.mean(p_rejected)
    std_p_rejected = np.std(p_rejected)
    dist = stats.norm(loc=mean_p_rejected, scale=std_p_rejected)
    ci_lower, ci_upper = dist.interval(0.95)

    plt.figure(figsize=(16, 9))

    # Create horizontal lollipop chart
    y_positions = range(len(x_items))
    plt.hlines(y=y_positions, xmin=0, xmax=p_rejected, color="grey", alpha=0.2)
    plt.plot(p_rejected, y_positions, "o", color=(1, 0, 0, 0.8), markersize=8)

    plt.axvline(x=mean_p_rejected, color="grey", linestyle="--", label="Mean")
    plt.axvline(
        x=ci_lower,
        color="blue",
        linestyle=":",
        label="95% CI Lower",
    )
    plt.axvline(
        x=ci_upper,
        color="red",
        linestyle=":",
        label="95% CI Upper",
    )

    # Annotate bars that exceed the upper confidence interval
    for i, (x_item, p_rej) in enumerate(zip(x_items, p_rejected)):
        if p_rej > ci_upper:
            plt.annotate(
                f"{x_item}",
                xy=(p_rej, i),
                xytext=(5, 0),
                textcoords="offset points",
                va="center",
                fontsize=8,
                color="red",
            )
    election_years = [election.year for election in elections]
    min_election_year = min(election_years)
    max_election_year = max(election_years)
    elections_label = f"({min_election_year} - {max_election_year})"

    plt.title(
        "Rejected Votes"
        + f" in Sri Lankan Parliamentary Elections {elections_label}"
    )
    plt.xlabel("Rejected Votes (%)")
    plt.ylabel(x_label)
    plt.yticks(y_positions, x_items, fontsize=min(12, int(800 / len(x_items))))
    plt.legend()
    plt.gca().xaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:.1%}")
    )

    id = f"{x_label.replace(' ', '-')}-"
    if min_election_year == max_election_year:
        id += f"{min_election_year}"
    else:
        id += f"{min_election_year}-{max_election_year}"
    image_path = os.path.join(
        os.path.dirname(__file__),
        f"By-{id}.png",
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
        elections,
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

    plot_bars(elections, ent_type.name.title(), ent_names, p_rejected_for_ents)


if __name__ == "__main__":
    all_elections = [
        election
        for election in ElectionParliamentary.list_all()
        if election.year != "2000"
    ]
    elections_last_20_years = [
        election for election in all_elections if int(election.year) >= 2004
    ]
    latest_election = [all_elections[-1]]
    for elections in [all_elections, elections_last_20_years, latest_election]:
        q1(elections)
        q2(elections, EntType.DISTRICT)
        q2(elections, EntType.PD)
