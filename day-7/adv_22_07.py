from dataclasses import dataclass, field
import re
import sys
from typing import Optional


@dataclass
class Dir:
    name: str
    size: int = 0
    dirs: list["Dir"] = field(default_factory=list)
    files: list["File"] = field(default_factory=list)
    parent: Optional["Dir"] = None

    @classmethod
    def build(cls, name):
        return Dir(name=name)


@dataclass
class File:
    size: int
    name: str

    @classmethod
    def build(cls, size, name):
        return File(size=int(size), name=name)


CD_LINE_RE = re.compile(r"^\$ cd ([a-zA-Z]*)$")
CD_UP_LINE_RE = re.compile(r"^\$ cd ..$")
LS_LINE_RE = re.compile(r"^\$ ls$")
FILE_LINE_RE = re.compile(r"^(\d*) (.*)$")
DIR_LINE_RE = re.compile(r"^dir (.*)$")


def tree_build(lines):
    assert lines[0] == "$ cd /"
    root = Dir(name="/")

    parent = root

    for line in lines[1:]:
        if line is None:
            continue

        result = parse_line(line)

        if isinstance(result, tuple) and result[0] == "cd":
            change_dir = result[1]
            for dir_ in parent.dirs:
                if dir_.name == change_dir:
                    parent = dir_
                    break

        elif result == "up":
            parent = parent.parent

        elif isinstance(result, File):
            parent.files.append(result)

        elif isinstance(result, Dir):
            setattr(result, "parent", parent)
            parent.dirs.append(result)

        elif result == "list":
            continue

    return root


def parse_line(line):
    if match := CD_LINE_RE.match(line):
        return "cd", match.groups()[0]
    if match := CD_UP_LINE_RE.match(line):
        return "up"
    if match := LS_LINE_RE.match(line):
        return "list"
    if match := FILE_LINE_RE.match(line):
        return File.build(*match.groups())
    if match := DIR_LINE_RE.match(line):
        return Dir.build(*match.groups())

    raise Exception(f"unmatched line {line}")


def recursive_size(dir_node):
    def _file_sum(node):
        return sum(file.size for file in node.files)

    def _dir_sum(node):
        return sum(dir_.size for dir_ in node.dirs)

    if len(dir_node.dirs) == 0:
        dir_node.size = _file_sum(dir_node)
    else:
        for child_node in dir_node.dirs:
            recursive_size(child_node)

        dir_node.size = _file_sum(dir_node) + _dir_sum(dir_node)


def find_small_dirs(dir_node, size=100000, part_1=False):
    # part 1
    if part_1 and (dir_node.size < size):
        yield dir_node
    else:
        yield dir_node

    for child_node in dir_node.dirs:
        yield from find_small_dirs(child_node)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="UTF-8") as fh:
        input_lines = map(lambda line: line.strip(), fh.readlines())

    tree = tree_build(list(input_lines))
    recursive_size(tree)

    cumulative_size = 0
    small_nodes = list(find_small_dirs(tree))
    for small_node in small_nodes:
        cumulative_size += small_node.size

    print("small nodes cumulative size: ", cumulative_size)
    print("in p1 test this is 95437")

    ## part 2
    total_available = 70000000
    unused_required = 30000000

    print("root node size: ", tree.size)
    print("current unused: ", total_available - tree.size)

    required_free = unused_required - (total_available - tree.size)

    print("require: ", required_free)
    print("\n\n")

    sized_dirs = sorted(
        list(find_small_dirs(tree, size=total_available)), key=lambda node: node.size
    )
    for sd in sized_dirs:
        if sd.size >= required_free:
            print("$$$ ", sd.name, sd.size)
            break

    print("p2 test answer is 24933642")
