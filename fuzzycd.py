from __future__ import print_function
import argparse
import os
from os import path

from fuzzywuzzy import process


FOLLOW_LINKS_DEFAULT = True
SHOW_HIDDEN_DEFAULT = False


def path_is_directory(single_path, follow_links=FOLLOW_LINKS_DEFAULT):
    is_directory = path.isdir(single_path)
    if follow_links:
        return is_directory
    return is_directory and not path.islink(single_path)


def filter_paths(
        path_list, follow_links=FOLLOW_LINKS_DEFAULT,
        show_hidden=SHOW_HIDDEN_DEFAULT):

    if show_hidden:
        return [
            item for item in path_list
            if path_is_directory(item, follow_links)]
    return [
        item for item in path_list
        if not item.startswith(".") and
        path_is_directory(item, follow_links)]


def print_directories(directories):
    dirs_output = [d + "/" for d in directories]
    dirs_output = " ".join(dirs_output)
    print(dirs_output)


def get_best_match(search, directories):
    match = process.extractOne(search, directories)
    if match[1] > 0:
        return match[0]
    return None


def main(config):
    path_list = os.listdir(".")
    directories = filter_paths(
        path_list, config["follow_links"], config["show_hidden"])
    directories.sort()

    if config["search"]:
        match = get_best_match(config["search"], directories)
        if match:
            print("found: " + match)
            exit(0)
        else:
            print("No match")
            exit(1)
    else:
        print_directories(directories)
        exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Some app...")
    parser.add_argument("-n", "--no-links", action="store_true")
    parser.add_argument("-a", "--show-hidden", action="store_true")
    parser.add_argument("search", nargs="?")
    args = parser.parse_args()

    app_config = {
        "follow_links": not args.no_links,
        "show_hidden": args.show_hidden,
        "search": args.search,
    }

    main(app_config)
