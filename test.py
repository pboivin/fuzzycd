from __future__ import print_function
import os
import shutil
import tempfile
import unittest

from fuzzycd import (
    path_is_directory,
)


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


class TestFuzzyCD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        script_path = os.path.realpath(__file__)
        script_dir_path = os.path.dirname(script_path)
        test_dir_path = os.path.join(script_dir_path, "test_dir")
        dir_link_path = os.path.join(test_dir_path, "dir_link")
        file_path = os.path.join(test_dir_path, "some_file")
        file_link_path = os.path.join(test_dir_path, "file_link")

        if os.path.exists(test_dir_path):
            shutil.rmtree(test_dir_path, ignore_errors=True)

        os.mkdir(test_dir_path)
        os.mkdir(os.path.join(test_dir_path, "one"))
        os.mkdir(os.path.join(test_dir_path, "two"))
        os.mkdir(os.path.join(test_dir_path, "three"))
        four_dir_path = os.path.join(test_dir_path, "four")
        os.mkdir(four_dir_path)
        os.symlink(four_dir_path, dir_link_path)
        touch(file_path)
        os.symlink(file_path, file_link_path)

        cls.test_dir_path = test_dir_path
        cls.dir_link_path = dir_link_path
        cls.file_path = file_path
        cls.file_link_path = file_link_path

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


if __name__ == "__main__":
    unittest.main()
