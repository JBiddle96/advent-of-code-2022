import re


def part1(input_list: list):
    def move(data, src, dest, count):
        for i in range(count):
            data[dest].append(data[src].pop())

    n_stacks = int((len(input_list[0]) + 1) / 4)
    stacks = {i + 1: [] for i in range(n_stacks)}

    split_idx = input_list.index("")
    stack_data = input_list[: split_idx - 1]
    move_data = input_list[split_idx + 1 :]

    for line in stack_data:
        idx = 0
        width = 3
        for key, data in stacks.items():
            elem = line[idx : idx + width]
            if not elem.isspace():
                data.append(elem.strip("[]"))

            idx += 4

    stacks = {key: list(reversed(data)) for key, data in stacks.items()}

    for line in move_data:
        pattern = re.compile(r"^move (\d+) from (\d+) to (\d+)$")
        match = re.match(pattern, line)
        if match:
            count, src, dest = match.group(1, 2, 3)
            move(stacks, int(src), int(dest), int(count))

    final_str = ""
    for data in stacks.values():
        final_str += data[-1]

    print("Part 1:", final_str)


def part2(input_list: list):
    def move(data, src, dest, count):
        to_move = data[src][-count:]
        data[src] = [d for d in data[src][:-count]]
        data[dest] = data[dest] + to_move

    n_stacks = int((len(input_list[0]) + 1) / 4)
    stacks = {i + 1: [] for i in range(n_stacks)}

    split_idx = input_list.index("")
    stack_data = input_list[: split_idx - 1]
    move_data = input_list[split_idx + 1 :]

    for line in stack_data:
        idx = 0
        width = 3
        for key, data in stacks.items():
            elem = line[idx : idx + width]
            if not elem.isspace():
                data.append(elem.strip("[]"))

            idx += 4

    stacks = {key: list(reversed(data)) for key, data in stacks.items()}

    for line in move_data:
        pattern = re.compile(r"^move (\d+) from (\d+) to (\d+)$")
        match = re.match(pattern, line)
        if match:
            count, src, dest = match.group(1, 2, 3)
            move(stacks, int(src), int(dest), int(count))

    print(stacks)

    final_str = ""
    for data in stacks.values():
        final_str += data[-1]

    print("Part 2:", final_str)


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.read().splitlines()

    part1(input_list)
    part2(input_list)
