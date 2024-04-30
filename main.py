from question_1 import question_1
from question_3 import question_3
from question_7 import question_7


def main():
    analyse_everything = True

    # The dictionary below have values that are functions without ()
    # These then get called later on, or if analyse_everything is set to false,
    # then choose the specific question to analyse
    # TODO: add all the questions starting function to this dictionary
    questions = {
        1: question_1,
        3: question_3,
        7: question_7
    }

    if not analyse_everything:
        # Which specific question do you want analysed?
        questions[7]()
    else:
        print("Analysing everything!")
        for value in questions.values():
            value()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
