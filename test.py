from __future__ import print_function
import os
import shutil
import tempfile
import unittest

from fuzzycd import (
    path_is_directory,
)


class TestFuzzyCD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Make directory
        cls.temp_dir_path = tempfile.mkdtemp()

        # Make directory link
        cls.temp_dir_path_link = cls.temp_dir_path + "_link"
        os.symlink(cls.temp_dir_path, cls.temp_dir_path_link)

        # Make regular file
        temp_file, temp_file_path = tempfile.mkstemp()
        cls.temp_file_path = temp_file_path

    @classmethod
    def tearDownClass(cls):
        if cls.temp_dir_path:
            shutil.rmtree(cls.temp_dir_path)
        if cls.temp_dir_path_link:
            os.remove(cls.temp_dir_path_link)
        if cls.temp_file_path:
            os.remove(cls.temp_file_path)

    def test_path_is_directory(self):
        self.assertTrue(path_is_directory(self.temp_dir_path))

    def test_path_is_directory_reject_file(self):
        self.assertFalse(path_is_directory(self.temp_file_path))

    def test_path_is_directory_accept_symlink(self):
        self.assertTrue(
            path_is_directory(self.temp_dir_path_link, follow_links=True))

    def test_path_is_directory_reject_symlink(self):
        self.assertFalse(
            path_is_directory(self.temp_dir_path_link, follow_links=False))


if __name__ == "__main__":
    unittest.main()
