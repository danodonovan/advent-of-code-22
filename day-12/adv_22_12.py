from dataclasses import dataclass, field
import string
import sys

import numpy as np


SCORES = {
    char: score
    for char, score in zip(string.ascii_lowercase, range(len(string.ascii_lowercase)))
}
SCORES["S"] = 0
SCORES["E"] = len(string.ascii_lowercase)


@dataclass
class Loc:
    x: int
    y: int
    signal: str
    next: list["Loc", ...] = field(default_factory=list)

    @property
    def xy(self) -> (int, int):
        return self.x, self.y

    def steppable(self, prev_loc: "Loc") -> bool:
        return SCORES[self.signal] - SCORES[prev_loc.signal] - 1 <= 0

    def __repr__(self):
        return self.signal


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

    grid = np.array([[char for char in line.strip()] for line in lines])

    return grid


def sub(grid, x, y, xsize, ysize):
    sx, sy = grid.shape
    xmsize = max(x - xsize + 1, 0)
    xpsize = min(x + xsize, sx)
    ymsize = max(y - ysize + 1, 0)
    ypsize = min(y + ysize, sy)

    return grid[xmsize:xpsize, ymsize:ypsize]


def main():
    grid = _read(sys.argv[1])
    x_size, y_size = grid.shape
    pure_grid = _read_grid(sys.argv[1])
    print(np.array(list(map(str, range(grid.shape[1])))))
    print(pure_grid)

    # start and end
    (x0,), (y0,) = np.where(pure_grid == "S")
    # (xn,), (yn,) = np.where(pure_grid == 'E')

    # print(sub(grid, x0, y0, 2, 2))
    # print(sub(grid, x0 + 2, y0 + 4, 2, 2))

    # build tree
    for x in range(x_size):
        for y in range(y_size):
            loc = grid[x, y]

            nbors = sub(grid, x, y, 2, 2)

            loc.next = [
                nbor
                for nbor in nbors.flatten()
                if nbor.steppable(loc) and loc.xy != nbor.xy
            ]

    # walk tree until we reach E
    path = []
    start = grid[x0, y0]
    walk_path(start, path)
    print(path)

    # import IPython; IPython.embed(using=False, header='')


def walk_path(location, path):
    if location.signal == "E":
        return path

    for next_location in location.next:
        if next_location in path:
            continue
        path.append(next_location)
        return walk_path(next_location, path)



if __name__ == "__main__":
    main()
