from gig import Ent

from elections_lk.core import ElectionParliamentary, PartyToVotes, Seats


class SeatAllocation:
    def analyze_region(
        self,
        region_id: str,
        party_to_seats: dict[str, int],
        party_to_votes: PartyToVotes,
    ):
        name = Ent.from_id(region_id).name
        print('\t', '-' * 80)
        print('\t', f'{name} ({region_id})')
        n_seats = sum(party_to_seats.values())
        total_votes = sum(party_to_votes.values())
        non_other_votes = 0
        non_eliminated_votes = 0

        # replay
        n_seats_bonus = Seats.get_n_seats_bonus(region_id)
        p_limit = Seats.get_p_limit(region_id)

        n_seats_non_bonus = n_seats - n_seats_bonus
        votes_per_non_bonus_seat = total_votes / n_seats_non_bonus
        print(
            '\t\t',
            'seats(int)'.rjust(10),
            f'{votes_per_non_bonus_seat:,.0f}'.rjust(10),
        )

        votes_limit = p_limit * total_votes
        print('\t\t', 'p_limit'.rjust(10), f'{votes_limit:,.0f}'.rjust(10))

        print('\t\t', '-' * 32)

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

        for party_id, votes in party_to_votes.items():
            seats = party_to_seats.get(party_id, 0)
            p_votes = votes / total_votes
            if seats == 0 and p_votes < min(0.1 / n_seats, 0.01):
                continue
            if votes > votes_limit:
                non_eliminated_votes += votes
            seats_f_true = n_seats * votes / total_votes
            d_seats = seats - seats_f_true
            votes_per_seat = f'{votes / seats:,.0f}' if seats > 0 else '∞'

            seats_f = party_to_seats_f.get(party_id, 0)
            seats_i = party_to_seats_i.get(party_id, 0)
            party_to_rem_seats.get(party_id, 0)
            seats_rem = party_to_seats_rem.get(party_id, 0)
            seats_bonus = party_to_seats_bonus.get(party_id, 0)

            limit_emoji = 'x' if p_votes < p_limit else ''

            print(
                '\t\t',
                party_id[:6].rjust(8),
                f'{votes:,}'.rjust(10),
                f'{p_votes:.2%}'.rjust(6),
                limit_emoji.rjust(2),
                f'{votes_per_seat}'.rjust(10),
                f'{seats}'.rjust(6),
                f'({seats_f_true:.2f})'.rjust(8),
                f'{d_seats:.2f}'.rjust(6),
                f'{seats_f:.2f}'.rjust(6),
                f'{seats_i} + {seats_rem} + {seats_bonus}'.rjust(15),
            )
            non_other_votes += votes
        other_votes = total_votes - non_other_votes
        p_votes = other_votes / total_votes
        seats_f_true = n_seats * other_votes / total_votes
        print(
            '\t\t',
            "Others".rjust(8),
            f'{other_votes:,}'.rjust(10),
            f'{p_votes:.2%}'.rjust(6),
            'x'.rjust(2),
            '∞'.rjust(10),
            '0'.rjust(6),
            f'({seats_f_true:.2f})'.rjust(8),
            f'{-seats_f_true:.2f}'.rjust(6),
        )

        p_non_eliminated = non_eliminated_votes / total_votes
        p_eliminated = 1 - p_non_eliminated
        print('\t\t', '-' * 32)
        print(
            '\t\t',
            "Eliminated".rjust(8),
            f'{p_eliminated:.1%}'.rjust(6),
        )

    def analyze_election(self, election: ElectionParliamentary):
        print(election.year)
        for (
            region_id,
            party_to_seats,
        ) in election.region_to_party_to_seats.items():
            result = election.get_result(region_id)
            self.analyze_region(
                region_id, party_to_seats, result.party_to_votes
            )

    def analyze(self):
        elections = ElectionParliamentary.list_all()[-2:-1]
        for election in elections:
            self.analyze_election(election)


if __name__ == "__main__":
    SeatAllocation().analyze()
