from elections_lk.core.election.base.Election import Election
from elections_lk.core.election.categories.ElectionCategory import \
    ElectionCategory


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


if __name__ == '__main__':
    for election in ElectionParliamentary.list_all():
        print(election.year, election.results[0])
