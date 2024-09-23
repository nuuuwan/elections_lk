from elections_lk.core.election.base.Election import Election
from elections_lk.core.election.categories.ElectionCategory import \
    ElectionCategory


class ElectionPresidential(Election):
    def __init__(self, year: str):
        super().__init__(year, ElectionCategory.PRESIDENTIAL)

    @staticmethod
    def get_years() -> list[str]:
        return [
            '1982',
            '1988',
            '1994',
            '1999',
            '2005',
            '2010',
            '2015',
            '2019',
            '2024',
        ]

    @staticmethod
    def list_all() -> list['ElectionPresidential']:
        return [
            ElectionPresidential(year)
            for year in ElectionPresidential.get_years()
        ]
