#%% Part 1

from icecream import ic
from lib import Bits
from lib import BitsParser

ic.disable()


def readBitsMessage(inp: str):
    with open(inp, "r") as file:
        return Bits.fromHex(file.read().strip())


#bits = Bits.fromHex("8A004A801A8002F478") # 16
#bits = Bits.fromHex("620080001611562C8802118E34") # 12
#bits = Bits.fromHex("C0015000016115A2E0802F182340") # 23
#bits = Bits.fromHex("A0016C880162017C3686B18A3D4780") # 31

bits = readBitsMessage("input.txt")
parser = BitsParser()
msg = ic(parser.parse(bits))

print("Result 1:", parser.versionSum)
print("Result 2:", msg.value)
