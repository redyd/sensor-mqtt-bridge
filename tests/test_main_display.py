import unittest


class MainDisplayTest(unittest.TestCase):
    def test_format_display_value_rounds_numbers_to_two_decimals(self):
        import main

        self.assertEqual(main.format_display_value(21.16665), "21.17")
        self.assertEqual(main.format_display_value(10), "10.00")
        self.assertEqual(main.format_display_value("-"), "-")


if __name__ == "__main__":
    unittest.main()
