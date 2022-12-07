import posixpath
from collections import defaultdict


def set_cwd(cwd, line):
    line = line.strip()
    if line == '$ cd /':
        nwd = '/'
    elif line == '$ cd ..':
        nwd = posixpath.dirname(cwd)
    else:
        target = line.removeprefix('$ cd ').strip()
        nwd = posixpath.join(cwd, target)
    return nwd


def calculate_dir_sizes(directories, paths_to_sizes):
    dir_sizes = dict()
    for directory in directories:
        dir_sizes[directory] = 0
        for path, size in paths_to_sizes.items():
            if path.startswith(directory):
                dir_sizes[directory] += size
    return dir_sizes


def get_directories_and_files_and_sizes(input_file):
    with open(input_file) as f:
        lines = iter(f.readlines())

    paths_to_sizes = defaultdict(int)
    directories = set('/')
    cwd = ''

    line = next(lines)
    while True:
        if line.startswith('$ ls'):
            line = next(lines)  # may be StopIteration
            while not line.startswith('$'):
                size, file = line.split()
                if size == 'dir':
                    directories.add(posixpath.join(cwd, file))
                else:
                    paths_to_sizes[posixpath.join(cwd, file)] = int(size)
                try:
                    line = next(lines)
                except StopIteration:
                    break
        elif line.startswith('$ cd'):
            cwd = set_cwd(cwd, line)
            try:
                line = next(lines)
            except StopIteration:
                break
        else:
            try:
                line = next(lines)
            except StopIteration:
                break
    dir_sizes = calculate_dir_sizes(directories, paths_to_sizes)
    return dir_sizes


def test__dir_sizes():
    dir_sizes = get_directories_and_files_and_sizes('day07_test_input.txt')
    assert 95437 == sum(size for dir, size in dir_sizes.items() if size < 100000)

    dir_sizes = get_directories_and_files_and_sizes('day07_real_input.txt')
    assert 1350966 == sum(size for dir, size in dir_sizes.items() if size < 100000)


def smallest_dir_to_free_target_size(dir_sizes):
    disk_size = 70000000
    free_space = disk_size - dir_sizes['/']
    required_space = 30000000
    space_to_be_freed = required_space - free_space

    ordered_dir_sizes = dict(sorted(dir_sizes.items(), key=lambda item: item[1]))
    for key, size in ordered_dir_sizes.items():
        if size > space_to_be_freed:
            return size
    return None


def test__dir_sizes_part2():
    dir_sizes = get_directories_and_files_and_sizes('day07_test_input.txt')
    assert 24933642 == smallest_dir_to_free_target_size(dir_sizes)

    dir_sizes = get_directories_and_files_and_sizes('day07_real_input.txt')
    assert 6296435 == smallest_dir_to_free_target_size(dir_sizes)



    # directories, paths_to_sizes = get_directories_and_files_and_sizes('day07_real_input.txt')
    # dir_sizes = get_dir_sizes(directories, paths_to_sizes)
    # size_ordered = dict(sorted(dir_sizes.items(), key=lambda item: item[1]))
    # disk_size = 70000000
    # free_space = disk_size - paths_to_sizes['/']
    # required_space = 30000000
    # space_to_be_freed = required_space - free_space
    # for key, size in size_ordered.items():
    #     if size > space_to_be_freed:
    #         assert key == 'a'
    #         return


