#%%

from icecream import ic
from __future__ import annotations


class Bits:
    _offset = -1
    _bitOffset = 4
    _data = None
    _currentNibble = None

    def __init__(self, data):
        self._data = data

    def fromHex(hexStr: str) -> Bits:
        return Bits([int(char, 16) for char in hexStr])

    def readBits(self, count: int):
        assert 0 < count <= 8
        byte = 0x0

        for _ in range(count):
            byte <<= 1
            byte |= self.readBit()

        return byte

    def readBit(self):
        if self._bitOffset >= 4:
            self._offset += 1
            self._bitOffset = 0
            self._currentNibble = self._data[self._offset]

        bit = (self._currentNibble >> 3 - self._bitOffset) & 0x1
        self._bitOffset += 1

        return bit


inp = "input.txt"
with open(inp, "r") as file:
    bits = Bits.fromHex(file.read().strip())

bits = Bits.fromHex("38006F45291200")

print(bits._currentNibble)
ic(bits.readBits(9))
print(bits._currentNibble)
