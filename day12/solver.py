from itertools import product
from string import ascii_lowercase

import networkx as nx
import numpy as np

elevation_dict = {letter: i for i, letter in enumerate(ascii_lowercase)}
START_VAL = 0
END_VAL = len(ascii_lowercase) - 1
elevation_dict["S"] = START_VAL
elevation_dict["E"] = END_VAL


def load_elevation(input_list: list[str]):
    if not input_list:
        return np.empty((0, 0))
    n_rows = len(input_list)
    n_cols = len(input_list[0])

    start, end = None, None
    elevation_map = np.zeros((n_rows, n_cols), dtype=np.int8)
    for i, row in enumerate(input_list):
        for j, letter in enumerate(row):
            elevation_map[i, j] = elevation_dict[letter]
            if letter == "S":
                start = (i, j)
            if letter == "E":
                end = (i, j)

    return elevation_map, start, end


def elevation_to_dg(elevation_map: np.ndarray) -> nx.DiGraph:
    n_rows, n_cols = elevation_map.shape
    g = nx.DiGraph()

    for i, j in product(range(n_rows), range(n_cols)):
        g.add_node((i, j))
        this_elevation = elevation_map[i, j]
        nbrs = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        nbrs = [
            (x, y) for x, y in nbrs if x >= 0 and y >= 0 and x < n_rows and y < n_cols
        ]
        for ni, nj in nbrs:
            nbr_elevation = elevation_map[ni, nj]
            if nbr_elevation - this_elevation <= 1:
                g.add_edge((i, j), (ni, nj))

    return g


def part1(input_list: list[str]):
    elevation_map, start, end = load_elevation(input_list)
    elevation_graph = elevation_to_dg(elevation_map)

    shortest_path = nx.dijkstra_path(elevation_graph, start, end)
    n_moves = len(shortest_path) - 1
    print("Part1:", n_moves)


def part2(input_list: list[str]):
    elevation_map, _, end = load_elevation(input_list)
    elevation_graph = elevation_to_dg(elevation_map)

    possible_starts = tuple(zip(*np.where(elevation_map == START_VAL)))

    path_lengths = []
    for start in possible_starts:
        try:
            shortest_path = nx.dijkstra_path(elevation_graph, start, end)
        except nx.NetworkXNoPath:
            continue

        n_moves = len(shortest_path) - 1
        path_lengths.append(n_moves)

    min_moves = min(path_lengths)
    print("Part2:", min_moves)


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.read().splitlines()

    part1(input_list)
    part2(input_list)
