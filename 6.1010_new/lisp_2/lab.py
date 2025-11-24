"""
6.101 Lab:
LISP Interpreter Part 2
"""

# KEEP THE ABOVE LINES INTACT, BUT REPLACE THIS COMMENT WITH ALL THE CODE IN
# THE lab.py FILE FROM THE lisp_1 LAB, WHICH SHOULD BE THE STARTING POINT FOR
# THIS LAB.


#!/usr/bin/env python3

# import typing  # optional import
# import pprint  # optional import
import doctest
import os
import sys
import string
from scheme_utils import (
    number_or_symbol,
    SchemeEvaluationError,
    SchemeNameError,
    SchemeSyntaxError, # uncomment in LISP part 2!
    SchemeREPL,
)

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!

# ==============================================================================
#                                  Built-ins
# ==============================================================================


def custom_sub(*args):
    """Handles (- a b) -> a-b and (- a b c...) -> a - (b+c+...)."""
    if len(args) == 2:
        return args[0] - args[1]

    first_num, *rest_nums = args
    return first_num - sum(rest_nums)


def custom_div(*args):
    """Handles (/ a b) -> a/b and (/ a b c...) -> a / (b*c*...)."""
    if len(args) == 2:
        return args[0] / args[1]

    first_num, *rest_nums = args
    return first_num / builtin_mul(*rest_nums)


def builtin_mul(*args):
    """Computes the product of arguments."""
    if len(args) == 2:
        return args[0] * args[1]

    first_num, *rest_nums = args
    return first_num * builtin_mul(*rest_nums)

def custom_compare(*args, func):
    if len(args) < 2:
        raise SchemeEvaluationError("bad")
    end_len = len(args)
    index = 1
    former = args[0]
    while index < end_len:
        current = args[index]
        if not func(former, current):
            return False
        index+= 1
        former = current
    return True
def custom_equal(*args):
    return custom_compare(*args, lambda x, y: x==y)
    
def custom_greater(*args):
    return custom_compare(*args, lambda x, y: x>y)
    
def custom_greater_equal(*args): 
    return custom_compare(*args, lambda x, y: x>=y)

def custom_lesser(*args):
    return custom_compare(*args, lambda x, y: x<y)
        
def custom_lesser_equal(*args):
    return custom_compare(*args, lambda x, y: x<=y)
   
def custom_not(*args):
    if len(args)!= 1:
        raise SchemeEvaluationError
    return True if args[0] == "#f" else False                 
SCHEME_BUILTINS = {
    "+": lambda *args: sum(args),
    "*": builtin_mul,
    "-": custom_sub,
    "/": custom_div,
    "#t" : True,
    "#f" : False,
    "equal?": custom_equal,
    ">": custom_greater,
    "">="": custom_greater_equal , 
    "<": custom_lesser, 
    "<=": custom_lesser_equal,
    "not": custom_not
}

# ==============================================================================
#                              Special Built-ins
# ==============================================================================


def run_define(branch, frame):
    """Handles (define x expr) and (define (f p) body)."""
    if isinstance(branch[1], str):
        # (define var expr)
        res = evaluate(branch[2], frame)
        var_name = branch[1]

    elif isinstance(branch[1], list) and len(branch[1]) >= 1:
        # (define (func params) body)
        var_name = branch[1][0]
        params = branch[1][1:]
        body = branch[2]
        res = ("user_func", params, body, frame)
    else:
        raise SchemeEvaluationError("Bad define form")

    if not is_var_name(var_name):
        raise SchemeNameError(f"Invalid variable name: {var_name}")

    frame.set(var_name, res)
    return res


def run_lambda(branch, frame):
    """Handles (lambda (params) body). Returns closure tuple."""
    if len(branch) > 3:
        raise SchemeEvaluationError("Lambda accepts only params and body")

    params = branch[1]
    body = branch[2]
    return ("user_func", params, body, frame)

def run_if(branch, frame):
    if len(branch) != 4:
        raise SchemeEvaluationError("bad")
    if evaluate(branch[1]):
        return branch[2]
    return branch[3]   

def run_and(branch, frame):
    for val in branch[1:]:
        if not evaluate(val):
            return False
    return True

def run_or(branch, frame):
    for val in branch[1:]:
        if evaluate(val):
            return True
    return False
        
SPECIAL_BUILTINS = {"define": run_define, 
                    "lambda": run_lambda,
                    "if": run_if,
                    "and": run_and,
                    "or": run_or}


# ==============================================================================
#                                Tokenization
# ==============================================================================
def tokenize(source):
    """
    Takes source, a string, and returns a list of individual token strings.
    Ignores comments and whitespace.

    >>> tokenize(' + ')
    ['+']
    >>> tokenize('-867.5309')
    ['-867.5309']
    >>> s = "((parse   these \n tokens) ;but ignore comments\n here );)"
    >>> tokenize(s)
    ['(', '(', 'parse', 'these', 'tokens', ')', 'here', ')']
    """
    result = []
    build = ""
    operators = ["*", "+", "-", "/"]
    par = False
    comment = False

    def add_to_result(build, result):
        if build:
            result.append(build)
            build = ""
        return result, build

    break_char = [" ", "\n", ";"]
    for index, char in enumerate(source):
        if comment or (char in break_char):
            # do nothing
            if ((char == "\n") and comment) or char == ";":
                comment = not comment
            result, build = add_to_result(build, result)
            continue

        # Handle parentheses immediately
        if char in ["(", ")"]:
            # If a token was being built (number or variable), finalize it first
            result, build = add_to_result(build, result)
            result.append(char)
            par = not par
            continue

        if char in operators:
            # Handle negative numbers vs subtraction operator
            if (char == "-") and (source[index + 1] not in string.whitespace):
                build += char
                continue
            result, build = add_to_result(build, result)
            result.append(char)
            continue

        build += char

    result, build = add_to_result(build, result)
    return result


# ==============================================================================
#                                   Parsing
# ==============================================================================


def parse(tokens):
    (
        """
    Parse a flat list of token strings into nested Python values:
      - numbers -> int/float via number_or_symbol
      - symbols -> str via number_or_symbol
      - parenthesized s-exprs -> Python lists

    This returns a single expression (not a stream).
    """
        """
    Parses a list of token strings and outputs a tree-like representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Hint: Make use of number_or_symbol imported from scheme_utils

    >>> parse(['+'])
    '+'
    >>> parse(['-867.5309'])
    -867.5309
    >>> parse(['(', '(', 'parse', 'these', 'tokens', ')', 'here', ')'])
    [['parse', 'these', 'tokens'], 'here']"""
    )
    end = len(tokens)

    def parse_at(index):
        if index >= end:
            raise SchemeSyntaxError("Unexpected EOF")
        token = tokens[index]

        if token == "(":
            result = []
            index += 1
            while index < end and tokens[index] != ")":
                expr, index = parse_at(index)
                result.append(expr)

            if index >= end or tokens[index] != ")":
                raise SchemeSyntaxError("Unmatched '('")
            return result, index + 1

        elif token == ")":
            raise SchemeSyntaxError("Unexpected ')'")
        else:
            return number_or_symbol(token), index + 1

    parsed, next_index = parse_at(0)

    if next_index != end:
        raise SchemeSyntaxError("Extra tokens after expression")
    return parsed


# ==============================================================================
#                                  Evaluation
# ==============================================================================


def is_var_name(name):
    if any(char in name for char in string.whitespace):
        return False
    if ";" in name:
        return False
    return True


class Scheme:
    """Represents an environment frame with parent linkage."""

    def __init__(self, parent_frame=None, built_ins=None):
        self.built_ins = built_ins if built_ins is not None else {}
        self.parent = parent_frame

    def get(self, item):
        if item in self.built_ins:
            return self.built_ins[item]
        elif self.parent is not None:
            return self.parent.get(item)
        else:
            raise SchemeNameError(f"Unbound name: {item}")

    def set(self, name, value):
        self.built_ins[name] = value


initial_frame = Scheme(None, SCHEME_BUILTINS)


def make_initial_frame():
    return Scheme(initial_frame)


def evaluate(branch, frame=make_initial_frame()):
    """
    Given tree, a fully parsed expression, evaluates and outputs the result of
    evaluating expression according to the rules of the Scheme language.

    >>> evaluate(6.101)
    6.101
    >>> evaluate(['+', 3, ['-', 3, 1, 1], 2])
    6
    """

    if isinstance(branch, (int, float)):
        return branch
    if isinstance(branch, str):
        return frame.get(branch)

    if not isinstance(branch, list) or len(branch) == 0:
        raise SchemeEvaluationError("Bad expression")

    # Evaluate Operator
    operator = branch[0]
    if isinstance(operator, str) and operator in SPECIAL_BUILTINS:
        return SPECIAL_BUILTINS[operator](branch, frame)

    func = evaluate(operator, frame)
    args = [evaluate(arg, frame) for arg in branch[1:]]

    # Built-in call
    if func in SCHEME_BUILTINS.values():
        try:
            return func(*args)
        except TypeError as exc:
            raise SchemeEvaluationError("Argument mismatch for builtin") from exc

    # User-defined Lambda call
    if isinstance(func, tuple) and func[0] == "user_func":
        _, params, body, closure_env = func

        if len(args) != len(params):
            raise SchemeEvaluationError("Argument mismatch")

        # Lexical Scoping: Parent is closure_env, NOT current frame
        call_frame = Scheme(parent_frame=closure_env, built_ins=dict(zip(params, args)))
        return evaluate(body, call_frame)

    raise SchemeEvaluationError(f"Not a function: {operator}")


# endregion
####################################################################
# region                       REPL
####################################################################

if __name__ == "__main__":
    run_doctest = False
    run_repl = True

    if run_doctest:
        _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        doctest.run_docstring_examples(tokenize, globals(), optionflags=_doctest_flags)
        # doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    if run_repl:
        sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
        SchemeREPL(
            sys.modules[__name__], verbose=True, repl_frame=make_initial_frame()
        ).cmdloop()

    # tokenize("(cat (dog (tomato)))")
    # """print(tokenize
    #     (;add the numbers 2 and 3
    #     (+ ; this expression
    #     2    ; spans multiple
    #     3    ; lines

    #     )))"""
    # print(parse(tokenize("(cat (dog (tomato)))")) )
    # print(parse(['2']))
    # print(parse(['x']))
    # print(parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')']))
    # endregion
    # print(evaluate(parse(tokenize(("+ 2 3")))))
    # print(parse(tokenize(("define pi 3.14"))))
    # print(evaluate([5, 4]))
    # evaluate(parse(tokenize('((lambda (x y) (* x y)) 1 2 3)')))
    # print(tokenize('bare-name'))
    # """print(parse(['bare-name']))
    # print(parse(['(', 'spam', ')']))
    # print(parse(['(', 'john', 'paul', 'george', 'ringo', ')']))"""
    # print(parse(['(', 'lambda', '(', 'r', ')', '(', '*', '3.14', '2', ')', ')']))
    # print(parse(['(', 'nested', '(', 'expressions', '(', 'test', ')', '
    # (', 'is', 'here', ')', '(', '(', '(', '(', 'now', ')', ')', ')', ')', ')', ')']))
    # print(parse(['(', '(', 'parse', 'these', 'tokens', ')', 'here', ')']))
#     print(evaluate(
#   ['define', 'addN', ['lambda', ['n'], ['lambda', ['i'], ['+', 'i', 'n']]]]))
#     print(evaluate(['define', 'add7', ['addN', 7]]))
#     print(evaluate(['add7', 2]))
#     print(evaluate(['add7', [['addN', 3], [['addN', 19], 8]]]))"""

#     print(evaluate(["o", 9, 4, ["-", ["+", 3, 2]]]))
