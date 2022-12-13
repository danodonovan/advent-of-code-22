from dataclasses import dataclass
import string
import sys

import numpy as np


SCORES = dict(
    zip(string.ascii_lowercase, range(len(string.ascii_lowercase)))
    )
SCORES["S"] = 0
SCORES["E"] = len(string.ascii_lowercase) - 1


@dataclass
class Loc:
    x: int
    y: int
    signal: str

    @property
    def xy(self) -> (int, int):
        return self.x, self.y

    def steppable(self, prev_loc: "Loc") -> bool:
        return SCORES[self.signal] - SCORES[prev_loc.signal] - 1 <= 0

    def __repr__(self):
        return f"{self.xy}: {self.signal}"


def _read(filename):
    with open(filename, encoding="UTF-8") as fh:
        lines = fh.readlines()

    grid = np.array(
        [
            [Loc(x=x, y=y, signal=char) for x, char in enumerate(line.strip())]
            for y, line in enumerate(lines)
        ]
    )

    return grid


def _read_grid(filename):
    with open(filename, encoding="UTF-8") as fh:
        lines = fh.readlines()

    grid = np.array([list(line.strip()) for line in lines])

    return grid


def sub(grid, x, y):
    if x - 1 >= 0:
        left = grid[x - 1, y]
    else:
        left = None
    if x + 1 < grid.shape[0]:
        right = grid[x + 1, y]
    else:
        right = None

    if y - 1 >= 0:
        up = grid[x, y - 1]
    else:
        up = None
    if y + 1 < grid.shape[1]:
        down = grid[x, y + 1]
    else:
        down = None

    return np.array(list(filter(None, [left, right, up, down])))


def main():
    grid = _read(sys.argv[1])
    pure_grid = _read_grid(sys.argv[1])
    print(np.array(list(map(str, range(grid.shape[1])))))
    print(pure_grid)

    # start and end
    (x0,), (y0,) = np.where(pure_grid == "S")
    (xn,), (yn,) = np.where(pure_grid == "E")

    graph = build_graph(grid)

    x0s, y0s = np.where(pure_grid == "a")

    path_lengths = []
    for x0, y0 in zip(x0s, y0s):
        start = grid[x0, y0]
        end = grid[xn, yn]

        path = shortest_path(graph, start, end)

        if path:
            path_lengths.append(len(path) - 1)


    # print(f"length: {len(path) - 1} - in test should be 31")
    print(f"length: {min(path_lengths)} - in test should be 29")

    # import IPython

    # IPython.embed(using=False, header="")


def build_graph(grid):
    graph = {}
    x_size, y_size = grid.shape
    for x in range(x_size):
        for y in range(y_size):
            loc = grid[x, y]

            nbors = sub(grid, x, y)

            graph[loc.xy] = [
                nbor
                for nbor in nbors.flatten()
                if nbor.steppable(loc) and loc.xy != nbor.xy
            ]

    return graph


def shortest_path(graph, node1, node2):
    path_list = [[node1]]
    path_index = 0

    # To keep track of previously visited nodes
    previous_nodes = {node1.xy}

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = graph[last_node.xy]
        # Search goal node
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if not next_node.xy in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node.xy)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []


if __name__ == "__main__":
    main()
