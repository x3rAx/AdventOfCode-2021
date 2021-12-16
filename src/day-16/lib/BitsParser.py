from .Bits import Bits
from .BitsPacket import BitsPacket, Type
from icecream import ic

class BitsParser:
    def parse(self, bits: Bits):
        return self._readPacket(bits)

    def _readPacket(self, bits: Bits):
        version = bits.readBits(3)
        typeID = bits.readBits(3)
        value = None

        if typeID == Type.LITERAL_VALUE.value:
            value = self._readValue(bits)
        else:
            # Packet is an operator
            lenTypeID = bits.readBit()
            if lenTypeID == 1:
                # N packets long (11-bit number)
                length = bits.readInt(11)
                value = []
                for _ in range(length):
                    # Read a package
                    packet = self._readPacket(bits)
                    value.append(packet)
            else:
                # N bit long (15-bit number)
                length = bits.readInt(15)
                bitsSlice = bits.getSlice(length)
                value = self._readAllPackets(bitsSlice)

        ic(version, typeID, value)

        packet = BitsPacket(version, typeID, value)
        ic(packet)
        return packet

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
            ic()
            isLastGroup = bits.readBit() == 0
            nibble = bits.readBits(4)

            value <<= 4
            value |= nibble

        return value
