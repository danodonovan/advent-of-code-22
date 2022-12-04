import string
import sys

with open(sys.argv[1]) as fh:
    lines = [line.strip() for line in fh.readlines()]


def _double_pack(line):
    a = line[: len(line) // 2]
    b = line[len(line) // 2 :]

    return list(set(a) & set(b))[0]


priority = {
    value: index
    for index, value in enumerate(
        string.ascii_lowercase + string.ascii_uppercase, start=1
    )
}


print(f"sum: {sum(priority[_double_pack(line)] for line in lines)}")
print("should be 157 in test")


def _triple_bags(*lines):
    l1, l2, l3 = lines
    return list(set(l1) & set(l2) & set(l3))[0]


sum_vals = sum(
    [priority[_triple_bags(*lines[i : i + 3])] for i in range(0, len(lines), 3)]
)

print(sum_vals, " = should be 70 in test")
