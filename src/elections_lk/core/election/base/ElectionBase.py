from dataclasses import dataclass
from functools import cached_property


@dataclass
class ElectionBase:
    year: str
    category: str

    def __hash__(self):
        return hash((self.year, self.category))

    @cached_property
    def title(self) -> str:
        return f'{self.year} {self.category.title()}'
