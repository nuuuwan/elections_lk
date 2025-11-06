import matplotlib.pyplot as plt
import os
from elections_lk import ElectionParliamentary


if __name__ == "__main__":
    years = []
    rejected_rates = []
    for election in ElectionParliamentary.list_all():
        if election.year == "2000":
            continue
        years.append(int(election.year))
        vote_summary = election.lk_result.vote_summary
        rejected_rates.append(vote_summary.p_rejected)

    plt.bar(years, rejected_rates, color='r')
    plt.title("Rejected Votes in Sri Lankan Parliamentary Elections")
    plt.xlabel("Election Year")
    plt.ylabel("Rejected Votes (%)")
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:.1%}")
    )
    plt.savefig(os.path.join(os.path.dirname(__file__), "rejected_votes.png"))

    