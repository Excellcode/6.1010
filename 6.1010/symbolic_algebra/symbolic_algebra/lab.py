"""
6.101 Lab:
Symbolic Algebra
"""

import string  # optional import

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class SymbolicEvaluationError(Exception):
    """
    An expression indicating that something has gone wrong when evaluating a
    symbolic algebra expression. Raised when a variable is not found in the
    provided mapping during evaluation.
    """

    pass


class Expr:
    """
    Base class for all symbolic expressions (variables, numbers, and operations).
    This class defines operator overloading to easily construct expression trees.
    """

    def __add__(self, class_expr):
        """
        Implements self + expr, returning an Add expression.
        Handles construction via operator overloading.
        """
        return Add(self, class_expr)

    def __radd__(self, class_expr):
        """
        Implements expr + self, returning an Add expression.
        """
        return Add(self, class_expr)

    def __sub__(self, class_expr):
        """
        Implements self - expr, returning aruff Sub expression.
        """
        return Sub(self, class_expr)

    def __rsub__(self, Class_expr):
        """
        Implements expr - self, returning a Sub expression (with swapped arguments).
        """
        return Sub(Class_expr, self)

    def __mul__(self, class_expr):
        """
        Implements self * expr, returning a Mul expression.
        """
        return Mul(self, class_expr)

    def __truediv__(self, class_expr):
        """
        Implements self / expr, returning a Div expression.
        """
        return Div(self, class_expr)

    def __rtruediv__(self, class_expr):
        """
        Implements expr / self, returning a Div expression (with swapped arguments).
        """
        return Div(class_expr, self)

    def __rmul__(self, class_expr):
        """
        Implements expr * self, returning a Mul expression.
        """
        return Mul(class_expr, self)


class Var(Expr):
    """
    Represents a symbolic variable (e.g., 'x', 'y').
    """

    def __init__(self, name):
        """
        Initializer. Store an instance variable called `name`, containing the
        name of the variable (a string).
        """
        self.name = name

    def __str__(self):
        """
        Returns the string representation of the variable's name.
        """
        return self.name

    def __repr__(self):
        """
        Returns a string that can be used to reconstruct the Var object.
        """
        return f"Var('{self.name}')"

    def evaluate(self, mapping):
        """
        Evaluates the variable by looking up its value in the provided mapping.

        Args:
            mapping (dict): A dictionary mapping
            variable names (str) to values (numbers).

        Returns:
            The numerical value of the variable from the mapping.

        Raises:
            SymbolicEvaluationError: If the variable's name is not in the mapping.
        """
        try:
            return mapping[self.name]
        except KeyError:
            raise SymbolicEvaluationError(
                f"Variable '{self.name}' not found in mapping"
            )

    def deriv(self, var):
        """
        Computes the symbolic derivative of the variable with respect to 'var'.
        The derivative of x with respect to x is 1; otherwise, it is 0.

        Args:
            var (str): The variable name to differentiate with respect to.

        Returns:
            Num(1) or Num(0).
        """
        # d/dx(x) = 1, d/dx(y) = 0
        return Num(1) if self.name == var else Num(0)

    def simplify(self):
        """
        A variable expression is already in its simplest form.

        Returns:
            The Var object itself.
        """
        return self


class Num(Expr):
    """
    Represents a numerical constant (e.g., 5, 3.14).
    """

    def __init__(self, n):
        """
        Initializer. Store an instance variable called `n`, containing the
        numerical value (an int or float).
        """
        self.n = n

    def __str__(self):
        """
        Returns the string representation of the number.
        """
        return str(self.n)

    def __repr__(self):
        """
        Returns a string that can be used to reconstruct the Num object.
        """
        return f"Num({self.n})"

    def __eq__(self, other):
        """
        Checks for equality between two Num objects based on their stored value `n`.
        """
        # Ensure 'other' is also a Num instance for comparison
        return isinstance(other, Num) and self.n == other.n

    def evaluate(self, mapping=None):
        """
        Evaluates the number expression.

        Args:
            mapping (dict): Unused for Num, but required by Expr interface.

        Returns:
            The numerical value `n`.
        """
        return self.n

    def deriv(self, var=None):
        """
        Computes the symbolic derivative of a constant with respect to any variable.
        The derivative of a constant is always 0.

        Args:
            var (str): The variable name to differentiate with respect to.

        Returns:
            Num(0).
        """
        return Num(0)

    def simplify(self):
        """
        A number expression is already in its simplest form.

        Returns:
            The Num object itself.
        """
        return self


class BinOp(Expr):
    """
    Base class for all binary operations (Add, Sub, Mul, Div).
    Handles wrapping of inputs and general string representation logic.
    """
    
    def __init__(self, left, right):
        """
        Initializer for a binary operation. Stores the left and right operands.
        Automatically wraps int/float/str inputs into Num/Var objects.

        Args:
            left (Expr or int/float/str): The left-hand operand.
            right (Expr or int/float/str): The right-hand operand.
        """
        
        # Helper function to convert raw types (int/float/str) into Expr subclasses
        def wrap_expr(expr_new):
            if isinstance(expr_new, (int, float)):
                return Num(expr_new)
            elif isinstance(expr_new, str):
                return Var(expr_new)
            else:
                return expr_new

        self.left = wrap_expr(left)
        self.right = wrap_expr(right)
        self.operators = {"Add": "+", "Sub": "-", "Mul": "*", "Div": "/"}
        # Define precedence for correct parenthesizing in __str__
        self.precidence_dict = {"Add": 0, "Sub": 0, "Mul": 1, "Div": 1} 
        # self.operator_name is set in subclass initializers

    def __str__(self, check=False):
        """
        Returns the algebraic string representation of the binary operation,
        including parentheses where necessary to maintain correct precedence.
        """
        left_string = str(self.left)
        right_string = str(self.right)

        # Rule 1: Parenthesize additive operations (Add, Sub) when they appear
        # as children of multiplicative operations (Mul, Div).
        if self.precidence == 1:
            try:
                # Check if the left child is an Add or Sub
                if self.left.precidence == 0:
                    left_string = f"({left_string})"
            except AttributeError:
                pass  # Not a BinOp, so no operator_name

            try:
                # Check if the right child is an Add or Sub
                if self.right.precidence == 1:
                    right_string = f"({right_string})"
                    check = True  # Flag to avoid re-checking right side for Rule 2
            except AttributeError:
                pass

        # Rule 2: Parenthesize right child if it has the same or lower precedence
        # as the current operator, but only for non-commutative/non-associative
        # operations (Sub, Div).
        if (not check) and (self.precidence == 1):
            try:
                # Check if the right child's precedence is less than or equal to current
                if (
                    self.precidence
                    <= self.precidence
                ):
                    right_string = f"({right_string})"
            except AttributeError:
                pass

        operator = self.operators[self.operator_name]
        return left_string + " " + operator + " " + right_string

    def __repr__(self):
        """
        Returns a string that can be used to reconstruct the BinOp object.
        """
        return f"{self.operator_name}({repr(self.left)}, {repr(self.right)})"

    def simplify(self):
        """
        Recursively simplifies the expression using standard algebraic identities
        and constant folding.
        """
        # Recursively simplify the children first
        left = self.left.simplify()
        right = self.right.simplify()
        operator = self.operator_name

        # 1. Constant folding: If both children are numbers,
        # evaluate and return a single Num
        if isinstance(left, Num) and isinstance(right, Num):
            # Use self.evaluate({}) to perform the arithmetic
            return Num(type(self)(left, right).evaluate({}))

        # 2. Identity rules
        # x + 0 = x, x - 0 = x
        if right == Num(0) and self.precidence[operator] == 0:
            return left  # Return the simplified left child

        # x * 1 = x, x / 1 = x
        if right == Num(1) and :
            return left

        # 3. Annihilation rules
        # x * 0 = 0, 0 * x = 0
        if (right == Num(0) or left == Num(0)) and operator == "Mul":
            return Num(0)

        # 0 / x = 0
        if left == Num(0) and operator == "Div":
            return Num(0)

        # 4. Identity rules for the left side
        # (only for Add/Mul, since they are commutative/associative)
        # 0 + x = x
        if left == Num(0) and operator == "Add":
            return right  # Return the simplified right child

        # 1 * x = x
        if left == Num(1) and operator == "Mul":
            return right

        # If no simplification rule applies,
        # return a new BinOp object with the simplified children
        return type(self)(left, right)


# Concrete Binary Operation Classes
class Add(BinOp):
    """Represents the addition operation."""

    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.operator_name = "Add"
        self.precidence = self.precidence_dict[self.operator_name]

    def evaluate(self, mapping):
        """Evaluates the addition operation: left + right."""
        left_val = self.left.evaluate(mapping)
        right_val = self.right.evaluate(mapping)
        return left_val + right_val

    def deriv(self, var):
        """Implements the sum rule: d/dx(u + v) = d/dx(u) + d/dx(v)."""
        # Note: The + operator here uses Expr.__add__ which returns a new Add object
        return self.left.deriv(var) + self.right.deriv(var)


class Sub(BinOp):
    """Represents the subtraction operation."""

    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.operator_name = "Sub"
        self.precidence = self.precidence_dict[self.operator_name]

    def evaluate(self, mapping):
        """Evaluates the subtraction operation: left - right."""
        left_val = self.left.evaluate(mapping)
        right_val = self.right.evaluate(mapping)
        return left_val - right_val

    def deriv(self, var):
        """Implements the difference rule: d/dx(u - v) = d/dx(u) - d/dx(v)."""
        # Note: The - operator here uses Expr.__sub__ which returns a new Sub object
        return self.left.deriv(var) - self.right.deriv(var)


class Mul(BinOp):
    """Represents the multiplication operation."""

    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.operator_name = "Mul"
        self.precidence = self.precidence_dict[self.operator_name]

    def evaluate(self, mapping):
        """Evaluates the multiplication operation: left * right."""
        left_val = self.left.evaluate(mapping)
        right_val = self.right.evaluate(mapping)
        return left_val * right_val

    def deriv(self, var):
        """Implements the product rule: d/dx(u * v) = u * d/dx(v) + v * d/dx(u)."""
        # Note: The * and + operators here use Expr methods for construction
        left_deriv = self.left.deriv(var)
        right_deriv = self.right.deriv(var)

        # (d/dx(u) * v) + (d/dx(v) * u)
        return left_deriv * self.right + right_deriv * self.left


class Div(BinOp):
    """Represents the division operation."""

    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.operator_name = "Div"
        self.precidence = self.precidence_dict[self.operator_name]

    def evaluate(self, mapping):
        """Evaluates the division operation: left / right."""
        left_val = self.left.evaluate(mapping)
        right_val = self.right.evaluate(mapping)
        return left_val / right_val

    def deriv(self, var):
        """
        Implements the quotient rule: d/dx(u / v) = (v * d/dx(u) - u * d/dx(v)) / v^2.
        v^2 is implemented as v * v.
        """
        # Note: All operators here use Expr methods for construction
        left_deriv = self.left.deriv(var)
        right_deriv = self.right.deriv(var)

        # Numerator: (d/dx(u) * v) - (d/dx(v) * u)
        numerator = left_deriv * self.right - right_deriv * self.left
        # Denominator: v * v
        denominator = self.right * self.right

        return numerator / denominator


def make_expression(new_expr):
    """
    Convenience function to take a string expression, tokenize it, and parse it
    into an Expr tree.

    Args:
        expr (str): The algebraic expression string.

    Returns:
        Expr: The root node of the parsed expression tree.
    """
    return parse(tokenize(new_expr))


def tokenize(new_expr):
    """
    Converts a string algebraic expression into a list of tokens.
    Handles multi-character variables, numbers (including floats), and correctly
    separates operators and parentheses.

    Args:
        expr (str): The input expression string.

    Returns:
        list: A list of tokens (strings).
    """
    build = ""
    token_type = None  # 'num', 'var', 'ope', 'par'
    operators = ["*", "+", "-", "/"]
    num_chars = set(string.digits + ".")
    result = []

    for index, char in enumerate(new_expr):
        # Skip whitespace
        if char == " ":
            continue

        # Handle parentheses immediately
        if char in ["(", ")"]:
            # If a token was being built (number or variable), finalize it first
            if build:
                result.append(build)
                build = ""
            result.append(char)
            token_type = "par"
            continue

        # Check for numbers (including negative numbers that start a token)
        is_num_char = char in num_chars or (
            char == "-"
            and index + 1 < len(new_expr)
            and new_expr[index + 1] in num_chars
            and (not result or result[-1] in ["(", "+", "-", "*", "/"])
        )

        if is_num_char:
            # If the previous token was a variable or operator, finalize it
            if token_type not in ("num", None):
                if build:
                    result.append(build)
                    build = ""

            # Continuation of a number or start of a new one
            build += char
            token_type = "num"
            continue

        # Check for operators
        if char in operators:
            # Finalize any previously built token (number or variable)
            if build:
                result.append(build)
                build = ""
            result.append(char)
            token_type = "ope"
            continue

        # Must be a variable/non-numeric part

        # If the previous token was a number or operator,
        # finalize it (e.g., '2x' or 'x+y')
        if token_type not in ("var", None):
            if build:
                result.append(build)
                build = ""

        build += char
        token_type = "var"

    # Append any remaining built token
    if build:
        result.append(build)

    return result


alphabets = string.ascii_lowercase


def parse(token):
    """
    Parses a list of tokens into an expression tree (Expr object).
    This function expects the tokens to represent a fully parenthesized
    expression (e.g., prefix-like structure for the binary operators).

    Args:
        token (list): A list of tokens (strings) generated by tokenize.

    Returns:
        Expr: The root of the parsed expression tree.
    """
    operators = {"+": Add, "-": Sub, "/": Div, "*": Mul}

    # Inner recursive function to parse a sub-expression starting at a given index
    def parse_expression(index):
        get_token = token[index]

        # Case 1: Number
        try:
            new_token = float(get_token)
            return Num(new_token), index + 1
        except ValueError:
            pass  # Not a number, continue

        # Case 2: Variable (checking if the first char is a letter)
        if get_token[0].lower() in string.ascii_lowercase:
            return Var(get_token), index + 1

        # Case 3: Parenthesized Binary Operation
        if get_token == "(":
            # Find the index of the main operator
            # for this parenthesized expression
            small_index = index + 1
            open_par_count = 0
            close_par_count = 0

            # Loop until the main operator is found
            # (must be at the top-level of this sub-expression)
            while (token[small_index] not in operators) or (
                open_par_count != close_par_count
            ):
                if token[small_index] == "(":
                    open_par_count += 1
                if token[small_index] == ")":
                    close_par_count += 1
                small_index += 1

            operator_index = small_index
            operator_class = operators[token[small_index]]

            # Recurse to parse the left operand
            # (tokens from index + 1 up to operator_index)
            left_expr = parse(token[index + 1 : operator_index])

            # Now find the end of the right operand (the matching closing parenthesis)
            open_par_count = 1  # Start count, since we are inside the outer '('
            close_par_count = 0
            small_index += 1  # Move past the operator

            start_right_index = small_index

            while open_par_count != close_par_count:
                if token[small_index] == "(":
                    open_par_count += 1
                if token[small_index] == ")":
                    close_par_count += 1
                small_index += 1

            end_right_index = small_index - 1  # The token before the closing ')'

            # Recurse to parse the right operand
            # (tokens from start_right_index up to end_right_index)
            right_expr = parse(token[start_right_index:end_right_index])

            # Construct the binary operation object
            return operator_class(left_expr, right_expr), small_index

    # Start parsing from the beginning of the token list
    parsed_expression, _ = parse_expression(0)
    return parsed_expression


if __name__ == "__main__":
    # Example usage and testing
    z = Add(Var("x"), Sub(Var("y"), Num(2)))
    print(f"Repr of z: {repr(z)}")
    print(f"Str of Mul: {str(Mul(Var('x'), Add(Var('y'), Var('z'))))}")

    x = Var("x")
    y = Var("y")

    # Expression: 2*x - x*y + 3*y
    expr = 2 * x - x * y + 3 * y
    print(f"\nOriginal expression: {expr}")

    # Test simplification
    print(f"Simplify: {expr.simplify()}")

    # Test derivatives
    deriv_x = expr.deriv("x")
    print(f"Derivative w.r.t x: {deriv_x}")
    print(f"Simplified deriv w.r.t x: {deriv_x.simplify()}")

    deriv_y = expr.deriv("y")
    print(f"Derivative w.r.t y: {deriv_y}")
    print(f"Simplified deriv w.r.t y: {deriv_y.simplify()}")

    # More simplification tests
    simplified_add = Add(Add(Num(2), Num(-2)), Add(Var("x"), Num(0))).simplify()
    print(f"\nAdd simplification: {simplified_add}")

    simplified_mul = (Num(0) * x + Num(1) * Num(2)).simplify()
    print(f"Mul/Add simplification: {simplified_mul}")

    simplified_zero_mul = Add(Mul(Num(40), Num(20)), Mul(Var("z"), Num(0))).simplify()
    print(f"Zero Mul simplification: {simplified_zero_mul}")

    # Test tokenization and parsing
    token_test = tokenize("((z * 3) + 0)")
    print(f"\nTokens for '((z * 3) + 0)': {token_test}")
    parsed_expr = parse(token_test)
    print(f"Parsed expression: {repr(parsed_expr)}")
    print(f"Parsed expression simplified: {parsed_expr.simplify()}")

    print(f"Tokens for '-4.9': {tokenize('-4.9')}")
