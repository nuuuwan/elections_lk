from elections_lk import ElectionLocalGovernment


def main():
    print("-" * 30)
    print("Year".ljust(5), "Turnout".rjust(10), "Rejected".rjust(10))
    for election in ElectionLocalGovernment.list_all():
        vote_summary = election.lk_result.vote_summary
        print(
            election.year.ljust(5),
            f"{vote_summary.p_turnout:.2%}".rjust(10),
            f"{vote_summary.p_rejected:.2%}".rjust(10),
        )
    print("-" * 30)


if __name__ == "__main__":
    main()
