from __future__ import annotations

from typing import Optional


class Coord:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, coord: Coord) -> Coord:
        return Coord(self.x + coord.x, self.y + coord.y)

    def __sub__(self, coord: Coord) -> Coord:
        return Coord(self.x - coord.x, self.y - coord.y)

    def __str__(self) -> str:
        return str((self.x, self.y))


def move(h_pos: Coord, t_pos: Coord, direction: Optional[str] = None):
    if direction == "R":
        h_move_vec = Coord(1, 0)
    elif direction == "L":
        h_move_vec = Coord(-1, 0)
    elif direction == "U":
        h_move_vec = Coord(0, 1)
    elif direction == "D":
        h_move_vec = Coord(0, -1)
    elif direction is None:
        h_move_vec = Coord(0, 0)
    else:
        raise ValueError(f"Unrecognised direction: {direction}")

    new_h_pos = h_pos + h_move_vec
    diff = new_h_pos - t_pos
    if max((abs(diff.x), abs(diff.y))) > 1:
        move_x = int(diff.x / abs(diff.x)) if diff.x != 0 else 0
        move_y = int(diff.y / abs(diff.y)) if diff.y != 0 else 0
        t_move_vec = Coord(move_x, move_y)
        new_t_pos = t_pos + t_move_vec
    else:
        new_t_pos = t_pos

    return new_h_pos, new_t_pos


def part1(input_list: list[str]):
    h_pos, t_pos = Coord(0, 0), Coord(0, 0)
    t_visited = {(int(0), int(0))}
    for line in input_list:
        direction, count = line.split()
        count = int(count)
        for i in range(count):
            h_pos, t_pos = move(h_pos, t_pos, direction)
            t_visited.add((t_pos.x, t_pos.y))

    print("Part 1:", len(t_visited))


def part2(input_list: list[str]):
    n_segments = 10
    rope = [Coord(0, 0) for i in range(n_segments)]
    t_visited = {(int(0), int(0))}
    for line in input_list:
        direction, count = line.split()
        count = int(count)
        for i in range(count):
            rope[0], rope[1] = move(rope[0], rope[1], direction)
            for i_s in range(n_segments - 1):
                rope[i_s], rope[i_s + 1] = move(rope[i_s], rope[i_s + 1])
            t_visited.add((rope[-1].x, rope[-1].y))

    print("Part 2:", len(t_visited))


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.read().splitlines()

    part1(input_list)
    part2(input_list)
