from question_1 import question_1
from question_2 import question_2
from question_3 import question_3
from question_4 import question_4
from question_5 import question_5
from question_6 import question_6
from question_7 import question_7
from question_8 import question_8
from question_9 import question_9
from question_10 import question_10


def main():
    analyse_everything = False

    # The dictionary below have values that are functions without ()
    # These then get called later on, or if analyse_everything is set to false,
    # then choose the specific question to analyse
    # TODO: add all the questions starting function to this dictionary
    questions = {
        1: question_1,
        2: question_2,
        3: question_3,
        4: question_4,
        5: question_5,
        6: question_6,
        7: question_7,
        8: question_8,
        9: question_9,
        10: question_10,
    }

    if not analyse_everything:
        # Which specific question do you want analysed?
        questions[10]()
    else:
        print("Analyzing everything!")
        for value in questions.values():
            value()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
