from calc_methods import *
from calculator_variables import *
from exceptions import *

"""
                              Validations
            modulo for validations checking over a given exercise 
        considering the order of operations and the rules of mathematics

"""


def execute_validation(exercise):
    """
    The function operates the validation functions for the given exercise
    :param exercise: string representing an exercise
    :return:
    """

    check_parentheses_normalcy(exercise)
    check_unnecessary_parentheses(exercise)
    # Look for minus sequences and make changes accordingly
    exercise = minuses_to_one(exercise)
    search_for_illegal_one_arg_op(exercise)
    search_for_illegal_middle_op(exercise)
    check_for_invalid_operators_sequence(exercise)
    check_around_floating_point(exercise)


def check_for_invalid_operators_sequence(exercise):
    """
    check_for_invalid_operators_sequence function checks whether there are
    two or more operators next to each other in an illegal order.
    If any were found, it raises an exception with the specified error .

    :param exercise: string representing an exercise
    :return:
    """

    # Run over the exercise
    for component_index in range(0, len(exercise)-1):

        # indexes of the left and right chars next to the current char
        left_index = component_index - 1
        right_index = component_index + 1
        # the left and right chars next to the current char
        left_char = exercise[left_index]
        right_char = exercise[right_index]
        # the current component in the exercise
        current_component = exercise[component_index]

        if is_operator(current_component):
            current_operator = current_component

            # Check illegal sequence around middle operators
            if get_op_side(current_operator) is "MIDDLE":
                # ex: num (op_X)(middle_op X+Y)num2 --> X,Y for weights
                if is_operator(left_char):
                    if get_weight(left_char) < get_weight(current_operator):
                        raise ValidationError(
                            "Invalid operators location" +
                            operators_error_string(exercise, left_index,
                                                   component_index))

                # if the right char to the middle operator is an operator
                # and not a minus representing negativity
                if is_operator(right_char) and not is_negative_minus(
                        exercise, right_index):
                    # if its not a left type of operator, raise exception
                    # ex: num ++ num2
                    if get_op_side(right_char) is not "LEFT":
                        raise ValidationError(
                            "ERROR: doubled Middle Operators" +
                            operators_error_string(exercise, component_index,
                                                   right_index))

                    # ex: num (m_op(X))(op(X/X-Y)) num2 --> X,Y for weights
                    elif get_weight(right_char) <= get_weight(current_operator):
                        raise ValidationError(
                            "ERROR: left operator is weaker then the middle "
                            "operator before it" +
                            operators_error_string(exercise, component_index,
                                                   right_index))

            # Check illegal sequence around Right operators
            if get_op_side(current_operator) is "RIGHT":

                if is_operator(right_char):
                    # ex:  5!~2
                    if get_op_side(right_char) is "LEFT":
                        raise ValidationError(
                            "ERROR: left operator cant appear after "
                            "right operator"
                            + operators_error_string(exercise, component_index,
                                                     right_index))

                    # ex: num(right_op(X))(right_op(X+Y)) --> X,Y for weights
                    elif get_op_side(right_char) is "RIGHT":
                        if get_weight(current_operator) < get_weight(
                                right_char):
                            raise ValidationError(
                                "ERROR: second right operator is stronger then"
                                " the first" + operators_error_string(
                                    exercise, component_index, right_index))

            # Check illegal sequence around left operators
            if get_op_side(current_operator) is "LEFT":

                # ex: ~+1
                if is_operator(right_char) \
                        and get_op_side(right_char) is not "LEFT" \
                        and not is_negative_minus(exercise, component_index+1):

                    raise ValidationError(
                        "Right/Middle operator cant appear after left operator"
                        + operators_error_string(exercise, component_index,
                                                 right_index))

                # ex: (left_op(X+Y))(left_op(X))num --> X,Y for weights
                if is_operator(right_char) and get_op_side(right_char)is'LEFT':
                    if get_weight(current_operator) > get_weight(right_char):
                        raise ValidationError(
                            "ERROR: first left operator is stronger then "
                            "the second" + operators_error_string(
                                exercise, component_index, right_index))


def search_for_illegal_one_arg_op(exercise):
    """
    search_for_illegal_one_arg_op function searches for illegal positions of
    a "single operand operators".
    If any was found, it raises an exception accordingly.

    example: !4, 4!5, ~1, 1~5, 5~+3
    :param exercise: string representing an exercise
    :return:
    """
    first_char = exercise[0]
    last_char = exercise[len(exercise)-1]

    # ex: (right_op)num --> right operator at the beginning of the exercise
    if is_operator(first_char) and get_op_side(first_char) is "RIGHT":
        raise ValidationError("ERROR: Right operator cant appear"
                              " at the beginning of the exercise" +
                              operator_error_string(exercise, 0))

    # ex: num(left_op) --> left operator at the end of the exercise
    if is_operator(last_char):
        if get_op_side(last_char) is "LEFT":
            error_str = "ERROR: Left operator cant " \
                        "appear at the end of the exercise"
            raise ValidationError(
                error_str + operator_error_string(exercise, len(exercise) - 1))

    # Run over the string with out the first and last chars
    for component_index in range(1, len(exercise)-1):

        current_char = exercise[component_index]
        if is_one_arg_op(current_char):
            current_op = current_char

            # ex: 5+!5
            if get_op_side(current_op) is 'RIGHT' and is_digit(
                    exercise[component_index + 1]):
                error_str = "ERROR: An operand cant appear after " \
                            "a right operator"
                raise ValidationError(
                    error_str + operator_error_string(exercise,
                                                      component_index))

            # ex: 5~+3
            if get_op_side(
                    exercise[component_index]) is 'LEFT' and is_digit(
                    exercise[component_index - 1]):
                error_str = "ERROR: An operand cant appear before "\
                                      "a left operator"
                raise ValidationError(error_str+operator_error_string(exercise,
                                                      component_index))


def search_for_illegal_middle_op(exercise):
    """
    search_for_illegal_middle_op function searches for missing arguments
    around middle operators.
    If any was found, it raises an exception accordingly.

    :param exercise: string representing an exercise
    :return:
    """
    # +4+5
    if is_operator(exercise[0]) and get_op_side(exercise[0]) is "MIDDLE":
        if not is_negative_minus(exercise, 0):
            error_str = "Missing operand to the left of the operator"
            raise ValidationError(error_str+operator_error_string(exercise, 0))
    # 4+5+
    last_index = len(exercise) - 1
    if is_operator(exercise[last_index]) and get_op_side(
            exercise[last_index]) is "MIDDLE":
        error_str = "Missing operand to the right of the operator"
        raise ValidationError(
            error_str + operator_error_string(exercise, last_index))


def check_parentheses_normalcy(exercise):
    """
    check_parentheses_normalcy function checks:
    - whether there are any missing Parentheses.
    - whether there are any Parentheses in the exercise,
     (not at start or at the end of it) that has no operators
     before and after them.
    - whether there are any operators next to parentheses in illegal way.
      example: (1!(1+1))
    :param exercise: string representing an exercise
    :return:
    """
    open_count = 0
    close_count = 0
    # checks whether each open Parentheses has closing Parentheses
    for component_index in range(0, len(exercise)):
        if is_opening_parentheses(exercise[component_index]):
            open_count = open_count+1
        if is_closing_parentheses(exercise[component_index]):
            close_count = close_count + 1
            if close_count > open_count:
                raise ValidationError(
                    "Missing opening Parentheses to closing Parentheses" +
                    char_error_string(exercise, component_index))

    # in case the number of closing and opening parentheses aren't equal,
    # there are missing closer parentheses
    if open_count != close_count:
        raise ValidationError(
            "Missing closing Parentheses to opening Parentheses")

    # last char in exercise
    last_pos = len(exercise) - 1
    if is_closing_parentheses(exercise[last_pos]):
        # # (3+) || (2~)
        if is_operator(exercise[last_pos - 1]) \
                and get_op_side(exercise[last_pos - 1]) is not 'RIGHT':
            raise ValidationError("Illegal position for Operator" +
                                  operator_error_string(exercise, last_pos-1))
    # first char in exercise
    first_pos = 0
    if is_opening_parentheses(exercise[first_pos]):
        # (+3) || (!2) --> operators next to opening parentheses
        # which aren't left operators
        if is_operator(exercise[1]) and (get_op_side(
                exercise[1]) != 'LEFT' and exercise[1] is not '-'):
            raise ValidationError("Illegal position for Operator" +
                                  operator_error_string(exercise,
                                                        1))
    # Checks whether there are any missing operators around parentheses
    # example: 4-4(3+1)
    for component_index in range(1, len(exercise)-1):
        current_char = exercise[component_index]

        left_index = component_index - 1
        left_to_parentheses = exercise[component_index - 1]
        right_index = component_index + 1
        right_to_parentheses = exercise[component_index + 1]

        # check around opening parentheses: '('
        if is_opening_parentheses(current_char):
            # ~($5$8)
            if is_operator(right_to_parentheses) and get_op_side(
                    right_to_parentheses) is not "LEFT" and right_to_parentheses is not '-':
                raise ValidationError("Illegal position for Operator" +
                                      operator_error_string(exercise, right_index))

            # 4!(3+1)
            if is_operator(left_to_parentheses) and get_op_side(
                    left_to_parentheses) is "RIGHT":
                raise ValidationError("Illegal position for right Operator" +
                                      operator_error_string(exercise, left_index))
            # 4(3+1)
            if not is_operator(
                    left_to_parentheses) and not is_opening_parentheses(
                    left_to_parentheses):
                raise ValidationError("Missing Operators Around Parentheses" +
                                      char_error_string(exercise, component_index))

        # check around closing parentheses: ')'
        if is_closing_parentheses(current_char):
            # (1+2)~1
            if is_operator(right_to_parentheses):
                if get_op_side(right_to_parentheses) is "LEFT":
                    raise ValidationError("Illegal position for Operator" +
                                 operator_error_string(exercise, right_index))
            # (1+2)(2+1) || (1+2)4
            elif not is_closing_parentheses(right_to_parentheses):
                raise ValidationError("Missing Operators Around Parentheses" +
                                      operator_error_string(exercise, component_index))
            # (1+1+)+2 || (2+2^)+2
            if is_operator(left_to_parentheses) \
                    and get_op_side(left_to_parentheses) is not "RIGHT":
                raise ValidationError("Illegal position for Operator" +
                                      operator_error_string(exercise, left_index))


def check_around_floating_point(exercise):
    """
    check_around_floating_point function Checks whether
    each floating point has digits in it's both sides and whether each number
    has one floating point
    example for invalid numbers: 2..2 , 2.3.2
    :param exercise:
    :return:
    """
    # Flag that indicates whether each number was separated by
    # operator before being connected with a dot again --> 2.2.2
    multiple_connectors_flag = False
    for component_index in range(0, len(exercise)):

        # Each operator reset the Flag to true
        if is_operator(exercise[component_index]):
            multiple_connectors_flag = False

        # '.' detected
        if is_number_connector(exercise[component_index]):
            if multiple_connectors_flag is False:
                # set flag to True
                multiple_connectors_flag = True
                # number connector cant appear at the start or the
                # end of the exercise
                if component_index == len(exercise)-1 or component_index == 0:
                    raise ValidationError("Invalid Floating point")

                # Only digits can surround a number connector
                if not is_digit(exercise[component_index-1]) \
                        or not is_digit(exercise[component_index+1]):
                    raise ValidationError("Invalid Floating point")
            # If the multiple_connectors_flag is on (True)
            # then the number is illegal --> 2.2.2
            else:
                raise ValidationError("Invalid Floating point")


def check_unnecessary_parentheses(exercise):
    """
    check_unnecessary_parentheses function checks if there are any unnecessary
    parentheses in the given exercise
    example: ((9+5))
    :param exercise:
    :return:
    """
    # In each loop cycle, expression is deleted with the parentheses around it
    # if empty parentheses are left,unnecessary parentheses are found
    while True:
        if exercise is '':
            break
        open_close_brackets = get_rightest_parentheses(exercise)
        if open_close_brackets is not None:

            # indexes of open and close parentheses
            open_parentheses = open_close_brackets[0]
            close_parentheses = open_close_brackets[1]

            # If empty parentheses were left,raise exception
            if open_parentheses == close_parentheses-1:
                raise ValidationError("ERROR: Unnecessary_parentheses")

            # delete the expression with the parentheses surrounding it
            left_side = exercise[:open_parentheses]
            right_side = exercise[close_parentheses+1:]
            exercise = left_side + right_side
        else:
            break


""""""""""""""""""" ERROR STRINGS METHODS FOR EXCEPTIONS """""""""""""""""""""


def operators_error_string(exercise, left_op_index, right_op_index):
    """
    Called when validation errors are detected and two operators has to be
    specified
    :param exercise: string representing the exercise
    :param left_op_index: index of first operator
    :param right_op_index: index of second operator
    :return:
    """
    # return a string presenting the given operators
    return "\nfirst operator: " + exercise[left_op_index] + " index:" + str(
                            left_op_index) + "\nsecond operator: " + exercise[
                            right_op_index] + " index:" + str(right_op_index)


def operator_error_string(exercise, operator_index):
    """
    Called when validation errors are detected and one operator has to be
    specified
    :param exercise: string representing the exercise
    :param operator_index: index of operator
    :return:
    """

    # return a string presenting the given operator
    return "\noperator : " + exercise[operator_index] + " index:" + str(
        operator_index)


def char_error_string(exercise, char_index):
    """
    Called when validation errors are detected and a char has to be
    specified
    :param exercise:
    :param char_index:
    :return:
    """
    # Return a string presenting the given char
    return "\nchar : " + exercise[char_index] + " index:" + str(
        char_index)



