from string import ascii_letters

PRIORITIES = {letter: i + 1 for i, letter in enumerate(ascii_letters)}


def part1(input_list):
    rucksacks = []
    for line in input_list:
        line = line.rstrip()
        comp_len = int(len(line) / 2)
        rucksacks.append((set(line[:comp_len]), set(line[comp_len:])))

    overlaps = [next(iter(u.intersection(v))) for u, v in rucksacks]
    priorities = [PRIORITIES[o] for o in overlaps]

    print("Part 1: ", sum(priorities))


def part2(input_list):
    groups = []
    for i, line in enumerate(input_list):
        if i % 3 == 0:
            groups.append([])

        groups[-1].append(set(line.rstrip()))

    overlaps = [a.intersection(b, c) for a, b, c in groups]
    priorities = [PRIORITIES[next(iter(o))] for o in overlaps]

    print("Part 2: ", sum(priorities))


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.readlines()

    part1(input_list)
    part2(input_list)
