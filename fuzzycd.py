from __future__ import print_function
import argparse
import os
from os import path
from collections import namedtuple

from fuzzywuzzy import process

FOLLOW_LINKS_DEFAULT = True
INCLUDE_HIDDEN_DEFAULT = False

AppConfig = namedtuple("AppConfig", [
    "follow_links", "include_hidden", "as_list", "search"])


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


def get_best_match(search, directories):
    match = process.extractOne(search, directories)
    if match and match[1] > 0:
        return match[0]
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
        "search", nargs="?",
        help="the string to use for fuzzy matching")
    args = parser.parse_args()

    return AppConfig(
        follow_links=not args.no_links,
        include_hidden=args.include_hidden,
        as_list=args.list,
        search=args.search)


def main(config):
    path_list = os.listdir(".")
    directories = filter_paths(
        path_list, config.follow_links, config.include_hidden)
    directories.sort()

    if config.search:
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
