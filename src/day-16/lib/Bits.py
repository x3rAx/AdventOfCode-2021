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

    def hasData(self) -> bool:
        return self._offset < len(self._data) and self._bitOffset < 4

    def readBits(self, count: int):
        assert 0 < count <= 8, f"Count must be `]0;8]` when reading bits. Was `{count}`"
        return self.readInt(count)

    def readBit(self):
        if self._bitOffset >= 4:
            self._offset += 1
            self._bitOffset = 0
            self._currentNibble = self._data[self._offset]

        bit = (self._currentNibble >> 3 - self._bitOffset) & 0x1
        self._bitOffset += 1

        return bit

    def getSlice(self, count: int):
        data = []
        for rest in range(count, 0, -4):
            l = min(4, rest)
            bits = self.readBits(l)
            if l < 4:
                bits <<= 4 - l
            data.append(bits)

        return Bits(data)

    def readInt(self, count):
        value = 0x0

        for _ in range(count):
            value <<= 1
            value |= self.readBit()

        return value

