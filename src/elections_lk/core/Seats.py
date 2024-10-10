class Seats:
    @staticmethod
    def get_filtered_party_to_votes(
        party_to_votes: dict[str, int], p_limit: float
    ) -> dict[str, int]:
        min_votes = party_to_votes.total * p_limit
        return {
            party: votes
            for party, votes in party_to_votes.items()
            if votes >= min_votes
        }

    @staticmethod
    def get_party_to_seats_f(
        party_to_votes: dict[str, int], n_seats: int
    ) -> dict[str, int]:
        total = sum(party_to_votes.values())
        party_to_seats_f = {}
        for party, votes in party_to_votes.items():
            party_to_seats_f[party] = n_seats * votes / total
        return party_to_seats_f

    @staticmethod
    def filter_nonzero(party_to_seats: dict[str, float]) -> dict[str, int]:
        return {
            party: int(seats)
            for party, seats in party_to_seats.items()
            if seats > 0
        }

    @staticmethod
    def get_party_to_seats_i(
        party_to_seats_f: dict[str, int]
    ) -> tuple[dict[str, int], dict[str, int]]:
        unfiltered = {
            party: int(seats) for party, seats in party_to_seats_f.items()
        }
        return Seats.filter_nonzero(unfiltered)

    @staticmethod
    def get_party_to_rem_seats(
        party_to_seats_f: dict[str, int]
    ) -> dict[str, float]:
        return {
            party: seats - int(seats)
            for party, seats in party_to_seats_f.items()
        }

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
    def get_party_to_seats_bonus(
        party_to_votes: dict[str, int], n_seats_bonus: int
    ) -> dict[str, int]:
        winning_party = sorted(
            party_to_votes.items(), key=lambda x: x[1], reverse=True
        )[0][0]
        return {winning_party: n_seats_bonus}

    @staticmethod
    def sort(
        party_to_seats: dict[str, int], party_to_votes: dict[str, int]
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
        if region_id == 'LK':
            return 0
        return 1

    @staticmethod
    def get_p_limit(region_id: str) -> float:
        if region_id == 'LK':
            return 0
        return 0.05

    @staticmethod
    def get_party_to_seats(
        region_id: str, n_seats: int, party_to_votes: dict[str, int]
    ) -> dict[str, int]:
        n_seats_bonus = Seats.get_n_seats_bonus(region_id)
        p_limit = Seats.get_p_limit(region_id)

        filtered_party_to_votes = Seats.get_filtered_party_to_votes(
            party_to_votes, p_limit
        )

        n_seats_non_bonus = n_seats - n_seats_bonus
        party_to_seats_f = Seats.get_party_to_seats_f(
            filtered_party_to_votes, n_seats_non_bonus
        )
        party_to_seats_i = Seats.get_party_to_seats_i(party_to_seats_f)
        party_to_rem_seats = Seats.get_party_to_rem_seats(party_to_seats_f)

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
