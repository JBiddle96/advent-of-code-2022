from itertools import product

import numpy as np


def count_visible(arr):
    visible = set()
    largest = -1
    for j, elem in enumerate(arr):
        if elem > largest:
            visible.add(j)
            largest = elem
    return visible


def check_visible(grid: np.ndarray):
    visible = set()
    n_rows, n_cols = grid.shape
    for i, row in enumerate(grid):
        from_right = count_visible(row)
        from_left = count_visible(reversed(row))
        visible.update({(i, j) for j in from_right})
        visible.update({(i, n_cols - j - 1) for j in from_left})

    for j, col in enumerate(grid.T):
        from_top = count_visible(col)
        from_bottom = count_visible(reversed(col))
        visible.update({(i, j) for i in from_top})
        visible.update({(n_rows - i - 1, j) for i in from_bottom})

    return visible


def part1(trees: np.ndarray):
    visible = check_visible(trees)
    print("Part 1:", len(visible))


def calc_score(height, candidates):
    score = 0
    for elem in candidates:
        score += 1
        if elem >= height:
            break
    return score


def scenic_score(grid: np.ndarray, coords):
    x, y = coords
    n_rows, n_cols = grid.shape
    this_height = grid[x, y]

    row = grid[x, :]
    if y < n_cols - 1:
        right_score = calc_score(this_height, row[y + 1 :])
    else:
        right_score = 0

    if y > 0:
        left_score = calc_score(this_height, reversed(row[:y]))
    else:
        left_score = 0

    col = grid[:, y]
    if x < n_rows - 1:
        bottom_score = calc_score(this_height, col[x + 1 :])
    else:
        bottom_score = 0

    if x > 0:
        top_score = calc_score(this_height, reversed(col[:x]))
    else:
        top_score = 0

    score = right_score * left_score * bottom_score * top_score
    return score


def part2(trees: np.ndarray):
    n_rows, n_cols = trees.shape
    scores = []
    for coord in product(range(n_rows), range(n_cols)):
        score = scenic_score(trees, coord)
        scores.append(score)

    print("Part 2:", max(scores))


if __name__ == "__main__":
    input_file = "input.txt"
    # input_file = "small_input.txt"
    with open(input_file, "r") as f:
        input_list = f.read().splitlines()

    n_rows = len(input_list)
    n_cols = len(input_list[0])
    trees = np.zeros((n_rows, n_cols), dtype=int)
    for i, line in enumerate(input_list):
        trees[i, :] = [int(char) for char in line]

    part1(trees)
    part2(trees)
