# ---------------------------------------------------------------------------------------------------------------------
# 7.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import Optional, List


# ---------------------------------------------------------------------------------------------------------------------
class FileNode:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class DirNode:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, name: str, parent: Optional['DirNode'] = None) -> None:
        self.name = name
        self.nodes = []
        self.parent = parent
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def dir_node_by_name(self, name: str) -> 'DirNode':
        for n in self.nodes:
            if isinstance(n, DirNode) and n.name == name:
                return n
        else:
            raise RuntimeError
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def total_file_size(self) -> int:
        result = 0
        for n in self.nodes:
            if isinstance(n, FileNode):
                result += n.size
            elif isinstance(n, DirNode):
                result += n.total_file_size()
            else:
                raise RuntimeError
        return result
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "<'%s': %d bytes>" % (self.name, self.total_file_size())
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def parse_input(filename: str = 'input.txt') -> DirNode:

    root = DirNode('/')

    with open(filename) as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    cwd = None
    ls_now = FileNode
    for next_line in all_lines:

        if next_line.startswith('$'):
            ls_now = False
            cmd_parts = next_line.split(' ')
            if len(cmd_parts) == 2:
                assert cmd_parts[1] == 'ls'
                ls_now = True
            elif len(cmd_parts) == 3:
                assert cmd_parts[1] == 'cd'
                if cmd_parts[2] == '/':
                    cwd = root
                elif cmd_parts[2] == '..':
                    assert cwd.parent is not None
                    cwd = cwd.parent
                else:
                    cwd = cwd.dir_node_by_name(cmd_parts[2])
            else:
                raise RuntimeError

        else:
            assert ls_now
            line_parts = next_line.split(' ')
            assert len(line_parts) == 2
            if line_parts[0] == 'dir':
                cwd.nodes.append(DirNode(line_parts[1], parent=cwd))
            else:
                cwd.nodes.append(FileNode(line_parts[1], int(line_parts[0])))

    return root
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def walk_filesystem1(filesystem: DirNode, small_dirs: List[DirNode], size_limit) -> None:

    if filesystem.total_file_size() <= size_limit:
        small_dirs.append(filesystem)

    for n in filesystem.nodes:
        if isinstance(n, DirNode):
            walk_filesystem1(n, small_dirs, size_limit)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def walk_filesystem2(filesystem: DirNode, all_dirs: List[DirNode]) -> None:

    all_dirs.append(filesystem)

    for n in filesystem.nodes:
        if isinstance(n, DirNode):
            walk_filesystem2(n, all_dirs)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    filesystem = parse_input()

    small_dirs: List[DirNode]
    small_dirs = []
    walk_filesystem1(filesystem, small_dirs, 100000)
    print("part 1: %d" % sum([d.total_file_size() for d in small_dirs]))

    all_dirs: List[DirNode]
    all_dirs = []
    walk_filesystem2(filesystem, all_dirs)

    all_dirs_sorted = sorted(all_dirs, key=lambda d: d.total_file_size())

    total_disk_space = 70000000
    needed_disk_space = 30000000

    print("total_disk_space: %d" % total_disk_space)
    print("needed_disk_space: %d" % needed_disk_space)

    used_disk_space = filesystem.total_file_size()
    free_disk_space = total_disk_space - used_disk_space

    print("used_disk_space: %d" % used_disk_space)
    print("free_disk_space: %d" % free_disk_space)

    assert needed_disk_space > free_disk_space

    extra_disk_space = needed_disk_space - free_disk_space
    print("extra_disk_space: %d" % extra_disk_space)

    target_dir = None
    for d in all_dirs_sorted:
        print("%s, %d bytes" % (d.name, d.total_file_size()), end='')
        if d.total_file_size() > extra_disk_space and target_dir is None:
            target_dir = d
            print(" <---")
        else:
            print("")

    assert target_dir is not None

    print("part 2: %d" % target_dir.total_file_size())
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
