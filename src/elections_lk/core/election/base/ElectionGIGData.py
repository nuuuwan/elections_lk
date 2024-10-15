import time
from functools import cache, cached_property

from gig import GIGTable
from utils import Log

from elections_lk.core.result import Result

log = Log('ElectionGIGData')


class ElectionGIGData:
    @property
    def gig_table(self) -> GIGTable:
        return GIGTable(
            f'government-elections-{self.category}', 'regions-ec', self.year
        )

    @cached_property
    def remote_data_list(self):
        t = 1
        while True:
            try:
                remote_data_list = self.gig_table.remote_data_list
                if remote_data_list:
                    return remote_data_list
            except BaseException:
                log.error('Retrying...')
                time.sleep(t)
                t *= 2

    @cached_property
    def pd_results(self) -> list[Result]:
        results = []
        for row in self.remote_data_list:
            entity_id = row['entity_id']
            if not (
                entity_id.startswith('EC-')
                and len(entity_id) >= 6
                and not entity_id.endswith('-')
            ):
                continue
            result = Result.from_dict(row)
            results.append(result)
        return results

    @cached_property
    def pd_results_idx(self) -> dict[str, Result]:
        return {result.id: result for result in self.pd_results}

    @cached_property
    def ed_results_idx(self) -> dict[str, Result]:
        ed_to_pd_results = {}
        for pd_result in self.pd_results:
            ed_id = pd_result.id[:5]
            if ed_id not in ed_to_pd_results:
                ed_to_pd_results[ed_id] = []
            ed_to_pd_results[ed_id].append(pd_result)

        return {
            ed_id: Result.from_list(ed_id, pd_results)
            for ed_id, pd_results in ed_to_pd_results.items()
        }

    @cached_property
    def lk_result(self):
        return Result.from_list('LK', self.pd_results)

    @cache
    def get_result(self, id: str) -> Result:
        if id in self.pd_results_idx:
            return self.pd_results_idx[id]
        if id in self.ed_results_idx:
            return self.ed_results_idx[id]
        if id == 'LK':
            return self.lk_result

        raise Exception(f'No result found for {id}')

    @cached_property
    def winning_party_id(self) -> str:
        return self.lk_result.winning_party_id
