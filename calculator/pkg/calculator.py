# calculator.py

class Calculator:
    """A simple calculator that evaluates basic arithmetic expressions using infix notation."""

    def __init__(self):
        # Define supported operators as lambdas
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        # Define operator precedence for infix evaluation
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        # Return None for empty or whitespace-only expressions
        if not expression or expression.isspace():
            return None
        # Tokenize the expression by splitting on spaces
        tokens = expression.strip().split()
        # Evaluate the tokenized infix expression
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        # Stack to hold numeric values
        values = []
        # Stack to hold operators
        operators = []

        for token in tokens:
            if token in self.operators:
                # While the top operator has higher or equal precedence, apply it
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                # Push the current operator onto the stack
                operators.append(token)
            else:
                # Try to convert the token to a float and push to values stack
                try:
                    values.append(float(token))
                except ValueError:
                    # Raise an error if token is not a valid number
                    raise ValueError(f"invalid token: {token}")

        # Apply any remaining operators
        while operators:
            self._apply_operator(operators, values)

        # There should be exactly one value left, the final result
        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        # Return early if no operators to apply
        if not operators:
            return

        # Pop the operator from the stack
        operator = operators.pop()
        # Ensure there are at least two operands to apply the operator
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        # Pop operands in correct order: a operator b
        b = values.pop()
        a = values.pop()
        # Apply the operator and push the result back to values stack
        values.append(self.operators[operator](a, b))
