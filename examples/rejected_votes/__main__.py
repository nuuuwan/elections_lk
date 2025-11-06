import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from utils import Log

from elections_lk import ElectionParliamentary

log = Log(os.path.basename(os.path.dirname(__file__)))


def q1():
    # Q1: Were rejected votes higher in some elections?
    years = []
    p_rejected = []
    for election in ElectionParliamentary.list_all():
        if election.year == "2000":
            continue
        years.append(int(election.year))
        vote_summary = election.lk_result.vote_summary
        p_rejected.append(vote_summary.p_rejected)

    mean_p_rejected = np.mean(p_rejected)
    std_p_rejected = np.std(p_rejected)
    dist = stats.norm(loc=mean_p_rejected, scale=std_p_rejected)
    ci_lower, ci_upper = dist.interval(0.95)

    plt.figure(figsize=(16, 9))
    plt.bar(years, p_rejected, color="r")
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
        "Rejected Votes in Sri Lankan Parliamentary Elections (1989 - 2024"
    )
    plt.xlabel("Election Year")
    plt.ylabel("Rejected Votes (%)")
    plt.legend()
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:.1%}")
    )
    image_path = os.path.join(os.path.dirname(__file__), "q1.png")
    plt.savefig(image_path)
    log.info(f"Wrote {image_path}")


if __name__ == "__main__":
    q1()
