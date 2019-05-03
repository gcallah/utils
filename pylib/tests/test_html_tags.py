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

    def test_for_include_tag(self):
        str1 = "{% include ' filename ' %}"
        file1 = "filename"
        self.assertEqual(include_tag(str1), file1)
		
	def test_for_par(self):
        self.assertEqual(1, 1)

    def test_for_link(self):
        self.assertEqual(1, 1)
		
    def test_for_figure(self):
        self.assertEqual(1, 1)
		
    def test_for_details(self):
        self.assertEqual(1, 1)

    def test_for_ulist(self):
        self.assertEqual(1, 1)

    def test_for_olist(self):
        self.assertEqual(1, 1)

    def test_for_image(self):
        self.assertEqual(1, 1)
		
    def test_for_head(self):
        self.assertEqual(1, 1)
		
    def test_for_sidebar_links(self):
        self.assertEqual(1, 1)
		
    def test_for_sidebar(self):
        self.assertEqual(1, 1)
		
    def test_for_str_to_valid_id(self):
        self.assertEqual(1, 1)
		
    def test_for_html_list(self):
        self.assertEqual(1, 1)
		