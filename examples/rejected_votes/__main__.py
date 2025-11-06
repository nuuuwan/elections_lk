import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from gig import Ent, EntType
from utils import Log

from elections_lk import ElectionParliamentary

log = Log(os.path.basename(os.path.dirname(__file__)))


def get_color(q, alpha=None):
    alpha = alpha or (1 if q >= 1 else 0.2)
    return (q, q if q < 0.5 else 1 - q, 1 - q, alpha)


def plot_bars(elections, x_label, x_items, p_rejected):
    n_x = len(x_items)
    if n_x == 1:
        return
    mean_p_rejected = np.mean(p_rejected)
    std_p_rejected = np.std(p_rejected)
    dist = stats.norm(loc=mean_p_rejected, scale=std_p_rejected)
    ci_lower, ci_upper = dist.interval(0.95)

    width = 8
    height = width
    plt.figure(figsize=(width, height * max(1, n_x / 100)))

    # Create horizontal lollipop chart
    y_positions = range(len(x_items))

    # Color each lollipop based on whether it exceeds ci_upper
    for i, (x_item, p_rej, y_pos) in enumerate(
        zip(x_items, p_rejected, y_positions)
    ):
        q = (p_rej - ci_lower) / (ci_upper - ci_lower)
        q = min(max(q, 0), 1)
        color = get_color(q)

        font_size = min(8, 1000 / n_x)
        plt.plot(p_rej, y_pos, "o", color=color, markersize=font_size)
        plt.annotate(
            f"{x_item} ({p_rej:.1%})",
            xy=(p_rej, i),
            xytext=(6, -1),
            textcoords="offset points",
            va="center",
            fontsize=font_size,
            color=color,
        )

    for [p, q] in zip([ci_lower, mean_p_rejected, ci_upper], [0, 0.5, 1]):
        color = get_color(q, 1)
        plt.axvline(x=p, color=color, linestyle="--", alpha=0.25)
        plt.text(
            p,
            n_x - 1,
            f"{p:.1%}",
            color=color,
            fontsize=9,
            ha="center",
            va="bottom",
        )

    election_years = [election.year for election in elections]
    min_election_year = min(election_years)
    max_election_year = max(election_years)
    elections_label = (
        f"({min_election_year} - {max_election_year})"
        if min_election_year != max_election_year
        else f"({min_election_year})"
    )

    plt.title(
        "Rejected Votes"
        + f" in Sri Lankan Parliamentary Elections {elections_label}"
    )
    plt.xlabel("Rejected Votes (%)")
    plt.yticks([])

    K = (ci_upper - ci_lower) / 2
    plt.xlim(ci_lower - K, ci_upper + K)

    plt.legend()
    plt.gca().xaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:.0%}")
    )

    chart_id = f"{x_label.replace(' ', '-')}-"
    if min_election_year == max_election_year:
        chart_id += f"{min_election_year}"
    else:
        chart_id += f"{min_election_year}-{max_election_year}"
    image_path = os.path.join(
        os.path.dirname(__file__),
        f"By-{chart_id}.png",
    )
    plt.savefig(image_path, dpi=300)
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
