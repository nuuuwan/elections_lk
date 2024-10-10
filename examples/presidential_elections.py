from elections_lk import ElectionPresidential


def main():
    for election in ElectionPresidential.list_all():
        print(
            election.year,
            election.lk_result.vote_summary.polled,
            election.lk_result.vote_summary.p_turnout,
            election.lk_result.vote_summary.p_valid,
            election.lk_result.vote_summary.p_rejected,
        )


if __name__ == "__main__":
    main()
