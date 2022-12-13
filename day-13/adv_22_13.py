from dataclasses import dataclass
import sys


def _read_packets(filename):
    with open(filename, encoding="UTF-8") as fh:
        return [line.strip() for line in fh.readlines()]


def main():
    lines = _read_packets(sys.argv[1])
    packets = [eval(line) for line in lines if line]
    left_packets = packets[::2]
    right_packets = packets[1::2]

    assert len(left_packets) == len(right_packets)

    indices = []
    for index, (left, right) in enumerate(zip(left_packets, right_packets), start=1):
        # print(f"**index** {index}")
        path = []
        compare(left, right, path)
        if path[0]:
            # print(f"true! {index}\n{left}\n{right}\n")
            indices.append(index)
        # else:
        #     print(f"false! {index}\n{left}\n{right}\n")

    print(f"\nindices: {indices}")
    print("in test should be [1, 2, 4, 6]")
    print(f"{sum(indices)} : in test should be 13")
    print("p1 3466 is too low, 4964 is too high")

    # part 2 - sort
    packets.append([[2]])
    packets.append([[6]])

    packet_objs = [Packet(data=packet) for packet in packets]

    sorted_packets = [packet.data for packet in sorted(packet_objs)]

    sep_2_index = next(
        i for i, pack in enumerate(sorted_packets, start=1) if pack == [[2]]
    )
    sep_6_index = next(
        i for i, pack in enumerate(sorted_packets, start=1) if pack == [[6]]
    )

    print(f"product: {sep_2_index} * {sep_6_index} = {sep_2_index * sep_6_index}")
    print("in test this is 140")


@dataclass
class Packet:
    data: list

    def __lt__(self, other):
        path = []
        compare(self.data, other.data, path)
        return path[0]


def compare(left, right, path):

    assert isinstance(left, list), f"left not list: {left}"
    assert isinstance(right, list), f"right not list: {right}"

    max_len = max(len(left), len(right))

    for i in range(max_len):
        try:
            l = left[i]
        except IndexError:
            # print("True: left list ran out")
            path.append(True)
            break

        try:
            r = right[i]
        except IndexError:
            # print("False: right list ran out")
            path.append(False)
            break

        if isinstance(l, int) and isinstance(r, int):
            # print(f"{l} vs {r}")
            if l < r:
                # print("True: left int smaller")
                path.append(True)
                break

            if l > r:
                # print("False: right int smaller")
                path.append(False)
                break

        elif isinstance(l, list) and isinstance(r, list):
            compare(l, r, path)
        elif isinstance(l, list) and isinstance(r, int):
            compare(l, [r], path)
        elif isinstance(l, int) and isinstance(r, list):
            compare([l], r, path)
        else:
            raise Exception("unreachable code")


if __name__ == "__main__":
    main()
