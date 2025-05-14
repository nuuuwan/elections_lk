from functools import cached_property

from gig import EntType

from elections_lk.constants import YEAR_TO_REGION_TO_SEATS
from elections_lk.core.election.base.Election import Election
from elections_lk.core.election.categories.ElectionCategory import (
    ElectionCategory,
)
from elections_lk.core.Seats import Seats


class ElectionParliamentary(Election):
    def __init__(self, year: str):
        super().__init__(year, ElectionCategory.PARLIAMENTARY)

    @staticmethod
    def get_base_ent_type() -> str:
        return EntType.PD

    @staticmethod
    def get_years() -> list[str]:
        return [
            "1989",
            "1994",
            "2000",
            "2001",
            "2004",
            "2010",
            "2015",
            "2020",
            "2024",
        ]

    @cached_property
    def region_to_seats(self) -> dict[str, Seats]:
        return YEAR_TO_REGION_TO_SEATS[self.year]

    @cached_property
    def region_to_party_to_seats(self) -> dict[str, dict[str, int]]:
        ed_to_result = self.get_results_idx_for_type(EntType.ED)
        idx = {}
        for region_id, n_seats in self.region_to_seats.items():
            result = (
                ed_to_result[region_id]
                if region_id != "LK"
                else self.lk_result
            )
            idx[region_id] = (
                Seats.get_party_to_seats(
                    region_id, n_seats, result.party_to_votes
                )
                if result
                else 0
            )
        return idx

    @cached_property
    def cum_party_to_seats(self) -> dict[str, int]:
        unsorted = Seats.concat(*self.region_to_party_to_seats.values())
        return Seats.sort(unsorted, self.lk_result.party_to_votes)
