from __future__ import print_function
import argparse
import difflib
import os
from os import path
from collections import namedtuple

RATIO = "ratio"
KEYWORD = "keyword"

FOLLOW_LINKS_DEFAULT = True
INCLUDE_HIDDEN_DEFAULT = False

AppConfig = namedtuple("AppConfig", [
    "follow_links", "include_hidden", "as_list", "search", "first"])


def path_is_directory(single_path, follow_links=FOLLOW_LINKS_DEFAULT):
    is_directory = path.isdir(single_path)
    if follow_links:
        return is_directory
    return is_directory and not path.islink(single_path)


def filter_paths(
        path_list, follow_links=FOLLOW_LINKS_DEFAULT,
        include_hidden=INCLUDE_HIDDEN_DEFAULT):

    if include_hidden:
        return [
            item for item in path_list
            if path_is_directory(item, follow_links)]
    return [
        item for item in path_list
        if not item.startswith(".") and
        path_is_directory(item, follow_links)]


def get_print_directories(directories, as_list=False):
    separator = "\n" if as_list else "  "
    dirs_output = [d + "/" for d in directories]
    dirs_output = separator.join(dirs_output)
    return dirs_output


def _find_matches(search, items):
    matches = []
    for item in items:
        # Give maximum priority for exact matches at the beginning
        if item.startswith(search):
            ratio = 1
        else:
            seq = difflib.SequenceMatcher(lambda x: x == " ", search, item)
            ratio = round(seq.ratio(), 3)
        if ratio > 0:
            matches.append({RATIO: ratio, KEYWORD: item})
    matches.sort(key=lambda x: x[RATIO], reverse=True)
    return matches


def get_best_match(search, directories):
    search = search.lower()
    items_map = {d.lower(): d for d in directories}
    matches = _find_matches(search, items_map.keys())
    if matches:
        best_ratio = matches[0][RATIO]
        best_matches = [m for m in matches if m[RATIO] == best_ratio]
        best_matches.sort(key=lambda x: x[KEYWORD])
        keyword = best_matches[0][KEYWORD]
        return items_map[keyword]
    return None


def get_config_from_command_args():
    parser = argparse.ArgumentParser(
        description="Change the current working directory using "
        "fuzzy string matching ")
    parser.add_argument(
        "-n", "--no-links", action="store_true",
        help="ignore symlinks")
    parser.add_argument(
        "-a", "--include-hidden", action="store_true",
        help="include hidden files (ignored by default)")
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="use a newline-separated listing format")
    parser.add_argument(
        "-f", "--first", action="store_true",
        help="change to first directory without matching")
    parser.add_argument(
        "search", nargs="?",
        help="the string to use for fuzzy matching")
    args = parser.parse_args()

    return AppConfig(
        follow_links=not args.no_links,
        include_hidden=args.include_hidden,
        as_list=args.list,
        first=args.first,
        search=args.search)


def main(config):
    path_list = os.listdir(".")
    directories = filter_paths(
        path_list, config.follow_links, config.include_hidden)
    directories.sort()

    if not directories:
        print("No directories to jump to")
        exit(1)
    elif config.first:
        print("found: " + directories[0])
        exit(0)
    elif config.search:
        match = get_best_match(config.search, directories)
        if match:
            print("found: " + match)
            exit(0)
        else:
            print("No match")
            exit(1)
    else:
        output = get_print_directories(directories, config.as_list)
        print(output)
        exit(0)


if __name__ == "__main__":
    app_config = get_config_from_command_args()
    main(app_config)
