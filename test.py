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
        cls.temp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        if cls.temp_dir:
            shutil.rmtree(cls.temp_dir)

    def test_path_is_directory(self):
        self.assertTrue(path_is_directory(self.temp_dir))


if __name__ == "__main__":
    unittest.main()
