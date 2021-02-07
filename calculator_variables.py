
"""
                          calculator_variables
       modulo which contains the calculator variables

"""


""""""""""""""""""""""""" CALCULATOR VARIABLES """""""""""""""""""""

# WARNING: Don't include brackets ([]) in the opening/closing set
opening_parentheses_set = ['(']
closing_parentheses_set = [')']

IN_CALCULATION_OPENING_BRACKETS = '['
IN_CALCULATION_CLOSING_BRACKETS = ']'

NUMBERS_CONNECTOR = '.'

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


""""""""""""""""""" CALCULATOR VARIABLES METHODS """""""""""""""""""""


def is_opening_parentheses(char):
    return char in opening_parentheses_set


def is_closing_parentheses(char):
    return char in closing_parentheses_set


def is_opening_calc_brackets(char):
    return char is IN_CALCULATION_OPENING_BRACKETS


def is_closing_calc_brackets(char):
    return char is IN_CALCULATION_CLOSING_BRACKETS


def is_number_connector(char):
    return char == NUMBERS_CONNECTOR








