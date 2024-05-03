import matplotlib.pyplot as plt
import numpy as np

from research_data_utils import load_json_data
from matplotlib.ticker import MaxNLocator

def extract_and_process_data_question_10(data):
    values_by_year = {}
    for entry in data['data']:
        year = entry['key'][0]
        value = float(entry['values'][0])
        values_by_year[year] = value
        print("Data Loaded:", data)  # Debug: Print the whole data structure
    return values_by_year

def plot_data_question_10(values_by_year):
    years = sorted(values_by_year.keys())
    values = [values_by_year[year] for year in years]

    years_numeric = np.array(list(map(int, years)))  # Convert years to numeric for polyfit
    prices_numeric = np.array(values)

    coefficients = np.polyfit(years_numeric, prices_numeric, 2)  # Quadratic fit
    polynomial = np.poly1d(coefficients)

    plt.figure(figsize=(15, 5))  # Increase width
    plt.plot(years, values, marker='o', label='Average values')
    plt.plot(years, polynomial(years_numeric), color='red', label='Trend Line')
    plt.plot(years, values, marker='o', linestyle='-')
    plt.title('Population Changes Over Years')
    plt.xlabel('Year')
    plt.ylabel('Total Change')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=len(years)//3))  # Reduce the number of X-axis labels
    plt.xticks(rotation=45)  # Rotate labels for better visibility
    plt.show()

def question_10():
    data_question_10 = load_json_data('question_10_data.json')
    values_by_year = extract_and_process_data_question_10(data_question_10)
    plot_data_question_10(values_by_year)
