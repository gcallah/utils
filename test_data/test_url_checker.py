import unittest
from url_checker import OurHTMLParser

class TestUrlChecker(unittest.TestCase):
    '''
    Tests for url_checker.py
    '''
    def setUp(self):
        self.url_checker = OurHTMLParser()

    def test_valid_url(self):
        link1 = "https://www.arresteddevops.com/"
        link2 = "http://devopscafe.org/"
        self.assertTrue(self.url_checker.is_accessible(link1))
        self.assertTrue(self.url_checker.is_accessible(link2))

    def test_invalid_url(self):
        link1 = "https://gcallah.github.io/DevOps/reviews/Practical_DevOps-Joakim_Verona.html"
        link2 = "weird.link.org"
        self.assertTrue(self.url_checker.is_accessible(link1))
        self.assertFalse(self.url_checker.is_accessible(link2))
        
if __name__ == '__main__':
    unittest.main()