from elections_lk.core.election.base.Election import Election
from elections_lk.core.election.categories.ElectionCategory import \
    ElectionCategory


class ElectionPresidential(Election):
    def __init__(self, year: str):
        super().__init__(year, ElectionCategory.PRESIDENTIAL)
