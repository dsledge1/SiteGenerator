import unittest
from main import *

class TestSplitNode(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# This is a Happy Header"
        extracted = extract_title(markdown)
        self.assertEqual(extracted, "This is a Happy Header")

