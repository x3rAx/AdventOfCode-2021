from dataclasses import dataclass
from enum import Enum


class Type(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL_VALUE = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


@dataclass()
class BitsPacket:
    version: int
    typeID: Type
    value: None
    subPackets: None
