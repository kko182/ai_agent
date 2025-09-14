# main.py

import sys
from pkg.calculator import Calculator
from pkg.render import render


def main():
    # Create an instance of the Calculator class
    calculator = Calculator()

    # If no arguments are provided, show usage instructions
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    # Combine all command-line arguments into a single expression string
    expression = " ".join(sys.argv[1:])

    try:
        # Evaluate the expression using the Calculator class
        result = calculator.evaluate(expression)

        # Format the result using the render function
        to_print = render(expression, result)

        # Display the result
        print(to_print)
    except Exception as e:
        # Print any errors that occur during evaluation or rendering
        print(f"Error: {e}")


# Entry point: only run main() if this script is executed directly
if __name__ == "__main__":
    main()
