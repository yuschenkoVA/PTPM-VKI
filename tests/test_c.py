import unittest
from src.c import add
class test_c (unittest.TestCase):
    def test_add (self):
        self.assertEqual(add(1,2), 3)
