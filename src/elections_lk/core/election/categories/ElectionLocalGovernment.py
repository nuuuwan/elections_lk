from functools import cached_property

from gig import EntType

from elections_lk.core.election.base.Election import Election
from elections_lk.core.election.categories.ElectionCategory import \
    ElectionCategory


class ElectionLocalGovernment(Election):
    def __init__(self, year: str):
        super().__init__(year, ElectionCategory.LOCAL_GOVERNMENT)

    @staticmethod
    def get_base_ent_type() -> str:
        return EntType.LG

    @staticmethod
    def get_years() -> list[str]:
        return [
            "2025",
        ]

    @cached_property
    def has_result_seats(self) -> bool:
        return True
