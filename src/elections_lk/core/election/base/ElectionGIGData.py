import time
from functools import cache, cached_property

from gig import GIGTable, EntType
from utils import Log

from elections_lk.core.result import Result

log = Log("ElectionGIGData")


class ElectionGIGData:

    @property
    def gig_table(self) -> GIGTable:
        return GIGTable(
            f"government-elections-{self.category}", "regions-ec", self.year
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
                log.error(f"[{t}s] Retrying...")
                time.sleep(t)
                t *= 2

    @cached_property
    def base_results(self) -> list[Result]:
        results = []
        base_ent_type = self.get_base_ent_type()
        for row in self.remote_data_list:
            entity_id = row["entity_id"]
            ent_type = EntType.from_id(entity_id)
            if ent_type != base_ent_type:
                continue
            result = Result.from_dict(row)
            results.append(result)
        return results

    @cached_property
    def base_results_idx(self) -> dict[str, Result]:
        return {result.id: result for result in self.base_results}

    @cached_property
    def lk_result(self):
        return Result.from_list("LK", self.base_results)
