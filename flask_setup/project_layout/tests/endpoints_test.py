from unittest import TestCase, main
from flask_restplus import Resource

from source import Hello, Home


class Test(TestCase):
    def setUp(self):
        # none of the object's members names should have caps!
        self.hello = Hello(Resource)
        self.home = Home(Resource)

    def test_hello(self):
        """
        See if Hello works.
        """
        rv = self.hello.get()
        self.assertEqual(rv, "Hello, World!")

    def test_home(self):
        '''
        Check that home returns an html
        '''
        rv = "test"
        self.assertEqual(rv, "test")


if __name__ == "__main__":
    main()
