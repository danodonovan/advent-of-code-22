from collections import defaultdict, namedtuple
import json
import re
import string
import sys


def _build_stacks(lines):

    stacks = defaultdict(list)

    index_line = next(filter(lambda line: "[" not in line, lines))
    index_values = [ix for ix in index_line.split(" ") if ix]
    index_index = [index_line.find(ix) for ix in index_values]
    index_lookup = {a: int(b) for a, b in zip(index_index, index_values)}

    for line in lines:
        for char_index, char in enumerate(line):
            if char in string.ascii_uppercase:
                index = index_lookup[char_index]
                stacks[int(index)].append(char)

    return stacks


Move = namedtuple("Move", ("count", "stack_0", "stack_1"))


def _build_moves(lines):
    move_re = re.compile(r"^move (\d*) from (\d*) to (\d*)$")

    moves = []
    for line in lines:
        count, stack_0, stack_1 = map(int, move_re.match(line).groups())
        moves.append(Move(count=count, stack_0=stack_0, stack_1=stack_1))

    return moves


def _update_stacks(stacks, move):
    crates = [stacks[move.stack_0].pop(0) for _ in range(move.count)]
    for item in crates:
        stacks[move.stack_1].insert(0, item)
    return stacks


def _update_stacks_part_2(stacks, move):
    crates = [stacks[move.stack_0].pop(0) for _ in range(move.count)]
    for item in crates[::-1]:
        stacks[move.stack_1].insert(0, item)
    return stacks


def print_stacks(stacks):

    copy_stacks = json.loads(json.dumps(stacks))

    def _get(row):
        try:
            return f"[{row.pop(-1)}]"
        except IndexError:
            return "   "

    keys = sorted(copy_stacks.keys())
    lines = ["".join(f" {index}  " for index in keys)]

    max_stack = max(len(values) for values in copy_stacks.values())
    for _ in range(max_stack):
        single_line = []
        for key in keys:
            value = _get(copy_stacks[key])
            single_line.append(f"{value} ")
        lines.append("".join(single_line))

    print("\n".join(lines[::-1]) + "\n")


def _print_stacks_top(stacks):
    copy_stacks = json.loads(json.dumps(stacks))
    keys = sorted(copy_stacks.keys())

    def _top_get(row):
        try:
            return row.pop(0)
        except IndexError:
            return ""

    top = "".join(_top_get(copy_stacks[key]) for key in keys)
    print(f"top: {top}")


if __name__ == "__main__":
    with open(sys.argv[1], encoding="UTF-8") as fh:
        _lines = []
        while (_line := fh.readline()) != "\n":
            _lines.append(_line.strip("\n"))

        _stacks = _build_stacks(_lines)

        _moves = map(lambda _line_: _line_.strip(), fh.readlines())

    print_stacks(_stacks)
    _moves_ = _build_moves(_moves)

    for i, _move in enumerate(_moves_):
        print(i, _move, "\n")
        _stacks = _update_stacks_part_2(_stacks, _move)
        print_stacks(_stacks)

    _print_stacks_top(_stacks)

    print("in test p1 final top stack is CMZ")
    print("in test p2 final top stack is MCD")
