from dataclasses import dataclass


@dataclass
class ElectionBase:
    year: str
    category: str
