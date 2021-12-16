from dataclasses import dataclass
from enum import Enum


class Type(Enum):
    LITERAL_VALUE = 4


@dataclass()
class BitsPacket:
    version: int
    typeID: Type
    value: None
