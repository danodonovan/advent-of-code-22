import sys

# part one

raw_data = sys.argv[1]

elf_cals = [sum(map(int, chunk.split("\n"))) for chunk in raw_data.split("\n\n")]

print(f"max cals: {max(elf_cals)}")
print("in test, this should be 24000")

# part two
sorted_cals = sorted(elf_cals)

print(f"max 3 elf cals: {sum(sorted_cals[-3:])}")
print("in test, this should be 45000")
