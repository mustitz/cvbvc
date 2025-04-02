import unittest
from utils import format_ranges

class TestFormatRanges(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(format_ranges([]), "")

    def test_single_number(self):
        self.assertEqual(format_ranges([5]), "5")

    def test_consecutive_numbers(self):
        self.assertEqual(format_ranges([1, 2, 3, 4, 5]), "1-5")

    def test_non_consecutive_numbers(self):
        self.assertEqual(format_ranges([1, 3, 5, 7]), "1, 3, 5, 7")

    def test_mixed_numbers(self):
        self.assertEqual(format_ranges([1, 2, 3, 5, 6, 8]), "1-3, 5-6, 8")

    def test_single_range_with_gap(self):
        self.assertEqual(format_ranges([1, 2, 3, 5, 6, 7]), "1-3, 5-7")

    def test_large_gap(self):
        self.assertEqual(format_ranges([1, 2, 10, 11, 12]), "1-2, 10-12")

    def test_multiple_ranges(self):
        self.assertEqual(format_ranges([1, 2, 4, 5, 7, 8, 10]), "1-2, 4-5, 7-8, 10")

    def test_iterator(self):
        self.assertEqual(format_ranges(range(42)), "0-41")

if __name__ == "__main__":
    unittest.main()
