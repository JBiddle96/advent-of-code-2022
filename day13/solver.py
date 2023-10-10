from __future__ import annotations

from functools import cmp_to_key
from string import digits
from typing import Optional

from icecream import ic


class ListTree:
    def __init__(self) -> None:
        self.children = []
        self.parent: Optional[ListTree] = None

    def add_child(self, child: ListTree):
        self.children.append(child)
        child.parent = self

    def append(self, val):
        self.children.append(val)

    def to_list(self) -> list:
        return [e.to_list() if isinstance(e, ListTree) else e for e in self.children]


def parse_string(input: str) -> list:
    if not input.startswith("["):
        raise ValueError("Invalid input")
    input = input[1:-1]
    result = ListTree()
    current_list = result
    num = ""
    for char in input:
        if char in digits:
            num += char
        elif num:
            current_list.append(int(num))
            num = ""

        if char == "[":
            current_list.add_child(ListTree())
            current_list = current_list.children[-1]
        elif char == "]":
            if current_list.parent is not None:
                current_list = current_list.parent
            else:
                return result.to_list()

    if num:
        current_list.append(int(num))

    return result.to_list()


def compare(left: list, right: list) -> int:
    for e1, e2 in zip(left, right):
        if isinstance(e1, int) and isinstance(e2, int):
            if e1 < e2:
                return -1
            elif e1 > e2:
                return 1
        elif isinstance(e1, int):
            if (res := compare([e1], e2)) != 0:
                return res
        elif isinstance(e2, int):
            if (res := compare(e1, [e2])) != 0:
                return res
        else:
            if (res := compare(e1, e2)) != 0:
                return res

    if len(left) < len(right):
        return -1
    elif len(left) > len(right):
        return 1

    return 0


def part1(input_list: list[str]):
    def parse_input(input_list: list[str]):
        result = []

        left = [parse_string(row) for row in input_list[::3]]
        right = [parse_string(row) for row in input_list[1::3]]
        result = list(zip(left, right))

        return result

    pairs = parse_input(input_list)

    result = []
    for left, right in pairs:
        res = compare(left, right)
        result.append(res)

    indices = [i + 1 for i, res in enumerate(result) if res <= 0]
    return sum(indices)


def part2(input_list: list[str]):
    def parse_input(input_list: list[str]):
        result = [parse_string(row) for row in input_list if row]
        return result

    values = parse_input(input_list)
    values.extend([[[2]], [[6]]])
    sorted_vals = sorted(values, key=cmp_to_key(compare))
    idx1 = sorted_vals.index([[2]]) + 1
    idx2 = sorted_vals.index([[6]]) + 1
    return idx1 * idx2


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.read().splitlines()

    result = part1(input_list)
    ic("Part 1", result)

    result = part2(input_list)
    ic("Part 2", result)
