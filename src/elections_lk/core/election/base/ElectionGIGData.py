import time
from functools import cache, cached_property

from gig import EntType, GIGTable
from utils import Log

from elections_lk.core.result import Result, ResultWithSeats

log = Log("ElectionGIGData")


class ElectionGIGData:

    @property
    def gig_table(self) -> GIGTable:
        return GIGTable(
            f"government-elections-{self.category}",
            "regions-ec",
            f"{self.year}",
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
                log.error(f"[{self.gig_table}] Retrying in {t}s...")
                time.sleep(t)
                t *= 2

    def get_result_from_row(self, row: dict) -> Result:
        if self.has_result_seats:
            return ResultWithSeats.from_dict(row)
        return Result.from_dict(row)

    @cache
    def get_result_for_id(self, entity_id: str) -> Result:
        for row in self.remote_data_list:
            if row["entity_id"] == entity_id:
                return self.get_result_from_row(row)
        raise ValueError(f"Result not found for entity_id: {entity_id}")

    def get_results_for_type(self, ent_type: EntType) -> list[Result]:
        results = []
        for row in self.remote_data_list:
            entity_id = row["entity_id"]
            if EntType.from_id(entity_id) == ent_type:
                result = self.get_result_from_row(row)
                results.append(result)
        return results

    def get_results_idx_for_type(
        self, ent_type: EntType
    ) -> dict[str, Result]:
        results = self.get_results_for_type(ent_type)
        return {result.id: result for result in results}

    @cached_property
    def base_results(self) -> list[Result]:
        return self.get_results_for_type(self.get_base_ent_type())

    @cached_property
    def lk_result(self):
        return self.get_result_for_id("LK")

    @cached_property
    def winning_party_id(self) -> str:
        return self.lk_result.winning_party_id
