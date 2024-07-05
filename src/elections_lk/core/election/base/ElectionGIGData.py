from gig import Ent, EntType, GIGTable

from elections_lk.core.result import ResultPD


class ElectionGIGData:
    @property
    def gig_table(self) -> GIGTable:
        return GIGTable(
            f'government-elections-{self.category}', 'regions-ec', self.year
        )

    @property
    def pd_results(self) -> list[ResultPD]:
        pd_ents = Ent.list_from_type(EntType.PD)
        pd_results = []
        for pd_ent in pd_ents:
            gig_table_row = pd_ent.gig(self.gig_table)
            pd_result = ResultPD.from_gig_table_row(gig_table_row)
            pd_results.append(pd_result)

        return pd_results
