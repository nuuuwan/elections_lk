from elections_lk.base import IntDict
from elections_lk.core.result.PartyToVotes import PartyToVotes


class Seats:

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
        return IntDict(party_to_seats_rem)

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
    ) -> IntDict:
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
        party_to_seats_bonus = IntDict({party_to_votes.max_key: n_seats_bonus})
        return (
            party_to_seats_i + party_to_seats_rem + party_to_seats_bonus
        ).sort(lambda party: party_to_votes[party])
