from __future__ import print_function
import os
import shutil
import tempfile
import unittest

from fuzzycd import (
    path_is_directory, filter_paths, get_print_directories, get_best_match)

TEST_DIR = "test_dir"


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


class TestFuzzyCD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        script_path = os.path.realpath(__file__)
        script_dir_path = os.path.dirname(script_path)
        test_dir_path = os.path.join(script_dir_path, TEST_DIR)

        if os.path.exists(test_dir_path):
            shutil.rmtree(test_dir_path, ignore_errors=False)

        # Root directory for tests
        os.mkdir(test_dir_path)
        os.chdir(test_dir_path)

        # 4 directories
        os.mkdir(os.path.join(test_dir_path, "one"))
        os.mkdir(os.path.join(test_dir_path, "two"))
        os.mkdir(os.path.join(test_dir_path, "three"))
        four_dir_path = os.path.join(test_dir_path, "four")
        os.mkdir(four_dir_path)

        # 1 symlink to a directory
        dir_link_path = os.path.join(test_dir_path, "dir_link")
        os.symlink(four_dir_path, dir_link_path)

        # 1 hidden directory
        os.mkdir(os.path.join(test_dir_path, ".hidden_dir"))

        # 1 regular file and 1 symlink
        file_path = os.path.join(test_dir_path, "some_file")
        file_link_path = os.path.join(test_dir_path, "file_link")
        touch(file_path)
        os.symlink(file_path, file_link_path)

        # Paths used in tests below
        cls.test_dir_path = test_dir_path
        cls.dir_link_path = dir_link_path
        cls.file_path = file_path
        cls.file_link_path = file_link_path

    @classmethod
    def get_test_dir_path_list(cls):
        return os.listdir(cls.test_dir_path)

    def test_path_is_directory(self):
        self.assertTrue(path_is_directory(self.test_dir_path))

    def test_path_is_directory_reject_file(self):
        self.assertFalse(path_is_directory(self.file_path))

    def test_path_is_directory_accept_symlink(self):
        self.assertTrue(
            path_is_directory(self.dir_link_path, follow_links=True))

    def test_path_is_directory_reject_symlink(self):
        self.assertFalse(
            path_is_directory(self.dir_link_path, follow_links=False))

    def test_filter_paths_include_symlinks(self):
        path_list = self.get_test_dir_path_list()
        filtered_path_list = filter_paths(path_list, follow_links=True)
        self.assertEqual(len(filtered_path_list), 5)

    def test_filter_paths_exclude_symlinks(self):
        path_list = self.get_test_dir_path_list()
        filtered_path_list = filter_paths(path_list, follow_links=False)
        self.assertEqual(len(filtered_path_list), 4)

    def test_filter_paths_include_hidden(self):
        path_list = self.get_test_dir_path_list()
        filtered_path_list = filter_paths(path_list, include_hidden=True)
        self.assertEqual(len(filtered_path_list), 6)

    def test_filter_paths_exlude_hidden(self):
        path_list = self.get_test_dir_path_list()
        filtered_path_list = filter_paths(path_list, include_hidden=False)
        self.assertEqual(len(filtered_path_list), 5)

    def test_get_print_directories(self):
        path_list = ["one", "two", "three", "four"]
        output = get_print_directories(path_list)
        output_list = output.split("  ")
        self.assertEqual(len(output_list), 4)

    def test_get_print_directories_as_list(self):
        path_list = ["one", "two", "three", "four"]
        output = get_print_directories(path_list, as_list=True)
        output_list = output.split("\n")
        self.assertEqual(len(output_list), 4)

    def test_get_best_match(self):
        path_list = [
            "Desktop", "Documents", "Downloads", "Projects", "Everything Else",
            "else"]
        self.assertEqual(
            "Desktop", get_best_match("desk", path_list))
        self.assertEqual(
            "Downloads", get_best_match("load", path_list))
        self.assertEqual(
            "else", get_best_match("else", path_list))
        self.assertEqual(
            "Documents", get_best_match("do", path_list))
        self.assertEqual(
            "Everything Else", get_best_match("something", path_list))

    def test_get_best_match_no_match(self):
        path_list = ["one", "two", "three"]
        self.assertEqual(None, get_best_match("xyz", path_list))


if __name__ == "__main__":
    unittest.main()
