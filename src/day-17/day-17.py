#%% Setup

from icecream import ic
import re


def readInp(inp: str):
    with open(inp, "r") as file:
        line = file.readline().strip()
        matches = re.match(
            "target area: x=(?P<xMin>(-|)\d+)\.\.(?P<xMax>(-|)\d+), y=(?P<yMin>(-|)\d+)\.\.(?P<yMax>(-|)\d+)",
            line,
        )
        xMin = int(matches["xMin"])
        xMax = int(matches["xMax"])
        yMin = int(matches["yMin"])
        yMax = int(matches["yMax"])
        return (xMin, xMax, yMin, yMax)


def triangularNumber(n):
    return (n * (n + 1)) / 2


#%% Part 1

# As there is no drag in y direction, only "gravity" affects the next height of
# the probe. Because gravity is constant, the probe eventually reaches exactly
# height 0 again when thrown up. However the y-velocity (`V_y_start`) is then
# inverted. In the nex step, the y-velosity is `V_y_start - 1` because of
# gravity.
#
# Hence, the maximum possible y velocity to still hit the target area
# is the one, for which the probes position reaches the lowest point of the
# target area (T_y_min), exactly one step after it passes height 0. As `-1` is
# added to the velocity in every step, the maximum allowed y velocity is
#
#     V_y_start = T_y_min - 1
#
# The `-1` here counteracts the `-1` of gravity, during fall, when velocity is
# negative: `-(T_y_min - 1) - 1 = -T_y_min + 1 - 1` = -T_y_min. So one step
# after passing height `0`, the probe is at position `T_y_min`.
#
# We can now calculate the height that would be reached with this velocity:
#
# Start by calculating the y position in each step:
#
#     y(0) = 0
#     y(t) = y(t-1) + V_y_start - (t-1)   , for t > 0
#
# So `y(3)` would be `V_y_start + V_y_start - 1 + V_y_start - 2`. If you try to
# find the maximum, you cannot let `V_y_start - (t-1)` become less than `0` so
#
#        argmax_{t}(y(t)) = argmax_{t}( V_y_start + V_y_start - (t-1) + ... + V_y_start - (V_y_start - 1) + V_y_start - (V_y_start+1 - 1) )
#     => argmax_{t}(y(t)) = argmax_{t}( V_y_start + V_y_start - (t-1) + ... + 1 + 0 )
#
# So for the maximum `t` value, `y(t)` is the
# [triangular number](https://en.wikipedia.org/wiki/Triangular_number)
# of `V_y_min`:
#
#     \sum_{k=1}^{n}{k} = 1 + 2 + 3 + ... + n
#                       = \frac{ n^2 + n }{ 2 }
#                       = \frac{ n (n + 1) }{ 2 }

xMin, xMax, yMin, yMax = readInp("input.txt")

V_start = -yMin
maxHeight = int(triangularNumber(V_start - 1))

print("Result 1:", maxHeight)
