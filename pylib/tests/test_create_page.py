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

    def test_for_create_page(self):
        str1 = "file name"
        file1 = "file_name"
        self.assertEqual(create_page(str1), file1)
        str2 = "filename"
        file2 = "filename"
        self.assertEqual(create_page(str2), file2)
    
    def test_for_create_subtopics(self):
        self.assertEqual(1,1)
		
		