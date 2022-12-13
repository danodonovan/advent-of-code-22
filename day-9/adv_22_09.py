from dataclasses import dataclass
import math
import sys


def _read_text(filename):
    with open(filename, encoding="UTF-8") as fh:
        return list(
            map(
                lambda pair: (pair[0], int(pair[1])),
                map(lambda line: line.strip().split(" "), fh.readlines()),
            )
        )


@dataclass
class State:
    head: (int, int)
    tail: (int, int)
    tails: [(int, int)]

    @classmethod
    def new(cls):
        return cls((0, 0), (0, 0), [0, 0])

    def __repr__(self):
        return f"State(head={self.head}, tail={self.tail}, tails={len(self.tails)})"


def move(state, direction_):

    p_head = state.head
    x, y = state.head
    if direction_ == "U":
        state.head = (x + 0, y + 1)
    elif direction_ == "R":
        state.head = (x + 1, y + 0)
    elif direction_ == "D":
        state.head = (x + 0, y - 1)
    elif direction_ == "L":
        state.head = (x - 1, y + 0)
    else:
        raise Exception

    state = update_tail(state, p_head)

    return state


def update_tail(state, p_head):

    distance_ = math.sqrt(sum((a - b) ** 2 for a, b in zip(state.head, state.tail)))

    if distance_ < 2.0:
        pass
    else:
        state.tail = p_head
        state.tails.append(state.tail)

    return state


if __name__ == "__main__":
    moves = _read_text(sys.argv[1])
    print(moves)

    s = State.new()
    print("initial", s)

    for direction, distance in moves:
        print(direction, distance)
        for d in range(1, distance + 1):
            s = move(s, direction)
            print("l", s)

    print(len(s.tails))
    print(f"visited: {len(set(s.tails))} - in test this is 13")
