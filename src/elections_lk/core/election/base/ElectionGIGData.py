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
    def results(self) -> list[Result]:
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
    def results_idx(self) -> dict[str, Result]:
        return {result.id: result for result in self.results}

    @cached_property
    def country_result(self):
        return Result.from_list('LK', self.results)

    @cached_property
    def pd_ids(self):
        return list(self.results_idx.keys())

    @cache
    def get_result(self, pd_id: str) -> Result:
        if pd_id == 'LK':
            return self.country_result
        if pd_id in self.results_idx:
            return self.results_idx[pd_id]
        log.error(f'No result found for {pd_id}')
        return None
