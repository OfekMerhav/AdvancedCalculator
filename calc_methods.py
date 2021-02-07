from calculator_variables import *
from arithmetic_operations import *

"""
                             CALC_METHODS
    A modulo which includes helping methods for the calculator solver modulo

"""


def is_digit(var):
    # return whether the given char is a digit or not
    return var in DIGITS


def strongest_operator_position(exercise):
    """
    :param exercise: string representing an exercise
    :return: Returns the index of the leftest most powerful operator
    in the given exercise
    """
    # default values
    max_op_pos = -1
    max_weight = -float('inf')

    # search for the strongest operator in the given exercise
    for char_index in range(0, len(exercise)):

        # operators that are not minus for value as -5 or + for e as 2e+2
        if is_operator(exercise[char_index]) and not is_negative_minus(
                exercise, char_index) \
                and exercise[char_index-1] is not 'e':

            current_op_weight = get_weight(exercise[char_index])
            if current_op_weight > max_weight:
                max_op_pos = char_index
                max_weight = current_op_weight
    # If no operators were found return None
    if max_op_pos == -1:
        return None

    return max_op_pos


def get_rightest_parentheses(exercise):
    """
    :param exercise: string representing an exercise
    :return: Return a tuple with the index of the beginning
            and the ending of the rightest parentheses in the exercise
    example: For:(4+5)+(3+(2-1)) -> returns (9,13) for (2-1)
    """
    # default flag indexes
    parentheses_open_ind = -1
    parentheses_close_ind = -1
    # Search for the rightest parentheses in the exercise
    for component_index in range(len(exercise)):
        if is_opening_parentheses(exercise[component_index]):
            parentheses_open_ind = component_index

            # If opening parentheses found,search for it's closing parentheses
            for j in range(component_index, len(exercise)):
                if is_closing_parentheses(exercise[j]):
                    parentheses_close_ind = j
                    break

    # If no parentheses were found return None
    if parentheses_close_ind is -1:
        return None

    return parentheses_open_ind, parentheses_close_ind


def is_negative_minus(exercise, op):
    """
     :param exercise: string representing an exercise
     :param op: index of an operator
     :return: Return whether the operator represents a negative minus
     example: the minus for: -5, 5+-2 are negative minuses
    """

    """
    If the operator is minus ,At the start of the exercise 
    or to the right of other operator return True, get_left_num function return 
    the same index of the given operator in cases like this
    """
    return exercise[op] is '-' and get_left_num(exercise, op)[0] == op


def get_left_num(exercise, op_index):
    """
    :param exercise: string representing the exercise
    :param op_index: index of an operator
    :return: Returns a tuple representing the indexes of the start and the end
    of the number to the left of the given operator
    (the end index of the left number is one index after the last
    digit of the number)
    example: for 55+4 --> returned indexes: 0,2
    """
    operator = exercise[op_index]
    # sets the default to the start of the exercise
    start_index_of_left_num = 0
    # set to the index of the expected end of the left number
    end_index_of_left_num = op_index - 1

    if end_index_of_left_num is 0:
        # when operator is the minus in: [-3]+3
        if is_opening_calc_brackets(exercise[end_index_of_left_num]):
            start_index_of_left_num = end_index_of_left_num + 1
            return start_index_of_left_num, end_index_of_left_num

    # when operator is the power in: [-3]^3 , returns 0
    if is_closing_calc_brackets(exercise[end_index_of_left_num]):
        close_bar_index = end_index_of_left_num
        # search for the open bracket
        for j in range(close_bar_index, -1, -1):
            if is_opening_calc_brackets(exercise[j]):
                open_bar_index = j
                return open_bar_index, end_index_of_left_num

    # Runs leftwards from the end of the number until it finds
    # char indicating the start of the number
    for component_index in range(end_index_of_left_num, -1, -1):
        if get_weight(operator) > get_weight('-'):

            # searches for char indicating the start of the left number
            # if the weight of the operator is stronger then minus,
            # don't include negative minus in the number: -2^2 -> -4
            if is_operator(exercise[component_index]) and exercise[
                component_index - 1] is not 'e' \
                    or is_opening_calc_brackets(exercise[component_index]):

                start_index_of_left_num = component_index + 1
                break

        # Else,include negative minus in the number: -2-2 -> -4
        else:
            # searches for char indicating the start of the left number
            if is_operator(exercise[component_index]) \
                    and not is_negative_minus(exercise, component_index) \
                    and exercise[component_index - 1] is not 'e' \
                    or is_opening_calc_brackets(exercise[component_index]):

                start_index_of_left_num = component_index + 1
                break

    return start_index_of_left_num, end_index_of_left_num+1


def get_right_num(exercise, op):
    """
    :param exercise: string representing the exercise
    :param op: index of an operator
    :return: Return the start and the end indexes of the number to
    the right of the operator.
    (the end index of the right number is one index after the last
    digit of the number)
    example: for 2+2 --> returns the index 2,3
    """
    # sets the default to the start of the string
    right_num_end = len(exercise)
    # index of the start of the right number
    right_num_start = op + 1

    # if operator is the power in: '7.0^[-8.0]' , returns 9,13
    if is_opening_calc_brackets(exercise[right_num_start]):
        open_bar_index = right_num_start
        for j in range(open_bar_index, len(exercise)):

            if is_closing_calc_brackets(exercise[j]):
                close_bar_index = j
                right_num_start = open_bar_index+1
                return right_num_start, close_bar_index

    # Runs rightwards from the start of the number until it finds
    # char indicating the end of the number
    for component_index in range(right_num_start, len(exercise)):
        current_component = exercise[component_index]

        # checks for char indicating the end of the right number
        if is_operator(current_component)\
                and not is_negative_minus(exercise, component_index) \
                and exercise[component_index - 1] is not 'e':

            right_num_end = component_index
            break

    return right_num_start, right_num_end


def delete_single_in_brackets(exercise):
    """
    delete_single_in_brackets function search for numbers that are in
    a "in calculation brackets"-> [ ] ,
    it deletes the brackets around them and returns the number
    :param exercise: string representing the exercise
    :return:
    """
    component_index = 0
    # Runs over the exercise
    while component_index < len(exercise):
        # search for -> '['
        if is_opening_calc_brackets(exercise[component_index]):
            # get the indexes of the start and the end of the in calc bracket
            bracket_opener, bracket_closer = \
                get_in_calc_brackets(exercise, component_index)

            in_parentheses_number = exercise[bracket_opener+1:bracket_closer]
            # update the exercise by deleting the in calc brackets
            exercise = exercise[:bracket_opener] \
            + in_parentheses_number + exercise[bracket_closer + 1:]

        component_index = component_index+1
    return exercise


def get_in_calc_brackets(exercise, opener_bracket):
    """
    get_in_calc_brackets function is Called after founding an In calculation
    opening brackets ('[ ]') and finds it's end bracket
    Note: The function assume the given opening bracket has a closer
    :param exercise: string representing an exercise
    :param opener_bracket: start index of an In calculation opening bracket
    :return: return a tuple with the start and the end of the given
    opening brackets
    """
    # default index for the closer bracket
    closer_bracket = opener_bracket
    # Runs over the exercise from given bracket index till it finds it's closer
    for current_char in range(opener_bracket + 1, len(exercise)):
        if is_closing_calc_brackets(exercise[current_char]):
            closer_bracket = current_char
            break
    return opener_bracket, closer_bracket


def minuses_to_one(exercise):
    """
    The functions search for minus Sequences and replace them
    with the proper sign => odd number of '-' replaced by '-'
    even number of '-' will be deleted (positive number)
    :param exercise: string representing the exercise
    :return: Return the new , fixed exercise
    """
    minuses_counter = 0
    flag = 1
    component_index = len(exercise)
    # Iterates over the exercise from the end to the start
    while component_index > 0:
        component_index = component_index-1
        # if its not an operator or an operator that comes from left like '~'
        if not is_operator(exercise[component_index]) or (
                is_operator(exercise[component_index]) and get_op_side(
                exercise[component_index]) is 'LEFT'):

            # if it has minus before it, run leftwards and change
            # the minus sequences accordingly
            if exercise[component_index-1] is '-':
                for j in range(component_index-1, -1, -1):
                    # 5'+'---3
                    if is_operator(exercise[j]) and exercise[j] is not '-':
                        if flag is -1:
                            exercise = exercise[0:j + 1] + '-' + exercise[
                                                            component_index:]
                        else:
                            exercise = exercise[0:j + 1] + exercise[
                                                           component_index:]
                        component_index = j+1
                        break

                    # 5---3 --> 5-3 || 5----3 --> 5--3
                    if not is_operator(
                            exercise[j]) and not is_opening_parentheses(
                            exercise[j]):

                        if flag is 1 and minuses_counter > 1:
                            exercise = exercise[0:j + 2] + '-' + exercise[component_index:]
                        else:
                            exercise = exercise[0:j+2]+exercise[component_index:]
                        component_index = j+1
                        break

                    # (--3+1) --> (3+1) || (---3+1) --> (-3+1)
                    if is_opening_parentheses(exercise[j]):
                        if flag is -1:
                            exercise = exercise[0:j + 1] + '-' + exercise[component_index:]
                        else:
                            exercise = exercise[0:j+1]+exercise[component_index:]
                        component_index = j+1
                        break

                    # minus sequence at the start of the exercise
                    if j is 0:
                        # -5 --> -5
                        if minuses_counter is 0:
                            exercise = '-' + exercise[component_index:]
                        else:
                            # ---4 --> -4 | --4 --> 4
                            if minuses_counter > 0 and flag is 1:
                                exercise = '-' + exercise[component_index:]
                            # --4 --> 4
                            else:
                                exercise = exercise[component_index:]
                        component_index = j
                        break

                    minuses_counter = minuses_counter + 1
                    flag = flag * -1
                minuses_counter = 0
                flag = 1
    return exercise


def get_rightest_left_op(exercise, current_left_op):
    """
    get_rightest_left_op function is called when the operator
    to be solved is a "left operator" , it searches for the
    closest "left operator" to the number to the right
    example: ~-~-(5+1) --> index 0 will be given , index 2 will be returned

    :param exercise: string representing the exercise
    :param current_left_op: index of a left,strongest operator in the exercise
    :return: Index of the closest "left operator" to the number
    """
    # set the default rightest "left operator" to the given operator
    rightest_left_op = current_left_op
    # Iterates over the exercise from the given operator to the number
    # or any other expression to the right of it
    for component_index in range(current_left_op+1, len(exercise)):

        # when arriving the expression after the operators,finish searching
        if not is_operator(exercise[component_index]):
            break

        if is_operator(exercise[component_index]) and get_op_side(
                exercise[component_index]) is "LEFT":

            # if there is a "left operator" weaker then the given operator,
            # raise an exception
            if get_weight(exercise[current_left_op]) > get_weight(
                    exercise[component_index]):
                raise RunTimeError("Illegal position for left operator")
            # Else, set the rightest operator to it
            rightest_left_op = component_index

    return rightest_left_op
