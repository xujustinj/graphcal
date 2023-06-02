from dataclasses import dataclass
from functools import cached_property
import os

from core import Name, Node

Value = Name

@dataclass(frozen=True)
class File:
    path: str

    def to_node(self) -> Node:
        return Node((f"!{self.__class__.__name__}", self.path))

    @cached_property
    def properties(self) -> dict[str, Value]:
        _, ext = os.path.splitext(self.path)
        size = os.stat(self.path).st_size
        return {
            "has_file_extension": ("!!file_extension", ext.lower()),
            "has_file_size": ("!!file_size_bytes", size),
        }
