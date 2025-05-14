from dataclasses import dataclass


@dataclass
class PartyToSeats:
    idx: dict[str, int]
