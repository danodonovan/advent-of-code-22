import sys
import numpy as np


def _read(filename):
    with open(filename, encoding="UTF-8") as fh:
        lines = fh.readlines()

    trees = [[int(tree) for tree in line.strip()] for line in lines]
    ncols = len(trees[0])

    for row in trees:
        assert len(row) == ncols

    return np.array(trees)


def _count_visible_2(trees):
    nrows = len(trees)
    ncols = len(trees[0])
    outside_visible = nrows * 2 + (ncols - 2) * 2

    count = 0
    for (row, col), tree in np.ndenumerate(trees):

        if row in (0, nrows - 1) or col in (0, ncols - 1):
            continue

        row_left = trees[row, :col]
        if np.all(row_left < tree):
            count += 1
            continue

        row_right = trees[row, col + 1 :]
        if np.all(row_right < tree):
            count += 1
            continue

        col_up = trees[:row, col]
        if np.all(col_up < tree):
            count += 1
            continue

        col_down = trees[row + 1 :, col]
        if np.all(col_down < tree):
            count += 1
            continue

    return count + outside_visible


def _scenic_scores(trees):
    scores = []
    for (row, col), tree in np.ndenumerate(trees):

        if row == 0 or col == 0:
            continue

        look_up = trees[:row, col][::-1]
        look_left = trees[row, :col][::-1]
        look_right = trees[row, col + 1 :]
        look_down = trees[row + 1 :, col]

        def _count(view, tree):
            i, count = 0, 0
            while i < len(view):
                count += 1

                if view[i] >= tree:
                    break

                i += 1

            return count

        _score = (
            _count(look_left, tree)
            * _count(look_right, tree)
            * _count(look_up, tree)
            * _count(look_down, tree)
        )

        scores.append(_score)

    return max(scores)


if __name__ == "__main__":
    trees_ = _read(sys.argv[1])

    print(trees_)
    print("")

    # part 1
    visible = _count_visible_2(trees_)
    print(f"visible {visible}: should be 21 in test")

    # part 2
    scenic = _scenic_scores(trees_)
    print(f"scenic {scenic}: should be 8 in test")
