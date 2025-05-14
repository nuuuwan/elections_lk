from functools import cache


class RawData:
    EXTRA_FIELD_DELIM = ":"

    @staticmethod
    @cache
    def is_extra_field(k: str, name: str = None) -> bool:
        if not name:
            return RawData.EXTRA_FIELD_DELIM in k
        return k.endswith(RawData.EXTRA_FIELD_DELIM + name)

    @staticmethod
    @cache
    def remove_extra_field(k: str) -> str:
        if RawData.is_extra_field(k):
            return k.split(RawData.EXTRA_FIELD_DELIM)[0]
        raise ValueError(f"Key {k} misses {RawData.EXTRA_FIELD_DELIM}")
