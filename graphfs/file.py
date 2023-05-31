from dataclasses import dataclass

@dataclass(frozen=True)
class File:
    path: str
