from dataclasses import dataclass

from core import Token, Node

@dataclass(frozen=True)
class ValueType:
    name: str

    def __call__(self, *values: list[Token]) -> Node:
        return Node((f"!!{self.name}", *values))

Bytes = ValueType("bytes")
Camera = ValueType("camera")
DurationSeconds = ValueType("duration_seconds")
FileExtension = ValueType("file_extension")
Pixels = ValueType("pixels")
Time = ValueType("time")
