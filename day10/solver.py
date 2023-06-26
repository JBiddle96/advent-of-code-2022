import abc
from enum import Enum


class Ops(str, Enum):
    NOOP = "noop"
    ADDX = "addx"


class Instruction(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def duration(self):
        raise NotImplementedError

    @abc.abstractmethod
    def run(self, val) -> int:
        raise NotImplementedError


class Addx(Instruction):
    def __init__(self, add) -> None:
        self.add = add

    @property
    def duration(self):
        return 2

    def run(self, val):
        return val + self.add


class NoOp(Instruction):
    @property
    def duration(self):
        return 1

    def run(self, val):
        return val


class Processor:
    def __init__(self, instructions: list[Instruction]) -> None:
        self.cycle = 1
        self.register = 1
        self.instructions = instructions if instructions is not None else []

    def run(self, record_cycles=None) -> list[int]:
        record_cycles = [] if record_cycles is None else [r for r in record_cycles]
        recorded_values = []
        instruction = NoOp()
        remaining_duration = 0
        while True:
            if remaining_duration == 0:
                self.register = instruction.run(self.register)
                instruction = self.instructions.pop(0)
                remaining_duration = instruction.duration

            remaining_duration -= 1
            if record_cycles and self.cycle == record_cycles[0]:
                recorded_values.append(self.register)
                record_cycles.pop(0)

            if not self.instructions:
                break

            self.cycle += 1
        return recorded_values


def part1(input_list: list[str]):
    target_cycles = [20 + i * 40 for i in range(6)]
    signal_strength = []
    instructions = []
    for line in input_list:
        if line.startswith(Ops.NOOP):
            instructions.append(NoOp())
        if line.startswith(Ops.ADDX):
            _, val = line.split()
            instructions.append(Addx(int(val)))

    processor = Processor(instructions)
    recorded_values = processor.run(target_cycles)
    signal_strength = [
        cycle * record for cycle, record in zip(target_cycles, recorded_values)
    ]

    print("Part 1:", sum(signal_strength))


def part2(input_list: list[str]):
    crt_width, crt_height = 40, 6
    target_cycles = list(range(1, crt_width * crt_height + 1))
    crt = [["." for _ in range(crt_width)] for _ in range(crt_height)]

    instructions = []
    for line in input_list:
        if line.startswith(Ops.NOOP):
            instructions.append(NoOp())
        if line.startswith(Ops.ADDX):
            _, val = line.split()
            instructions.append(Addx(int(val)))

    processor = Processor(instructions)
    sprite_positions = processor.run(target_cycles)

    for i, sprite_pos in enumerate(sprite_positions):
        y = int(i / crt_width)
        x = i % crt_width

        if abs(sprite_pos - x) <= 1:
            crt[y][x] = "#"

    final_str = "\n".join(" ".join(row) for row in crt)
    print("Part 2:")
    print(final_str)


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.read().splitlines()

    part1(input_list)
    part2(input_list)
