def main():
    from elections_lk import ElectionParliamentary

    for election in ElectionParliamentary.list_all():
        print("-" * 80)
        print(election.year)
        lk_result = election.get_result("LK")
        party_to_pvotes = lk_result.party_to_votes.party_to_pvotes

        nl_party_to_seats = election.region_to_party_to_seats["LK"]

        print("\t", "1 SEAT")
        for party, seats in nl_party_to_seats.items():
            if seats == 1:
                pvotes = party_to_pvotes[party]
                print("\t\t", party, f"{pvotes:.6%}")

        print("\t", "0 SEATS")
        for party, pvotes in party_to_pvotes.items():
            if pvotes < 0.005:
                continue
            seats = nl_party_to_seats.get(party, 0)
            if seats == 0:
                print("\t\t", party, f"{pvotes:.6%}")


if __name__ == "__main__":
    main()
