from dataclasses import dataclass
from functools import cached_property

from gig import Ent, EntType
from utils import Log

from elections_lk import ElectionParliamentary, Result

log = Log("SoClose")


class ImaginaryElectionParliamentary(ElectionParliamentary):
    def __init__(
        self,
        real_election: ElectionParliamentary,
        region_id: str,
        party_id: str,
        d_votes: int,
    ):
        super().__init__(real_election.year)
        self.real_election = real_election
        self.region_id = region_id
        self.party_id = party_id
        self.d_votes = d_votes

    def get_result(self, region_id):
        result = self.real_election.get_result(region_id)

        if not self.region_id == region_id:
            return result

        result_copy = result.copy()

        result_copy.party_to_votes.idx[self.party_id] += self.d_votes

        result_copy.vote_summary.polled += self.d_votes
        result_copy.vote_summary.valid += self.d_votes

        return result_copy


@dataclass
class SoCloseInfo:
    region_id: str
    total_before: int
    party_id: str
    votes_before: int
    d_votes: int
    party_to_seats_before: dict
    party_to_seats_after: dict

    @staticmethod
    def get_sorter():
        return lambda so_close_info: abs(so_close_info.d_votes)

    def __str__(self):
        return "\t".join(
            [
                self.region_id,
                self.region_name.ljust(15),
                self.party_id,
                f"{self.d_votes:+,}",
                f"({self.p_d_votes:+.1%} of {self.votes_before:,})",
                f"{self.p_votes_before:.1%} -> {self.p_votes_after:.1%}",
                f"{self.party_to_seats_before} -> {self.party_to_seats_after}",
            ]
        )

    @cached_property
    def p_d_votes(self):
        return self.d_votes / self.votes_before

    @cached_property
    def votes_after(self):
        return self.votes_before + self.d_votes

    @cached_property
    def p_votes_before(self):
        return self.votes_before / self.total_before

    @cached_property
    def total_after(self):
        return self.total_before + self.d_votes

    @cached_property
    def p_votes_after(self):
        return self.votes_after / self.total_after

    @cached_property
    def region_name(self):
        ent = Ent.from_id(self.region_id)
        return ent.name

    @cached_property
    def seats_before(self):
        return self.party_to_seats_before.get(self.party_id, 0)

    @cached_property
    def seats_after(self):
        return self.party_to_seats_after.get(self.party_id, 0)

    @cached_property
    def d_votes_nice(self):
        abs_d_votes = abs(self.d_votes)
        label = "more" if self.d_votes >= 0 else "fewer"
        return f"{abs_d_votes} {label}"

    @cached_property
    def title(self):
        return "".join([f"{self.party_id} {self.region_name}"])

    @cached_property
    def seats_after_nice(self):
        if self.seats_after == 1:
            return "won a seat"
        if self.seats_after == 0:
            return "lost their only seat"
        return f"gone from {self.seats_before} to {self.seats_after} seats"

    @cached_property
    def subtitle(self):
        return " ".join(
            [
                f"With {self.d_votes_nice} votes",
                f"({self.p_d_votes:.1%} of the {self.votes_before:,} they gained)",
                f"in {self.region_name},",
                f"the {self.party_id} would have",
                f"{self.seats_after_nice}.",
            ]
        )


class SoClose:
    MAX_P_GAINS = 0.5
    ALL_MAX_D_VOTES = 1_000

    def __init__(self, year: str):
        self.year = year

    def get_min_d_votes_for_next_seat(
        self,
        region_id,
        party_id,
        is_gains,
    ):
        so_close = None
        min_d_votes = 0
        max_d_votes = SoClose.ALL_MAX_D_VOTES
        for d_votes_incr in [1000, 100, 10, 1]:
            so_close = self.get_min_d_votes_for_next_seat_helper(
                region_id,
                party_id,
                is_gains,
                min_d_votes,
                max_d_votes,
                d_votes_incr,
            )
            if not so_close:
                return None

            max_d_votes = abs(so_close.d_votes) + 1
            min_d_votes = max_d_votes - d_votes_incr
        return so_close

    def get_min_d_votes_for_next_seat_helper(
        self,
        region_id,
        party_id,
        is_gains,
        min_d_votes,
        max_d_votes,
        d_votes_incr,
    ):

        real_election = ElectionParliamentary(self.year)
        region_result = real_election.get_result(region_id)
        party_to_votes = region_result.party_to_votes
        party_to_seats_before = real_election.region_to_party_to_seats[
            region_id
        ]
        seats_before = party_to_seats_before.get(party_id, 0)
        votes_before = party_to_votes[party_id]
        max_d_votes_by_p = votes_before * SoClose.MAX_P_GAINS
        total_before = party_to_votes.total
        for abs_d_votes in range(
            min_d_votes, max_d_votes + d_votes_incr, d_votes_incr
        ):
            if abs_d_votes > max_d_votes_by_p:
                return None
            d_votes = abs_d_votes * (1 if is_gains else -1)

            imag_election = ImaginaryElectionParliamentary(
                real_election, region_id, party_id, d_votes
            )
            party_to_seats_after = imag_election.region_to_party_to_seats[
                region_id
            ]
            seats_after = party_to_seats_after.get(party_id, 0)

            if seats_before != seats_after:

                return SoCloseInfo(
                    region_id=region_id,
                    total_before=total_before,
                    party_id=party_id,
                    votes_before=votes_before,
                    d_votes=d_votes,
                    party_to_seats_before=party_to_seats_before,
                    party_to_seats_after=party_to_seats_after,
                )
        return None

    def analyze(self, is_gains: bool):  # noqa

        real_election = ElectionParliamentary(self.year)

        ed_ents = Ent.list_from_type(EntType.ED)
        so_close_info_list = []
        for ed_ent in ed_ents:
            region_id = ed_ent.id

            region_result = real_election.get_result(region_id)
            party_to_pvotes = region_result.party_to_votes.party_to_pvotes
            for party_id, p_votes in party_to_pvotes.items():
                if p_votes < 0.05 / (1 + SoClose.MAX_P_GAINS):
                    continue
                so_close_info = self.get_min_d_votes_for_next_seat(
                    region_id, party_id, is_gains=is_gains
                )
                if so_close_info:
                    so_close_info_list.append(so_close_info)

        so_close_info_list.sort(key=SoCloseInfo.get_sorter())

        for i, so_close_info in enumerate(so_close_info_list, start=1):
            print(f"{i}. {so_close_info.title}")
            print(so_close_info.subtitle)
            print()


def main():
    pass


if __name__ == "__main__":
    YEAR = "2024"

    print(f"{YEAR} - NEAR MISSES")
    SoClose(YEAR).analyze(is_gains=True)
    print("-" * 64)

    print(f"{YEAR} - NEAR HITS")
    SoClose(YEAR).analyze(is_gains=False)
    print("-" * 64)
