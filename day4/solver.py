def part1(input_list):
    total_count = 0
    for line in input_list:
        r1, r2 = line.split(",")

        l1, u1 = r1.split("-")
        l1, u1 = int(l1), int(u1)
        s1 = set(range(l1, u1 + 1))

        l2, u2 = r2.split("-")
        l2, u2 = int(l2), int(u2)
        s2 = set(range(l2, u2 + 1))

        intersect = s1.intersection(s2)
        if intersect == s1 or intersect == s2:
            total_count += 1

    print("Part 1: ", total_count)


def part2(input_list):
    total_count = 0
    for line in input_list:
        r1, r2 = line.split(",")

        l1, u1 = r1.split("-")
        l1, u1 = int(l1), int(u1)
        s1 = set(range(l1, u1 + 1))

        l2, u2 = r2.split("-")
        l2, u2 = int(l2), int(u2)
        s2 = set(range(l2, u2 + 1))

        intersect = s1.intersection(s2)
        if intersect:
            total_count += 1

    print("Part 2: ", total_count)


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.read().splitlines()

    part1(input_list)
    part2(input_list)
