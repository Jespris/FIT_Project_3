import question_1
import question_3

from question_7 import load_data_question_7, extractAndProcessData_question_7, plot_data_question_7
def main():
    questions = {
        1: question_1.question_1,
        3: question_3.question_3
    }

    # Which question do you want analysed?
    questions[1]()

    # question 7
    data_question_7 = load_data_question_7('question_7_data.json')
    average_prices_by_year = extractAndProcessData_question_7(data_question_7)
    plot_data_question_7(average_prices_by_year)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
