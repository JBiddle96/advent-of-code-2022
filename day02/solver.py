OPPONENT_MAP = {"A": 0, "B": 1, "C": 2}


def part1(input_list):
    CHOICE_SCORES = {"X": 1, "Y": 2, "Z": 3}
    MY_MAP = {"X": 0, "Y": 1, "Z": 2}

    def outcome_score(opponent: str, me: str) -> int:
        opp = OPPONENT_MAP[opponent]
        me = MY_MAP[me]
        if opp == me:
            return 3
        if (opp + 1) % 3 == me:
            return 6
        return 0

    total_score = 0
    for line in input_list:
        opp, me = line.rstrip().split(" ")
        total_score += CHOICE_SCORES[me] + outcome_score(opp, me)

    print("Part 1: ", total_score)


def part2(input_list):
    INVERSE_MAP = {0: "A", 1: "B", 2: "C"}
    CHOICE_SCORES = {"A": 1, "B": 2, "C": 3}
    OUTCOME_SCORES = {"X": 0, "Y": 3, "Z": 6}

    def choice_score(opponent: str, result: str):
        opp = OPPONENT_MAP[opponent]
        if result == "X":
            choice = INVERSE_MAP[(opp - 1) % 3]
            return CHOICE_SCORES[choice]
        elif result == "Y":
            return CHOICE_SCORES[opponent]
        else:
            choice = INVERSE_MAP[(opp + 1) % 3]
            return CHOICE_SCORES[choice]

    total_score = 0
    for line in input_list:
        opp, result = line.rstrip().split(" ")
        total_score += choice_score(opp, result) + OUTCOME_SCORES[result]

    print("Part 2: ", total_score)


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.readlines()

    part1(input_list)
    part2(input_list)
