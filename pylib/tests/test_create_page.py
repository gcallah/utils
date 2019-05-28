"""
This is the test suite for create_page.py.
"""

import os
from unittest import TestCase, main
from pylib.create_page import create_page  # , create_subtopics

templ_dir = os.getenv("templ_dir", default="")

class CreatePageTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_page(self):
        page = create_page(templ_dir + "/template.ptml", "Test page")
        self.assertIn(page, "Test page")

    def create_subtopics(self):
        self.assertEqual(1, 1)
