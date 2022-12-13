from dataclasses import dataclass
from math import prod
import sys


@dataclass
class Monkey:
    id: int
    items: [int, ...]
    op_str: str
    test_div: int
    test_true: int
    test_false: int
    inspect: int = 0


def monkey_parser(text_lines):
    monkey_list = []
    _lines = [line for line in text_lines if line]
    for i in range(0, len(_lines), 6):
        monkey_lines = _lines[i : i + 6]

        monkey_obj = _monkey_parser(monkey_lines)
        monkey_list.append(monkey_obj)

    return monkey_list


def _monkey_parser(monkey_lines):
    assert monkey_lines[0].startswith("Monkey")
    _, monkey_id_str = monkey_lines[0].split("Monkey ")

    assert monkey_lines[1].startswith("Starting items:")
    _, items_str = monkey_lines[1].split("Starting items:")
    items = [int(_i) for _i in items_str.split(", ")]

    assert monkey_lines[2].startswith("Operation:")
    _, op_str = monkey_lines[2].split("Operation: new = ")

    assert monkey_lines[3].startswith("Test: divisible by")
    _, test_div_str = monkey_lines[3].split("Test: divisible by")

    assert monkey_lines[4].startswith("If true: throw to monkey")
    _, true_str = monkey_lines[4].split("If true: throw to monkey")

    assert monkey_lines[5].startswith("If false: throw to monkey")
    _, false_str = monkey_lines[5].split("If false: throw to monkey")

    return Monkey(
        id=int(monkey_id_str.strip(":")),
        items=items,
        op_str=op_str,
        test_div=int(test_div_str),
        test_true=int(true_str),
        test_false=int(false_str),
    )


def monkey_round(monkeys, modulo):
    for monkey_id in range(len(monkeys)):
        monkeys = update_monkey(monkey_id, monkeys, modulo)

    return monkeys


def update_monkey(monkey_id, monkeys, modulo):
    monkey = monkeys[monkey_id]

    items = []
    items[:] = monkey.items
    monkey.items = []

    # 'old' is used in eval
    for old in items:  # pylint: disable=unused-variable
        new = eval(monkey.op_str)

        bored = new % modulo

        if bored % monkey.test_div:
            monkeys[monkey.test_false].items.append(bored)
        else:
            monkeys[monkey.test_true].items.append(bored)

        monkeys[monkey_id].inspect += 1

    assert len(monkey.items) == 0, monkey

    return monkeys


def main():
    with open(sys.argv[1], encoding="UTF-8") as fh:
        lines = [line.strip() for line in fh.readlines()]

    monkey_lookup = {monkey.id: monkey for monkey in monkey_parser(lines)}

    modulo = prod(monkey.test_div for monkey in monkey_lookup.values())

    for round_ in range(1, 10001):
        monkey_lookup = monkey_round(monkey_lookup, modulo)

        if round_ in {1, 20, 10000}:
            print(f"round {round_}")
            for monkey in monkey_lookup.values():
                print(f"monkey {monkey.id} {monkey.inspect}")

    inspects = sorted([m.inspect for m in monkey_lookup.values()])
    product = inspects[-2] * inspects[-1]

    print(f"{product} should be 10605 in test")
    print(f"{product} should be 2713310158 in p2 test")


if __name__ == "__main__":
    main()
