from exceptions import *
from calculator_variables import *


""""""""""""""""""""""""" ARITHMETIC METHODS """""""""""""""""""""


def add(num1, num2):
    return return_number(num1 + num2)


def sub(num1, num2):
    return return_number(num1 - num2)


def mul(num1, num2):
    return return_number(num1 * num2)


def div(num1, num2):
    return return_number(num1 / num2)


def power(num1, num2):
    return return_number(num1 ** num2)


def negative(num):
    return return_number(-num)


def modulo(num1, num2):
    return return_number(num1 % num2)


def factorial(num):

    # there is no factorial for a negative and fraction number
    if num < 0:
        raise RunTimeError("MATH ERROR: Factorial for negative number")
    if num % 1 != 0:
        raise RunTimeError("MATH ERROR: Factorial for fraction number")

    # The limit for a number factorial calculation
    if num >= 170:
        raise RunTimeError(
            "MATH ERROR: Factorial for the number " + str(num) + " is too big")

    # calculate the number factorial
    result = 1
    for i in range(1, int(num+1)):
        result *= i
    return return_number(result)


def average(num1, num2):
    return return_number(float((num1 + num2) / 2))


def maximum(num1, num2):
    return return_number(num1) if num1 > num2 else return_number(num2)


def minimum(num1, num2):
    return return_number(num1) if num1 < num2 else return_number(num2)


def return_number(result):
    """
    return_number function is called by each of the arithmetic methods,
    it's role is to wrap a negative result in "in calc brackets" -> [ ]
    :param result: result of an arithmetic methods
    :return: return the result after changes if needed
    """
    # if the number is complex, raise exception
    if isinstance(result, complex):
        raise RunTimeError("MATH ERROR: No solution, complex number")
    # in case of inf result, raise proper exception
    if float(result) == float('inf') or result == float('-inf'):
        raise RunTimeError("MATH ERROR: Result was too big")
    # wrap the negative result in "in calc brackets"
    if result < 0:
        return IN_CALCULATION_OPENING_BRACKETS + str(result) + \
               IN_CALCULATION_CLOSING_BRACKETS
    return str(result)


"""""""""""""""""""""" CALCULATOR OPERATORS DICTIONARY """""""""""""""""""""

"""
    arithmetic_methods it's a dictionary structure for the arithmetic operators
    Each operator has a delegate for it's method,it's weight and it's side
    relative to the number/numbers he operates on

    key: operator char
    value: method, weight, side of the operator

    Note: For future changes add a single char representing operator
"""
arithmetic_methods = {

    '+': (add, 1, "MIDDLE"),
    '-': (sub, 1, "MIDDLE"),
    '*': (mul, 2, "MIDDLE"),
    '/': (div, 2, "MIDDLE"),
    '^': (power, 3, "MIDDLE"),
    '~': (negative, 6, "LEFT"),
    '%': (modulo, 4, "MIDDLE"),
    '!': (factorial, 6, "RIGHT"),
    '@': (average, 5, "MIDDLE"),
    '$': (maximum, 5, "MIDDLE"),
    '&': (minimum, 5, "MIDDLE")

}

""""""""""""""""""" CALCULATOR OPERATORS METHODS """""""""""""""""""""


def get_op_side(operator):
    """
    :param operator: char representing an operator
    :return: returns the side of the given operator relative to
     the number/numbers he operates on
    """
    return arithmetic_methods[operator][2]


def get_weight(operator):
    """
    :param operator: char representing an operator
    :return: returns the weight of the given operator
    """
    return arithmetic_methods[operator][1]


def is_operator(char):
    """
    :param char:
    :return: returns whether the char represents an operator
    """
    return char in arithmetic_methods.keys()


def is_one_arg_op(char):
    """
    :param char:
    :return: returns True/False if the operator operates on a single
    argument or not
    """
    # if the given char isn't operator, return False
    if not is_operator(char):
        return False
    return arithmetic_methods[char][2] != "MIDDLE"


def run_arithmetic_method(operator, num1, num2=0):
    """
    :param operator: The wanted arithmetic method to be executed
    :param num1:
    :param num2: if the operator is a one argument operator num2 set to 0 as
    default
    :return: Returns the result of the executed arithmetic method
    """
    try:
        if is_one_arg_op(operator):
            return arithmetic_methods[operator][0](num1)
        else:
            return arithmetic_methods[operator][0](num1, num2)
    except OverflowError:
        raise ValidationError("solution is too big")
    except RunTimeError as RT:
        raise RT