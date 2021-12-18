#%%

from __future__ import annotations
from os import EX_PROTOCOL
from typing import TypeVar, Generic, Union
from icecream import ic
from dataclasses import dataclass
import json

T = TypeVar("T")


@dataclass()
class Ref(Generic[T]):
    val: T

    def _deref(self, other):
        if type(other) is Ref:
            return other.val
        return other

    def __add__(self, other):
        self.val = Ref(self.val + self._deref(other))

    def __iadd__(self, other):
        self.val += self._deref(other)

    def __eq__(self, other):
        return self.val == self._deref(other)

    def __repr__(self) -> str:
        return f"*{self.val.__repr__()}"

    def __str__(self) -> str:
        return f"{self.val.__str__()}"

    def __bool__(self):
        return not not self.val


def left(pair: Ref[list]) -> Ref:
    return pair.val[0]


def right(pair: Ref[list]) -> Ref:
    return pair.val[1]


def descend(selector, pair, stop=lambda el: type(el.val) is not list):
    if stop(pair):
        return pair
    return descend(selector, selector(pair), stop)


def leftmost(pair: Ref[list]) -> Union[Ref, None]:
    return descend(left, pair)


def rightmost(pair: Ref[list]) -> Union[Ref, None]:
    return descend(right, pair)


def finalize_explode(num: Ref[list], stack: list = None):
    """
    Returns true when done
    Returns false while no pair is being exploded
    """
    if not stack:
        stack = []
    stack = stack.copy()

    if type(num.val) is int:
        ic("num", len(stack), num)
        return False

    if len(stack) >= 4:
        ic("len", len(stack), num)

        branchStack = stack.copy()
        leftBranch = None
        rightBranch = None
        current = num
        while branchStack and not (leftBranch and rightBranch):
            child = current
            current = branchStack.pop()
            leftChild = left(current)
            rightChild = right(current)
            if not leftBranch and (
                type(child.val) != type(leftChild.val) or child != leftChild
            ):
                leftBranch = leftChild
            if not rightBranch and (
                type(child.val) != type(rightChild.val) or child != rightChild
            ):
                rightBranch = rightChild

        if leftBranch:
            leftNum = rightmost(leftBranch)
            leftNum += left(num)
        if rightBranch:
            rightNum = leftmost(rightBranch)
            rightNum += right(num)

        num.val = 0
        return True

    stack.append(num)

    done = finalize_explode(left(num), stack)
    if done:
        return True

    done = finalize_explode(right(num), stack)
    if done:
        return True


def findFirst(predicate, pair, stack=None):
    if not stack:
        stack = []

    stack = stack.copy()

    if predicate(pair, stack):
        return pair, stack

    if type(pair.val) is not list:
        return None

    stack.append(pair)

    if result := findFirst(predicate, left(pair), stack):
        return result
    if result := findFirst(predicate, right(pair), stack):
        return result

    return None


def finalize_explode2(pair: list):
    def exploding(el, stack):
        return type(el.val) is list and len(stack) >= 4
    result = findFirst(exploding, pair)

    if not result:
        return False
    pair, stack = result

    leftBranch = None
    rightBranch = None
    current = pair
    while stack and not (leftBranch and rightBranch):
        child = current
        current = stack.pop()
        leftChild = left(current)
        rightChild = right(current)
        if not leftBranch and (
            type(child.val) != type(leftChild.val) or child != leftChild
        ):
            leftBranch = leftChild
        if not rightBranch and (
            type(child.val) != type(rightChild.val) or child != rightChild
        ):
            rightBranch = rightChild

    if leftBranch:
        leftNum = rightmost(leftBranch)
        leftNum += left(pair)
    if rightBranch:
        rightNum = leftmost(rightBranch)
        rightNum += right(pair)

    pair.val = 0

    return True


def convertToRefs(el):
    if type(el) is list:
        return Ref([convertToRefs(x) for x in el])
    return Ref(el)


numbers = [
    "[[[[[9,8],1],2],3],4]",
    "[7,[6,[5,[4,[3,2]]]]]",
    "[[6,[5,[4,[3,2]]]],1]",
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
]

for i,number in enumerate(numbers):
    number = json.loads(number)
    num0 = convertToRefs(number)
    num1 = convertToRefs(number)
    num2 = convertToRefs(number)

    ic.prefix = f"ic| {i}| "
    ic('----------')
    ic(num0)
    ic(finalize_explode(num1))
    ic(finalize_explode2(num2))

    ic(num0)
    ic(num1)
    ic(num2)
