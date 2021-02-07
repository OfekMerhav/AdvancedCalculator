from calc_methods import *

"""
                                InputHandler
        deletes white spaces from the input and checks the input integrity
                          by means of invalid syntax 
                        
"""


def handle_input(exercise):
    # remove empty spaces as ' ' and tabs
    exercise = remove_empty_spaces(exercise)
    # check integrity of the input
    check_if_empty(exercise)
    search_illegal_input(exercise)

    return exercise


def remove_empty_spaces(string_to_change):
    """
    :param string_to_change:
    :return: Returns the received string without empty spaces
    """
    # delete empty spaces and tabs
    string_to_change = string_to_change.replace(" ", "")
    string_to_change = string_to_change.replace("\t", "")
    return string_to_change


def check_if_empty(exercise):
    """
    check_if_empty function raises exception if the input is empty
    (being operated after empty spaces removal
    :param exercise: string representing an exercise
    :return:
    """
    if exercise is '':
        raise ValidationError("ERROR: Empty input")


def search_illegal_input(exercise):
    """
    search_illegal_input function checks whether there are any chars in the
    input that are illegal to the calculator (aren't knows as operators,digits,
    parentheses,or number connectors)

    :param exercise: string representing an exercise
    :return:
    """
    for component_index in range(len(exercise)):
        current_component = exercise[component_index]
        if not is_operator(current_component) \
                and not is_digit(current_component) \
                and not is_opening_parentheses(current_component) \
                and not is_closing_parentheses(current_component)\
                and not is_number_connector(current_component):
            raise ValidationError("ERROR: Unsupported input chars")


