import sys
import re

line_re = re.compile(r"^(\d*)\-(\d*)\,(\d*)\-(\d*)$")

with open(sys.argv[1], encoding="UTF-8") as fh:
    lines = [line.strip() for line in fh.readlines()]



def range_check(line, part_1=False):
    a0, a1, b0, b1 = map(int, line_re.match(line).groups())

    a_range = list(range(a0, a1 + 1))
    b_range = list(range(b0, b1 + 1))

    overlap = set(a_range) & set(b_range)


    # part 1
    if part_1:
        return bool(overlap and len(overlap) == min(len(a_range), len(b_range)))

    # part 2
    return bool(overlap)


overlaps = sum(map(range_check, lines))

print(f'overlaps: {overlaps} .. should be 2 in test p1, 4 in test p2')
