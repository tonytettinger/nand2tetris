import unittest
from parser import Parser


class TestParser(unittest.TestCase):

    def test_has_more_lines(self):
        parser = Parser('SimpleAdd')
        self.assertTrue(parser.has_more_lines())  # First line
        self.assertTrue(parser.has_more_lines())  # Second line
        self.assertTrue(parser.has_more_lines())  # Third line (should be empty, but still exists)

    def test_advance(self):
        parser = Parser('SimpleAdd')

        # First line
        parser.advance()
        self.assertEqual(parser.command_type, 'push')
        self.assertEqual(parser.arg1, 'constant')
        self.assertEqual(parser.arg2, '7')
        # Second line
        parser.advance()
        self.assertEqual(parser.command_type, 'push')
        self.assertEqual(parser.arg1, 'constant')
        self.assertEqual(parser.arg2, '8')

        # Third line
        parser.advance()
        self.assertEqual(parser.command_type, 'add')
        self.assertEqual(parser.arg1, None)
        self.assertEqual(parser.arg2, None)


if __name__ == '__main__':
    unittest.main()
