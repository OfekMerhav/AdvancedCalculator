from calc_methods import *

"""
                             Calculator_Solver
        modulo for solving a given arithmetic expression by the order
         of operations using the methods from the Calc_Method modulo

"""


def solve_exercise(exercise):
    """
    solve_exercise function solves the given exercise by the order of operations
    considering parentheses and the strength of each operator
    :param exercise:
    :return: Returns the solution to the given exercise
    """
    # Look for minus sequences and make changes accordingly
    exercise = minuses_to_one(exercise)
    # tuple of the opener and closer of parentheses
    open_close_brackets = get_rightest_parentheses(exercise)
    if open_close_brackets is not None:
        # In case parentheses were found,solve_exercise the expression
        # inside the parentheses
        return solve_exercise(
            solve_parentheses(exercise, open_close_brackets))

    strongest_op = strongest_operator_position(exercise)
    if strongest_op is not None:
        # -[-5]+1 --> --5+1 --> 5+1
        if get_weight(exercise[strongest_op]) <= get_weight('-'):
            # delete parentheses around single number
            exercise = delete_single_in_brackets(exercise)
            # Look for minus sequences and make changes accordingly
            exercise = minuses_to_one(exercise)
            # Update the operator again after changing the exercise
            strongest_op = strongest_operator_position(exercise)
        # solve_exercise the expression around the strongest operator
        if strongest_op is not None:
            return solve_exercise(solve_strongest_op(exercise, strongest_op))

    # when whats left is a number:
    # delete parentheses around single number
    exercise = delete_single_in_brackets(exercise)
    # Look for minus sequences and make changes accordingly
    exercise = minuses_to_one(exercise)
    return float(exercise)


def solve_parentheses(exercise, open_close_brackets):
    """
    solve_parentheses function gets an exercise and indexes of parentheses
    it solves the expression inside the parentheses and return the exercise
    with the parentheses solved.
    to a minus result [ ] brackets will be added
    example: (5+(2+2)) --> (5+2) ,  (5+(1-3)) --> (5+[-2])

    :param exercise: string representing an exercise
    :param open_close_brackets: indexes of the start and the end
    of parentheses
    :return:
    """

    # open and close bracket indexes
    open_parentheses = open_close_brackets[0]
    close_parentheses = open_close_brackets[1]

    # (2+1) --> 2+1
    in_parentheses_expression = exercise[open_parentheses + 1
                                         :close_parentheses]
    # the rest of the exercise to the left of the parentheses
    left_side_of_ex = exercise[:open_parentheses]
    parentheses_result = solve_exercise(in_parentheses_expression)

    # Checks whether the parentheses were at the end of the exercise
    if close_parentheses + 1 >= len(exercise):
        # solve_exercise the expression inside the parentheses
        parentheses_result = str(parentheses_result)
        exercise = left_side_of_ex + parentheses_result
        exercise = minuses_to_one(exercise)
        # return the exercise after parentheses are solved
        return exercise

    parentheses_result = return_number(parentheses_result)
    # the rest of the exercise to the right of the parentheses
    right_side_of_ex = exercise[close_parentheses + 1:]
    exercise = left_side_of_ex + str(parentheses_result) + right_side_of_ex

    # return the exercise after parentheses are solved
    return exercise


def solve_strongest_op(exercise, strongest_op):
    """
    solve_strongest_op function gets an exercise and index of
    the wanted operator to be solved , solves it and return the exercise
    with the expression solved
    example: 4+2*2 --> 4+4

    :param exercise:
    :param strongest_op:
    :return:
    """

    # the side of the operator relative to the operands it has to get
    # + -> middle || ~ -> left || ! -> right
    strong_op_side = get_op_side(exercise[strongest_op])
    if strong_op_side is not "LEFT":
        # start and end indexes of the number to the left of the operator
        left_num_start, left_num_end = get_left_num(exercise, strongest_op)
        number_to_left = exercise[left_num_start:left_num_end]
        # the rest of the exercise to the left of the expression
        left_side_of_ex = exercise[:left_num_start]

    if is_one_arg_op(exercise[strongest_op]):

        if strong_op_side is "RIGHT":
            # operators as !
            # the rest of the exercise to the right of the expression
            right_side_of_ex = exercise[strongest_op + 1:]
            answer = run_arithmetic_method(exercise[strongest_op],
                                           solve_exercise(number_to_left))

        if strong_op_side is "LEFT":  # operators as ~
            # change the left operator to the closest one to the number
            strongest_op = get_rightest_left_op(exercise, strongest_op)

            # the number to the right of the strongest operator
            right_num_start, right_num_end = get_right_num(exercise,
                                                           strongest_op)
            # The number to the right of the operator
            number_to_right = exercise[right_num_start:right_num_end]

            # 1+(1-2)+3 --> 1+[-1]+3 | right_side => +3
            if is_opening_calc_brackets(exercise[strongest_op + 1]):
                # don't include closer bracket
                right_side_of_ex = exercise[right_num_end+1:]
            else:
                right_side_of_ex = exercise[right_num_end:]

            # the rest of the exercise to the left of the expression
            left_side_of_ex = exercise[:strongest_op]
            operator = exercise[strongest_op]
            # solve_exercise the expression around the operator
            answer = run_arithmetic_method(operator, solve_exercise(number_to_right))

    # for middle operators
    else:
        right_num_start, right_num_end = get_right_num(exercise,
                                                       strongest_op)
        # the number to the right of the strongest operator
        number_to_right = exercise[right_num_start:right_num_end]

        if right_num_end == len(exercise):
            # if the right number is at the end, right side is empty
            right_side_of_ex = ''
        else:
            # 1^[-2]+2 | right_side => +2
            if is_closing_calc_brackets(exercise[right_num_end]):
                # The rest of the exercise from the right side
                right_side_of_ex = exercise[right_num_end+1:]
            else:
                # The rest of the exercise from the right side
                right_side_of_ex = exercise[right_num_end:]

        # solve_exercise the expression around the operator
        answer = run_arithmetic_method(exercise[strongest_op],
                                       solve_exercise(number_to_left),
                                       solve_exercise(number_to_right))

    # Build again the exercise after solving the wanted expression
    exercise = left_side_of_ex + str(answer) + right_side_of_ex
    return exercise

