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

    @cache
    def get_result_for_id(self):
        for row in self.remote_data_list:
            if row["entity_id"] == id:
                return Result.from_dict(row)
        raise ValueError(f"Result not found for id: {id}")

    @cache
    def get_results_for_type(self, ent_type: EntType) -> list[Result]:
        results = []
        for row in self.remote_data_list:
            entity_id = row["entity_id"]
            if EntType.from_id(entity_id) != ent_type:
                continue
            result = Result.from_dict(row)
            results.append(result)
        return results

    @cache
    def get_results_idx_for_type(self, ent_type: EntType) -> dict[str, Result]:
        results = self.get_results_for_type(ent_type)
        return {result.id: result for result in results}

    @cached_property
    def base_results(self) -> list[Result]:
        return self.get_results_for_type(self.get_base_ent_type())

    @cached_property
    def base_results_idx(self) -> dict[str, Result]:
        return self.get_results_idx_for_type(self.get_base_ent_type())

    @cached_property
    def lk_result(self):
        return self.get_result_for_id("LK")
