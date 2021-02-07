from calculator_solver import *
import validations
from input_handler import *


def check_and_solve(exercise):
    """
    check_and_solve function gets an exercise, checks if it's valid and return
    the result from the solve_exercise. else, returns an error
    :param exercise:
    :return:
    """
    try:
        ex = exercise
        ex = handle_input(ex)
        validations.execute_validation(ex)
        ex = solve_exercise(ex)
        print("Exercise Solution: "+str(ex))
        return float(ex)
    except ZeroDivisionError:
        return "MATH ERROR: Zero Division"
    except OverflowError:
        return "over flow error"
    except RecursionError:
        return "Exercise has too many operators"
    except ValidationError as VE:
        # when validation error was raised
        return str(VE)
    except RunTimeError as RT:
        # when run time error was raised
        return str(RT)


def test_syntax_error1():
    assert check_and_solve("3^*2") == "ERROR: doubled Middle Operators" \
                                      "\nfirst operator: ^ index:1" \
                                      "\nsecond operator: * index:2"


def test_syntax_error2():
    assert check_and_solve("!2") == "ERROR: Right operator cant appear" \
                                    " at the beginning of the exercise" \
                                    "\noperator : ! index:0"


def test_syntax_error3():
    assert check_and_solve("4!4") == "ERROR: An operand cant appear after" \
                                     " a right operator\noperator : ! index:1"


def test_syntax_error4():
    assert check_and_solve("5(4+1)") == "Missing Operators Around " \
                                        "Parentheses\nchar : ( index:1"


def test_syntax_error5():
    assert check_and_solve("!") == "ERROR: Right operator cant appear at " \
                                   "the beginning of the exercise\noperator " \
                                   ": ! index:0"


def test_syntax_error6():
    assert check_and_solve("(5+2") == "Missing closing Parentheses to " \
                                      "opening Parentheses"


def test_syntax_error7():
    assert check_and_solve("+4+5") == "Missing operand to the left " \
                                      "of the operator\noperator : + index:0"


def test_syntax_error8():
    assert check_and_solve("~+1") == "Right/Middle operator cant appear " \
                                     "after left operator\nfirst operator:" \
                                     " ~ index:0\nsecond operator: + index:1"


def test_syntax_error9():
    assert check_and_solve("((2+1))") == "ERROR: Unnecessary_parentheses"


def test_syntax_error10():
    assert check_and_solve("2.2.2+1") == "Invalid Floating point"


def test_syntax_error11():
    assert check_and_solve("5!~2") == "ERROR: left operator cant appear " \
                                      "after right operator\nfirst operator:" \
                                      " ! index:1\nsecond operator: ~ index:2"


def test_unsupported_input_chars():
    assert check_and_solve("Calculator solver") == "ERROR: Unsupported " \
                                                   "input chars"


def test_empty_input():
    assert check_and_solve("") == "ERROR: Empty input"


def test_white_space_input():
    assert check_and_solve("\t") == "ERROR: Empty input"


def test_math_error1():
    assert check_and_solve("(-1)^2.2") == \
           "MATH ERROR: No solution, complex number"


def test_math_error2():
    assert check_and_solve("(2+2)/(2-2)") == "MATH ERROR: Zero Division"


def test_math_error3():
    assert check_and_solve("0.5!") == \
           "MATH ERROR: Factorial for fraction number"


def test_math_error4():
    assert check_and_solve("(-1)!") == \
           "MATH ERROR: Factorial for negative number"


def test_simple_ex1():
    assert check_and_solve("2+2") == 4


def test_simple_ex2():
    assert check_and_solve("3*2+1") == 7


def test_simple_ex3():
    assert check_and_solve("2^(1+2)") == 8


def test_simple_ex4():
    assert check_and_solve("3/2") == 1.5


def test_simple_ex5():
    assert check_and_solve("3%2") == 1


def test_simple_ex6():
    assert check_and_solve("3!!") == 720


def test_simple_ex7():
    assert check_and_solve("20-(1-2)") == 21


def test_simple_ex8():
    assert check_and_solve("~2+1") == -1


def test_simple_ex9():
    assert check_and_solve("3@2") == 2.5


def test_simple_ex10():
    assert check_and_solve("3@2") == 2.5


def test_simple_ex11():
    assert check_and_solve("5$2") == 5


def test_simple_ex12():
    assert check_and_solve("3&2") == 2


def test_simple_ex13():
    assert check_and_solve("(4-2)^2") == 4


def test_simple_ex14():
    assert check_and_solve("(4-1)!") == 6


def test_simple_ex15():
    assert check_and_solve("2*(4-2)^2") == 8


def test_complex_ex1():
    exercise = "18-6^2+5%4$3+2+4+5+6-------9+7&5/3.2%4.2"
    assert check_and_solve(exercise) == -7.4375


def test_complex_ex2():
    assert check_and_solve("(0!+-1*2/3^4%5&6$7@~8)^((3+1)/2)") == 1


def test_complex_ex3():
    assert check_and_solve("((1+2)^((-1+~2)*-1)!+(3-1)!)/2") == 365.5


def test_complex_ex4():
    assert check_and_solve("24%12^2-7*9&(2+3-4+6$22--8--~9+8!)") == -63


def test_complex_ex5():
    exercise = "(2!!*(8/2)@(4/2))---3^(24%12^2-7)"
    assert check_and_solve(exercise) == 5.999542752629172


def test_complex_ex6():
    exercise = "7&8*22^3!-7^3+((22%2 * 7)+3$5^3&~7)"
    assert check_and_solve(exercise) == 793658985.0000128


def test_complex_ex7():
    exercise = "14$5%2&4+4+4-7.7+(5*3$2)!"
    assert check_and_solve(exercise) == 1307674368000.3


def test_complex_ex8():
    exercise = "~((88/23*2.2)^3&(5!+---6^3))"
    assert check_and_solve(exercise) == -1.5239066784713154e-89


def test_complex_ex9():
    exercise = "((2!+3!)& (  4! + 7))^(~-(6*2/7))"
    assert check_and_solve(exercise) == 35.330864437561985


def test_complex_ex10():
    exercise = "~-~(6^2)@(3$5^3&~7)/(2.2/1.2^3)"
    assert check_and_solve(exercise) == -14.138176791272725


def test_complex_ex11():
    assert check_and_solve("3%-~(5/((-2)^(4!-(1+3)!+(10/2))))") == -0.125


def test_complex_ex12():
    exercise = "1$5/-~(3@(2))@40+55^50$93"
    assert check_and_solve(exercise) == 7.140524653815484e+161


def test_complex_ex13():
    exercise = "(~1%(9!+6))+91$00781&4^92"
    assert check_and_solve(exercise) == 2.4519928653854222e+55


def test_complex_ex14():
    assert check_and_solve("1&~~((5!!)$6)*6/09-(6!^2)") == -518399.3333333333


def test_complex_ex15():
    exercise = "53*(25!)--3/8$31$4&9!-7-9"
    assert check_and_solve(exercise) == 8.220941322965422e+26


def test_complex_ex16():
    assert check_and_solve("9-3^(39)@4+~5+(31%48)/7/6") == -18117863207.973747


def test_complex_ex17():
    assert check_and_solve("(93)-~(6)^4%39/-(7)@6*~13") == -2499.0


def test_complex_ex18():
    exercise = "09%6/2*45+209$6^(~(4)%5!)"
    assert check_and_solve(exercise) == 1.3707845121057112e+269


def test_complex_ex19():
    assert check_and_solve("(97$1/(75))-5^95%~07*~~14") == 1.1813333333333331


def test_complex_ex20():
    exercise = "~8%(98)!&7/32^-(8-(30))*2"
    assert check_and_solve(exercise) == 9.244463733058732e-33


def test_complex_ex21():
    assert check_and_solve("~-194@-7!-(9)@(6!&3%5+0!)") == -2429.5


def test_complex_ex22():
    assert check_and_solve("95^-(-4/4*09)@8+~(8+6!*1)") == -718.253205655191


def test_complex_ex23():
    assert check_and_solve("9*2/~~12@1-0*7&287@(-0)+4") == 6.769230769230769


def test_complex_ex24():
    exercise = "9^(4-5)^68*6-(~(~-54)*~0)"
    assert check_and_solve(exercise) == 7.756407337183831e-65


def test_complex_ex25():
    assert check_and_solve("8*8&~-9@6^~2^33&-(7-78)^6") == 0.0


def test_complex_ex26():
    assert check_and_solve("1-(8)%(-(~1))!-((9)+4%~9)") == -3.0


def test_complex_ex27():
    assert check_and_solve("1&97%9@~(~2)&5&~1$3$~-~-7") == 1.0
