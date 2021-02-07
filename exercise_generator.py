from random import *
import validations
from input_handler import *

# list which contains all of the structures that contain
# the valid input for the calculator
variables = [arithmetic_methods, arithmetic_methods, arithmetic_methods,
             opening_parentheses_set, closing_parentheses_set, DIGITS]


def get_exercise(length):
    # generate exercise with half of the wanted length
    exercise = generate_exercise('', int(length/2))
    # generate exercise
    exercise = generate_exercise(exercise, length)
    return exercise


def generate_exercise(exercise, length):
    """
    generate_exercise method creates an exercise randomly with the given length
    :param exercise: string representing an exercise (if the given exercise is
    not empty , it will be filled to the wanted length
    :param length:
    :return:
    """
    if length == 0:
        return exercise

    constant_ex = exercise
    while True:
        exercise = constant_ex
        for i in range(0, length-len(constant_ex)+1):
            if len(exercise) == length:
                try:
                    handle_input(exercise)
                    validations.execute_validation(exercise)
                    return exercise
                except Exception:
                    break

            char = get_char()
            exercise = exercise + char


def get_char():
    """
    get_char function selects randomly a char from a list containing all of the
    input valid possibilities

    example: if arithmetic_methods are chosen within the list the method will
    also select a method inside the arithmetic_methods dictionary and return it

    :return: selected char from the list
    """
    # choose a structure containing some valid input
    chosen_one = choice(variables)
    # set a limit for the in structure random selecting
    limit = len(chosen_one)-1
    num = randint(0, limit)
    # if the operators dictionary was selected,choose randomly operator
    if type(chosen_one) is dict:
        chosen_one = dict(chosen_one).keys()
        num = randint(0, len(chosen_one)-1)
        counter = 0
        for i in chosen_one:
            if counter is num:
                chosen_one = i
                break
            else:
                counter = counter+1
        return chosen_one
    chosen_one = chosen_one[num]
    return chosen_one



