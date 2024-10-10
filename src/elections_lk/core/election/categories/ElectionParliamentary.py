from functools import cached_property

from elections_lk.constants import YEAR_TO_REGION_TO_SEATS
from elections_lk.core.election.base.Election import Election
from elections_lk.core.election.categories.ElectionCategory import \
    ElectionCategory
from elections_lk.core.Seats import Seats


class ElectionParliamentary(Election):
    def __init__(self, year: str):
        super().__init__(year, ElectionCategory.PARLIAMENTARY)

    @staticmethod
    def get_years() -> list[str]:
        return [
            '1989',
            '1994',
            '2000',
            '2001',
            '2004',
            '2010',
            '2015',
            '2020',
        ]

    @staticmethod
    def list_all() -> list['ElectionParliamentary']:
        return [
            ElectionParliamentary(year)
            for year in ElectionParliamentary.get_years()
        ]

    @cached_property
    def region_to_seats(self) -> dict[str, Seats]:
        return YEAR_TO_REGION_TO_SEATS[self.year]

    @cached_property
    def region_to_party_to_seats(self) -> dict[str, dict[str, int]]:
        return {
            region_id: Seats.get_party_to_seats(
                region_id, n_seats, self.get_result(region_id).party_to_votes
            )
            for region_id, n_seats in self.region_to_seats.items()
        }

    @cached_property
    def cum_party_to_seats(self) -> dict[str, int]:
        unsorted = Seats.concat(*self.region_to_party_to_seats.values())
        return Seats.sort(unsorted, self.get_result('LK').party_to_votes)
