"""
This is the test suite for parse_site.
"""

from unittest import TestCase, main
from pylib.parse_site import test_parse_site

class HtmlTagTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_for_parse_site(self):
		self.assertEqual(test_parse_site(“http://www.thedevopscourse.com/”), “The DevOps Course“)