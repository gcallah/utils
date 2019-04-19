"""
This is the test suite for misc.py.
"""

from unittest import TestCase, main
from pylib.misc import filenm_from_key


class MiscTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_filenm_from_key(self):
        str1 = "file name"
        file1 = "file_name"
        self.assertEqual(filenm_from_key(str1), file1)
        str2 = "filename"
        file2 = "filename"
        self.assertEqual(filenm_from_key(str2), file2)
