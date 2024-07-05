from functools import cached_property

from gig import Ent, EntType, GIGTable

from elections_lk.core.result import Result


class ElectionGIGData:
    @property
    def gig_table(self) -> GIGTable:
        return GIGTable(
            f'government-elections-{self.category}', 'regions-ec', self.year
        )

    @cached_property
    def pd_results(self) -> list[Result]:
        pd_ents = Ent.list_from_type(EntType.PD)
        pd_results = []
        for pd_ent in pd_ents:
            gig_table_row = pd_ent.gig(self.gig_table)
            pd_result = Result.from_gig_table_row(gig_table_row)
            pd_results.append(pd_result)

        return pd_results

    @cached_property
    def pd_results_idx(self) -> dict[str, Result]:
        return {pd_result.id: pd_result for pd_result in self.pd_results}

    @cached_property
    def country_result(self):
        return Result.from_list('LK', self.pd_results)
