from functools import reduce
import operator
from .Bits import Bits
from .BitsPacket import BitsPacket, Type
from icecream import ic


class BitsParser:
    versionSum = 0

    def parse(self, bits: Bits):
        self.versionSum = 0

        return self._readPacket(bits)

    def _readPacket(self, bits: Bits):
        version = bits.readBits(3)
        typeID = Type(bits.readBits(3))
        value = None
        subPackets = None

        self.versionSum += version

        if typeID == Type.LITERAL_VALUE:
            value = self._readValue(bits)
        else:
            # Packet is an operator
            lenTypeID = bits.readBit()
            if lenTypeID == 1:
                # N packets long (11-bit number)
                length = bits.readInt(11)
                subPackets = []
                for _ in range(length):
                    # Read a package
                    packet = self._readPacket(bits)
                    subPackets.append(packet)
            else:
                # N bit long (15-bit number)
                length = bits.readInt(15)
                bitsSlice = bits.getSlice(length)
                subPackets = self._readAllPackets(bitsSlice)

            values = [p.value for p in subPackets]

            if typeID == Type.SUM:
                value = sum(values)
            if typeID == Type.PRODUCT:
                value = reduce(operator.mul, values)
            if typeID == Type.MINIMUM:
                value = min(values)
            if typeID == Type.MAXIMUM:
                value = max(values)
            if typeID == Type.GREATER_THAN:
                value = 1 if values[0] > values[1] else 0
            if typeID == Type.LESS_THAN:
                value = 1 if values[0] < values[1] else 0
            if typeID == Type.EQUAL_TO:
                value = 1 if values[0] == values[1] else 0

        packet = BitsPacket(version, typeID, value, subPackets)
        return ic(packet)

    def _readAllPackets(self, bits: Bits):
        packets = []
        while bits.hasData():
            packet = self._readPacket(bits)
            packets.append(packet)
        return packets

    def push(self, symbol):
        self._stack.append()

    def peek(self):
        return self._stack[-1]

    def pop(self):
        return self._stack.pop()

    def _reset(self):
        self._stack = []

    def _readValue(self, bits: Bits):
        value = 0x0
        isLastGroup = False
        while not isLastGroup:
            isLastGroup = bits.readBit() == 0
            nibble = bits.readBits(4)

            value <<= 4
            value |= nibble

        return value
