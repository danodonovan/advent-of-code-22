import sys
import re

line_re = re.compile(r"^(\d*)\-(\d*)\,(\d*)\-(\d*)$")

with open(sys.argv[1]) as fh:
    lines = [line.strip() for line in fh.readlines()]



def range_check(line, part_1=False):
    a0, a1, b0, b1 = match = line_re.match(line).groups()

    a_range = list(range(int(a0), int(a1) + 1))
    b_range = list(range(int(b0), int(b1) + 1))

    overlap = set(a_range) & set(b_range)


    # part 1
    if part_1: 
        if overlap and len(overlap) == min(len(a_range), len(b_range)):
            return True
        else:
            return False

    # part 2
    if not part_1:
        return bool(overlap)


overlaps = sum(map(range_check, lines))

print(f'overlaps: {overlaps} .. should be 2 in test p1, 4 in test p2')

