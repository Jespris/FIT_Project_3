import question_1
import question_3


def main():
    questions = {
        1: question_1.question_1,
        3: question_3.question_3
    }

    # Which question do you want analysed?
    questions[1]()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
