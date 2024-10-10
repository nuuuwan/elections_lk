from elections_lk import ElectionParliamentary


def main():
    elections = ElectionParliamentary.list_all()[-1:]
    for election in elections:
        print(
            election.year,
            election.winning_party_id,
            election.cum_party_to_seats,
        )


if __name__ == "__main__":
    main()
