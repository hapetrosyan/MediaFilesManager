import os
import filecmp


def get_all_files_in_folder(original_location):
    files = []
    for dirpath, dirnames, filenames in os.walk(original_location):
        for filename in filenames:
            full_file_path = os.path.join(dirpath, filename)
            files.append(full_file_path)
    return files


def make_pairs_from_list(list_of_files):
    result = []
    for p1 in range(len(list_of_files)):
        for p2 in range(p1 + 1, len(list_of_files)):
            result.append([list_of_files[p1], list_of_files[p2]])
    return result


def get_pairs_of_files_in_folder(original_location):
    files = get_all_files_in_folder(original_location)
    pairings = make_pairs_from_list(files)
    return pairings


def compare_pair_of_files(file1, file2):
    return filecmp.cmp(file1, file2, shallow = False)


def get_same_files_in_folder(original_location):
    matching_pairs = []
    pairs = get_pairs_of_files_in_folder(original_location)
    for pair in pairs:
        if compare_pair_of_files(*pair):
            matching_pairs.append(pair)
    return matching_pairs

