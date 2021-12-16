#%%

from icecream import ic
from lib import Bits
from lib import BitsParser

inp = "input.txt"
with open(inp, "r") as file:
    bits = Bits.fromHex(file.read().strip())

bits = Bits.fromHex("EE00D40C823060")
parser = BitsParser()
msg = ic(parser.parse(bits))

