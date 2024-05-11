#question_10.py

import matplotlib.pyplot as plt
import numpy as np

from research_data_utils import load_json_data
from matplotlib.ticker import MaxNLocator


def extract_and_process_data_question_10(data):

   # values_by_year = {}
   # for entry in data['data']:
   #     year = entry['key'][0]
   #     value = float(entry['values'][0])
   #     values_by_year[year] = value
   #     print("Data Loaded:", data)  # Debug: Print the whole data structure
   # return values_by_year


    values_by_year = {}


    values = data['dataset']['value']

    print("values")
    print(values)

    # here extracts vuosi from the dataset
    years = data['dataset']['dimension']['Vuosi']['category']['index']# this line of code navigates trough a nested datastructure in question_10_data.json

    print("data")
    print(data)

    for year, index in years.items():
        values_by_year[year] = values[index]


    print("Data Loaded:", values_by_year)

    return values_by_year


def plot_data_question_10(values_by_year):
    years = sorted(values_by_year.keys())
    values = [values_by_year[year] for year in years]

    years_numeric = np.array(list(map(int, years)))  # Convert years to numeric for polyfit
    prices_numeric = np.array(values)

    coefficients = np.polyfit(years_numeric, prices_numeric, 2)  # Quadratic fit
    polynomial = np.poly1d(coefficients)

    plt.figure(figsize=(18, 12))  # Increase width

    # this code add value in the graph to each data point
    # enumerate expands the values list into indexes and values
    for i, txt in enumerate(values):
        plt.annotate(f'{txt:.2f}', (years[i], values[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.plot(years, values, marker='o', label='Antal personer')
    plt.plot(years, polynomial(years_numeric), color='red', label='Trend Linje')
    plt.plot(years, values,color='blue',marker='o', linestyle='-')
    #plt.title('Population Changes Over Years in Finland')
    plt.title('Hur har befolkningsförändringen utvecklats i finland från 1990 till 2022')
    plt.xlabel('År')
    plt.ylabel('Totala befolknings förändringen (personer)')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=len(years)//3))  # Reduce the number of X-axis labels
    plt.xticks(rotation=45)  # Rotate labels for better visibility
    plt.legend()  # this shows the labels for each line
    plt.show()


def question_10():
    data_question_10 = load_json_data('question_10_data.json')
    values_by_year = extract_and_process_data_question_10(data_question_10)
    plot_data_question_10(values_by_year)
