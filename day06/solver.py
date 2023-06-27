def part1(input):
    window_len = 4
    n_windows = len(input) - window_len + 1

    solution = None
    for i in range(n_windows):
        window = input[i : i + window_len]
        if len(window) == len(set(window)):
            solution = i + window_len
            break

    print("Part 1:", solution)


def part2(input):
    window_len = 14
    n_windows = len(input) - window_len + 1

    solution = None
    for i in range(n_windows):
        window = input[i : i + window_len]
        if len(window) == len(set(window)):
            solution = i + window_len
            break

    print("Part 2:", solution)


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input = f.read()

    part1(input)
    part2(input)
