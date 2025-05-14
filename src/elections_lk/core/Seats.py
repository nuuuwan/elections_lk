from elections_lk.core.result.PartyToVotes import PartyToVotes


class Seats:

    @staticmethod
    def get_party_to_seats_bonus(
        party_to_votes: PartyToVotes, n_seats_bonus: int
    ) -> dict[str, int]:
        winning_party = sorted(
            party_to_votes.items(), key=lambda x: x[1], reverse=True
        )[0][0]
        return {winning_party: n_seats_bonus}

    @staticmethod
    def get_party_to_seats_rem(
        party_to_rem_seats: dict[str, float], n_seats_rem: int
    ) -> dict[str, int]:
        party_to_seats_rem = {}
        for party, _ in sorted(
            party_to_rem_seats.items(), key=lambda x: x[1], reverse=True
        )[:n_seats_rem]:
            if party not in party_to_seats_rem:
                party_to_seats_rem[party] = 0
            party_to_seats_rem[party] += 1
        return party_to_seats_rem

    @staticmethod
    def sort(
        party_to_seats: dict[str, int], party_to_votes: PartyToVotes
    ) -> dict[str, int]:
        return dict(
            sorted(
                party_to_seats.items(),
                key=lambda x: (x[1], party_to_votes[x[0]]),
                reverse=True,
            )
        )

    @staticmethod
    def concat(*party_to_seats_list: list[dict[str, int]]) -> dict[str, int]:
        party_to_seats = {}
        for party_to_seats_i in party_to_seats_list:
            for party, seats in party_to_seats_i.items():
                party_to_seats[party] = party_to_seats.get(party, 0) + seats
        return party_to_seats

    @staticmethod
    def get_n_seats_bonus(region_id: str) -> int:
        if region_id == "LK":
            return 0
        return 1

    @staticmethod
    def get_p_limit(region_id: str) -> float:
        if region_id == "LK":
            return 0
        return 0.05

    @staticmethod
    def get_party_to_seats(
        region_id: str, n_seats: int, party_to_votes: PartyToVotes
    ) -> dict[str, int]:
        n_seats_bonus = Seats.get_n_seats_bonus(region_id)

        filtered_party_to_votes = party_to_votes.filter(
            lambda _, votes: votes
            >= party_to_votes.total * Seats.get_p_limit(region_id)
        )

        n_seats_non_bonus = n_seats - n_seats_bonus
        party_to_seats_f = filtered_party_to_votes.norm * n_seats_non_bonus
        party_to_seats_i = party_to_seats_f.int.nonzero
        party_to_rem_seats = party_to_seats_f.non_int.nonzero

        n_seats_i = sum(party_to_seats_i.values())
        party_to_seats_rem = Seats.get_party_to_seats_rem(
            party_to_rem_seats, n_seats_non_bonus - n_seats_i
        )

        party_to_seats_bonus = Seats.get_party_to_seats_bonus(
            party_to_votes, n_seats_bonus
        )

        unsorted = Seats.concat(
            party_to_seats_i, party_to_seats_rem, party_to_seats_bonus
        )
        return Seats.sort(unsorted, party_to_votes)
