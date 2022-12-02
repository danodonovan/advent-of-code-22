import sys

with open(sys.argv[1], "r") as fh:
    text = fh.readlines()

lookup = {
    "A": "Rock",
    "X": "Rock",
    "B": "Paper",
    "Y": "Paper",
    "C": "Scissors",
    "Z": "Scissors",
}

score = {"Paper": 2, "Rock": 1, "Scissors": 3}


win = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}

lose = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}


# part 1
def p1_round_score(you, other):
    def _score(you, other):
        if you == other:
            return 3
        elif you == "Rock" and other == "Paper":
            return 0
        elif you == "Rock" and other == "Scissors":
            return 6
        elif you == "Paper" and other == "Rock":
            return 6
        elif you == "Paper" and other == "Scissors":
            return 0
        elif you == "Scissors" and other == "Rock":
            return 0
        elif you == "Scissors" and other == "Paper":
            return 6
        else:
            raise Exception

    return score[you] + _score(you, other)


# part 2 alt score
def round_score(other_code, you_code):
    other = lookup[other_code]
    you = lookup[you_code]

    def _new_you(you_code, other):
        if you_code == "X":  # lose
            return 0, win[other]
        elif you_code == "Z":  # win
            return 6, lose[other]
        elif you_code == "Y":  # draw
            return 3, other
        else:
            raise Exception(you_code, other)

    win_score, new_you = _new_you(you_code, other)

    return score[new_you] + win_score


running_score = [
    round_score(other_code, you_code)
    for other_code, you_code in map(lambda row: row.strip().split(" "), text)
]


print(f"sum of scores: {sum(running_score)}")
print("in p1 test this should be 15")
print("in p2 test this should be 12")
