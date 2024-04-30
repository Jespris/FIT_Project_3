from question_1 import question_1
from question_3 import question_3
from question_7 import question_7


def main():
    questions = {
        1: question_1,
        3: question_3,
        7: question_7
    }

    # Which question do you want analysed?
    questions[7]()




if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
