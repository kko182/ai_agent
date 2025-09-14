# tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Unit tests for the Calculator class."""

    def setUp(self):
        # Create a new Calculator instance before each test
        self.calculator = Calculator()

    def test_addition(self):
        # Test basic addition
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        # Test basic subtraction
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        # Test basic multiplication
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        # Test basic division
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        # Test an expression with multiple operations (order of operations)
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        # Test a more complex expression with multiple operators
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        # Test that an empty string returns None
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        # Test that invalid operators raise a ValueError
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        # Test that incomplete expressions raise a ValueError
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")


# Run the unit tests when this script is executed directly
if __name__ == "__main__":
    unittest.main()
