from dataclasses import dataclass


@dataclass
class ElectionBase:
    year: str
    category: str

    def __hash__(self):
        return hash((self.year, self.category))