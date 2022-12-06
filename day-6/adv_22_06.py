import sys


def subroutine(data, packet_size=4):

    stack = []
    count = 0
    data = iter(data)

    while True:
        try:
            char = next(data)
        except StopIteration:
            break

        if len(stack) >= packet_size:
            stack.pop(0)

        stack.append(char)
        count += 1

        if len(set(stack)) == packet_size:
            print(f"found: at {count} : {''.join(stack)}")
            break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # data_ = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
        # data_ = "bvwbjplbgvbhsrlpgdmjqwftvncz"
        data_ = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

    else:
        with open(sys.argv[1], encoding="UTF-8") as fh:
            data_ = fh.readline().strip()

    print(f"searching: {data_}")

    subroutine(data_, packet_size=14)
