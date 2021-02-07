from calculator_solver import *
from exercise_generator import *


def main():
    while True:
        try:
            # Menu
            print("\nPlease select one of the following:")
            print("Type 1 - generate and solve random exercise")
            print("Type 2 - solve exercise from input")
            print("For finishing, type 3")

            try:
                # get user selection
                selection = input()
            except Exception:
                print("ERROR: invalid input")

            exercise = ''
            # for choice 1
            if selection == '1':
                print("Please enter the length of the wanted exercise")
                print("Notice, 25 is the maximum possible length")
                try:
                    length = int(input())
                    # if the input isn't in the correct range
                    if length > 25 or length < 1:
                        raise ValidationError("invalid length for exercise")
                except ValidationError as VE:
                    raise VE
                except Exception:
                    raise ValidationError("ERROR: invalid input")

                # get a random exercise from the generator
                exercise = get_exercise(length)
                print("generated exercise: " + exercise)

            # for choice 2
            if selection == '2':
                print("Insert Exercise")
                try:
                    # get the user's input
                    exercise = input()
                except Exception:
                    raise ValidationError("ERROR: invalid input")

            # for choice 3
            if selection == '3':
                print("Thanks for using my Calculator! :)")
                break
                
            # in case of an invalid selection
            if selection != '1' and selection != '2' and selection != '3':
                print("Invalid input")
                continue

            exercise = handle_input(exercise)
            validations.execute_validation(exercise)
            # Solve
            exercise = solve_exercise(exercise)
            print("Exercise Solution: "+str(exercise))

        except ZeroDivisionError:
            print("MATH ERROR: Zero Division")
        except OverflowError:
            print("Number's too big")
        except RecursionError:
            print("Exercise is too long")
        except ValidationError as VE:
            # when validation error was raised
            print(VE)
        except RunTimeError as RT:
            # when run time error was raised
            print(RT)


if __name__ == "__main__":
    main()