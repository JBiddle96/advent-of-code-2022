from __future__ import annotations

from functools import reduce
from typing import Callable

from ttp import ttp

ttp_template = """\
Monkey {{monkey_id|to_int}}:
  Starting items: {{starting_items|ORPHRASE|split(", ")}}
  Operation: new = old {{operation|PHRASE}}
  Test: divisible by {{divisible_by|to_int}}
    If true: throw to monkey {{true_dest|to_int}}
    If false: throw to monkey {{false_dest|to_int}}
"""


class Monkey:
    def __init__(
        self,
        monkey_id: int,
        starting_items: list[int],
        operation: Callable[[int], int],
        test_divisor: int,
        true_dest: int,
        false_dest: int,
        worry_divisor: int = 1,
        worry_reducer: int = 1,
    ) -> None:
        self.id = monkey_id
        self.items = starting_items
        self.operation = operation
        self.test_divisor = test_divisor
        self.true_dest = true_dest
        self.false_dest = false_dest
        self.worry_divisor = worry_divisor
        self.worry_reducer = worry_reducer

    def take_turn(self, other_monkeys: dict[int, Monkey]) -> int:
        n_inspections = len(self.items)
        for item in self.items:
            target = self.operation(item)
            target = int(target / self.worry_divisor)
            if target % self.test_divisor == 0:
                target = target % self.worry_reducer
                self.throw_item(target, other_monkeys[self.true_dest])
            else:
                target = target % self.worry_reducer
                self.throw_item(target, other_monkeys[self.false_dest])
        self.items = []
        return n_inspections

    def throw_item(self, item: int, target_monkey: Monkey):
        target_monkey.items.append(item)


def load_monkeys(input: str):
    parser = ttp(data=input, template=ttp_template)  # type: ignore
    parser.parse()
    results: list[dict] = parser.result()[0][0]
    monkeys = []
    for monkey_data in results:  # type: ignore
        id = monkey_data["monkey_id"]
        starting_items = [int(item) for item in monkey_data["starting_items"]]
        op, val = monkey_data["operation"].split()
        operation: Callable[[int], int] = eval(f"lambda old: old {op} {val}")
        test_divisor = monkey_data["divisible_by"]
        true_dest = monkey_data["true_dest"]
        false_dest = monkey_data["false_dest"]
        monkey = Monkey(
            id,
            starting_items,
            operation,
            test_divisor,
            true_dest,
            false_dest,
        )
        monkeys.append(monkey)
    return monkeys


def part1(monkeys: list[Monkey]):
    n_rounds = 20
    for monkey in monkeys:
        monkey.worry_divisor = 3
    monkey_dict = {monkey.id: monkey for monkey in monkeys}
    inspection_dict = {monkey.id: 0 for monkey in monkeys}
    for i in range(n_rounds):
        for monkey in monkeys:
            inspection_dict[monkey.id] += monkey.take_turn(monkey_dict)

    n_inspections = sorted(list(inspection_dict.values()), reverse=True)
    print("Part 1:", n_inspections[0] * n_inspections[1])


def part2(monkeys: list[Monkey]):
    n_rounds = 10000
    monkey_dict = {monkey.id: monkey for monkey in monkeys}
    inspection_dict = {monkey.id: 0 for monkey in monkeys}
    divisor = reduce((lambda x, y: x * y), [m.test_divisor for m in monkeys])
    for monkey in monkeys:
        monkey.worry_reducer = divisor
    for i in range(n_rounds):
        for monkey in monkeys:
            inspection_dict[monkey.id] += monkey.take_turn(monkey_dict)

    n_inspections = sorted(list(inspection_dict.values()), reverse=True)
    print("Part 2:", n_inspections[0] * n_inspections[1])


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input = f.read()

    part1(load_monkeys(input))
    part2(load_monkeys(input))
