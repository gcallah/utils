"""
This is the test suite for create_page.py.
"""

from unittest import TestCase, main
from pylib.create_page import create_page, create_subtopics


class CreatePageTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_page(self):
        str1 = "file name"
        file1 = "file_name"
        self.assertEqual(filenm_from_key(str1), file1)
        str2 = "filename"
        file2 = "filename"
        self.assertEqual(filenm_from_key(str2), file2)
    
    def create_subtopics(self):
        self.assertEqual(1,1)
		
		