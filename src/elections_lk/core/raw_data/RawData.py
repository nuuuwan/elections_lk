from functools import cache


class RawData:
    EXTRA_FIELD_DELIM = ":"

    @staticmethod
    @cache
    def is_extra_field(k: str) -> bool:
        return RawData.EXTRA_FIELD_DELIM in k
