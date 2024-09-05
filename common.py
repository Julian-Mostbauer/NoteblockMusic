from __future__ import annotations
from typing import Dict

class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def absolute_str(self) -> str:
        return f"{self.x} {self.y} {self.z}"

    def relative_str(self) -> str:
        return f"~{self.x} ~{self.y} ~{self.z}"

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)


class Block:
    def __init__(self, name: str, attributes: Dict, position: Position):
        self.name = name
        self.attributes = attributes
        self.position = position

    def absolute_str(self) -> str:
        atr_str = ",".join([f"{key}={value}" for key, value in self.attributes.items()])
        return f"{self.position.absolute_str()} minecraft:{self.name}[{atr_str}]"

    def relative_str(self) -> str:
        atr_str = ",".join([f"{key}={value}" for key, value in self.attributes.items()])
        return f"{self.position.relative_str()} minecraft:{self.name}[{atr_str}]"