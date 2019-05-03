"""
This is the test suite for html_tags.py.
"""

from unittest import TestCase, main
from pylib.html_tags import include_tag, par, link, figure, details, ulist, olist, image
from pylib.html_tags import head, sidebar_links, sidebar, str_to_valid_id, html_list


class HtmlTagTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def include_tag(self):
        str1 = "{% include ' filename ' %}"
        file1 = "filename"
        self.assertEqual(include_tag(str1), file1)
		
	def par(self):
        self.assertEqual(1, 1)

    def link(self):
        self.assertEqual(1, 1)
		
    def figure(self):
        self.assertEqual(1, 1)
		
    def details(self):
        self.assertEqual(1, 1)

    def ulist(self):
        self.assertEqual(1, 1)

    def olist(self):
        self.assertEqual(1, 1)

    def image(self):
        self.assertEqual(1, 1)
		
    def head(self):
        self.assertEqual(1, 1)
		
    def sidebar_links(self):
        self.assertEqual(1, 1)
		
    def sidebar(self):
        self.assertEqual(1, 1)
		
    def str_to_valid_id(self):
        self.assertEqual(1, 1)
		
    def html_list(self):
        self.assertEqual(1, 1)
		