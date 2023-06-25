from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable, Optional


class Tree:
    class Node:
        def __init__(self, name, parent: Optional[Tree.Node] = None, data=None) -> None:
            data = defaultdict(lambda: 0) if data is None else data
            self.name = name
            self.data: dict = data
            self.children: dict[Any, Tree.Node] = {}
            self.parent = parent

        def _add_child(self, name, data=None) -> Tree.Node:
            existing_child = self.children.get(name)
            if existing_child is None:
                child = Tree.Node(name, parent=self, data=data)
                self.children[name] = child
                return child
            else:
                return existing_child

    def __init__(self, root_name, root_data=None):
        self.root = Tree.Node(root_name, root_data)
        self.nodes: set[Tree.Node] = {self.root}

    def __getitem__(self, item):
        return {node for node in self if node.name == item}

    @property
    def leaf_nodes(self) -> set[Node]:
        return {node for node in self if not node.children}

    def __iter__(self):
        return iter(self.nodes)

    def add_child(self, parent: Node, name, data=None) -> Node:
        child = parent._add_child(name, data=data)
        self.nodes.add(child)
        return child


def process_ls(directory: Tree, location: Tree.Node, output: str):
    if not output:
        return
    if output.startswith("dir"):
        new_dir = output[4:]
        directory.add_child(location, new_dir)
    else:
        size, _ = output.split(" ")
        size = int(size)
        location.data["size"] += size


def process_cd(directory: Tree, location: Tree.Node, new_dir):
    if new_dir == "..":
        if location.parent is not None:
            return location.parent
        else:
            return location
    location = directory.add_child(location, new_dir)
    return location


def calculate_sizes(directory: Tree) -> list[tuple[Any, int]]:
    update_sizes([directory.root])
    sizes = [(node.name, node.data["size"]) for node in directory]
    return sizes


def update_sizes(roots: Iterable[Tree.Node]):
    for root in roots:
        children = set(root.children.values())
        update_sizes(children)
        root.data["size"] = root.data["size"] + sum(c.data["size"] for c in children)


def part1(input_list: list[str]):
    directory = Tree("/")
    loc = directory.root

    for line in input_list[1:]:
        if line.startswith("$"):
            command = line[2:]

            if command.startswith("cd"):
                new_dir = command[3:]
                loc = process_cd(directory, loc, new_dir)

        else:
            process_ls(directory, loc, line)

    sizes = calculate_sizes(directory)

    cutoff = 100000
    sizes = [(d, s) for d, s in sizes if s <= cutoff]
    print("Part 1:", sum([s for _, s in sizes]))
    return directory


def part2(input_list: list[str]):
    directory = Tree("/")
    loc = directory.root

    for line in input_list[1:]:
        if line.startswith("$"):
            command = line[2:]

            if command.startswith("cd"):
                new_dir = command[3:]
                loc = process_cd(directory, loc, new_dir)

        else:
            process_ls(directory, loc, line)

    sizes = calculate_sizes(directory)

    fs_size = 70000000
    required_space = 30000000
    used_space = directory.root.data["size"]
    to_free = used_space - (fs_size - required_space)

    sizes = sorted(sizes, key=lambda elem: elem[1])

    result = 0
    for node, size in sizes:
        if size > to_free:
            result = size
            break
    print("Part 2:", result)
    return directory


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        input_list = f.read().splitlines()

    part1(input_list)
    directory = part2(input_list)
