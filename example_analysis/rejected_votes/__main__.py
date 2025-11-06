import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from gig import Ent, EntType
from utils import Log

from elections_lk import ElectionParliamentary

log = Log(os.path.basename(os.path.dirname(__file__)))

CONF = 0.95


def get_color(q, alpha=None):
    alpha = alpha or (1 if q >= 1 else 0.5)
    return (q, q if q < 0.5 else 1 - q, 1 - q, alpha)


def plot_bars(
    elections, parent_ent_id, ents, x_label, x_items, p_rejected, polled
):
    display_ents = [ent for ent in ents if parent_ent_id in ent.id]
    n_x = len(display_ents)
    if n_x <= 1:
        return

    mean_p_rejected = np.average(p_rejected, weights=polled)
    variance = np.average(
        (np.array(p_rejected) - mean_p_rejected) ** 2, weights=polled
    )
    std_p_rejected = np.sqrt(variance)
    dist = stats.norm(loc=mean_p_rejected, scale=std_p_rejected)
    ci_lower, ci_upper = dist.interval(CONF)

    width = 8
    height = width * 9 / 16
    plt.figure(figsize=(width, height * max(1, n_x / 100)))
    y_positions = range(len(x_items))

    font_size = min(8, 1000 / n_x)
    uppers = []

    for i, (x_item, p_rej, y_pos, ent) in enumerate(
        zip(x_items, p_rejected, y_positions, ents)
    ):
        if parent_ent_id not in ent.id:
            continue

        q = (p_rej - ci_lower) / (ci_upper - ci_lower)
        q = min(max(q, 0), 1)
        color = get_color(q)

        plt.plot(p_rej, y_pos, "o", color=color, markersize=font_size)
        plt.annotate(
            f"{p_rej:.2%} {x_item}",
            xy=(p_rej, i),
            xytext=(6, -1),
            textcoords="offset points",
            va="center",
            fontsize=font_size,
            color=color,
        )

        if q >= 1:
            uppers.append((x_item, ent.id, p_rej))

    uppers.sort(key=lambda t: t[1])
    for upper in uppers:
        print(f"- {upper[0]} ({upper[2]:.2%})")

    for [p, q, legend_label] in zip(
        [ci_upper, mean_p_rejected, ci_lower],
        [1, 0.5, 0],
        [
            f"{CONF:.0%} CI Upper",
            "Mean Reject %",
            f"{CONF:.0%} CI Lower",
        ],
    ):
        color = get_color(q, 1)
        plt.axvline(
            x=p,
            color=color,
            linestyle="--",
            alpha=0.25,
            label=f"{legend_label} ({p:.2%})",
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
    plt.xticks([])

    K = (ci_upper - ci_lower) / 3
    plt.xlim(ci_lower - K, ci_upper + K)

    # Remove outer box (spines)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.legend()
    plt.gca().xaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:.0%}")
    )

    chart_id = f"{x_label.replace(' ', '-')}-"
    if min_election_year == max_election_year:
        chart_id += f"{min_election_year}"
    else:
        chart_id += f"{min_election_year}-{max_election_year}"
    chart_id += f"-{parent_ent_id}"
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
    polled = []
    for election in elections:
        years.append(int(election.year))
        vote_summary = election.lk_result.vote_summary
        p_rejected.append(vote_summary.p_rejected)
        polled.append(vote_summary.polled)

    plot_bars(
        elections,
        "LK",
        [Ent.from_id("LK") for year in years],
        "Election Year",
        years,
        p_rejected,
        polled,
    )


from dataclasses import dataclass


@dataclass
class DummyEnt:
    id: str
    name: str


def q2(elections, parent_ent_id, ent_type):
    # Q2: Were rejected votes significantly higher
    # in particular polling divisions?
    ents = [DummyEnt(ent.id, ent.name) for ent in Ent.list_from_type(ent_type)]

    if ent_type == EntType.PD:
        for ent in Ent.list_from_type(EntType.ED):
            postal_ent = DummyEnt(ent.id + "P", f"Postal {ent.name}")
            ents.append(postal_ent)
    ents.sort(key=lambda e: e.id, reverse=True)

    p_rejected_for_ents = []
    ent_names = [ent.name for ent in ents]
    polled = []
    for ent in ents:
        p_sum_polled = 0
        p_sum_rejected = 0
        sum_polled = 0
        for election in elections:
            vote_summary = election.get_result_for_id(ent.id).vote_summary
            p_sum_polled += vote_summary.polled
            p_sum_rejected += vote_summary.rejected
            sum_polled += vote_summary.polled
        mean_p_rejected_for_ent = p_sum_rejected / p_sum_polled
        p_rejected_for_ents.append(mean_p_rejected_for_ent)
        polled.append(sum_polled)

    plot_bars(
        elections,
        parent_ent_id,
        ents,
        ent_type.name.title(),
        ent_names,
        p_rejected_for_ents,
        polled,
    )


if __name__ == "__main__":
    all_elections = [
        election
        for election in ElectionParliamentary.list_all()
        if election.year != "2000"
    ]
    for elections in [all_elections]:
        q1(elections)
        q2(elections, "EC", EntType.ED)

        for parent_ent_id in [
            "EC",
            "EC-01",
            "EC-04",
            "EC-05",
            "EC-06",
            "EC-10",
            "EC-11",
            "EC-19",
        ]:
            q2(elections, parent_ent_id, EntType.PD)
