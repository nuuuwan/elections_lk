from gig import EntType

from elections_lk.core.election.base.Election import Election
from elections_lk.core.election.categories.ElectionCategory import \
    ElectionCategory


class ElectionPresidential(Election):
    def __init__(self, year: str):
        super().__init__(year, ElectionCategory.PRESIDENTIAL)

    @staticmethod
    def get_base_ent_type() -> str:
        return EntType.PD

    @staticmethod
    def get_years() -> list[str]:
        return [
            "1982",
            "1988",
            "1994",
            "1999",
            "2005",
            "2010",
            "2015",
            "2019",
            "2024",
        ]
