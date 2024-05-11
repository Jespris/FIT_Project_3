import matplotlib.pyplot as plt
import numpy as np

from research_data_utils import load_json_data


# 9: Hur har energiförbrukning inom industri i finland ändrats från 2010 till 2023?
# Länk: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__ehk/statfin_ehk_pxt_12vk.px/


def question_9():
    # question 9
    print("Accessing question_9_data.json")

    data_question_9 = load_json_data('question_9_data.json')  # calls load_json_data from research_data_utils.py
    average_prices_by_year = extract_and_process_data_question_9(data_question_9)  # process the data from question_9_data.json
    plot_data_question_9(average_prices_by_year)  # takes the values from average_prices_by_year and plots the data on a graph


# Extract and process the energy price data
def extract_and_process_data_question_9(data):

    values_by_year = {}
    # values_by_year is a dictionary not an array
    # Iterate over the data
    for item in data['data']:

        year = item['key'][0]  # Extract the year from the 'key' in the format 'YYYY'
        value = float(item['values'][0])  # Convert value to float

        print("year " + year + " " + " GWh Value "+ str(value))

        # checks if yearMonth is in values_by_year.
        # The if-else structure checks if the extracted yearMonth already exists as a key in the values_by_year dictionary.
        if year in values_by_year: # creates a new list for a year
            values_by_year[year].append(value)
        else:
            values_by_year[year] = [value]

    # Calculate the average price for each year
    # values_by_year.items() is a tuple
    # This is a new dictionary year: sum(values) / len(values)
    # average_values_by_year does not really calculate an average. it just value/year. this is done to convert the value to a form that np.polyfit can use for the trend line
    average_values_by_year = {year: sum(values) / len(values) for year, values in values_by_year.items()} #calculates average value of each year for each value in values_by_year

    # average_values_by_year makes the values in the dictionary into numerical values that can be used in  coefficients = np.polyfit(years_numeric, prices_numeric
    print("average_values_by_year:", average_values_by_year)
    print("Data Loaded:", data)  # Debug: Print the whole data structure
    return average_values_by_year


# Plot the results
def plot_data_question_9(average_values_by_year):
    # need to convert dictionaries into list due to that dictionaries are not always ordered
    years = list(average_values_by_year.keys())  # list() converts a dictionary to a list
    values = list(average_values_by_year.values())  # () converts values dictionary to a list
    years_numeric = np.array(list(map(int, years)))  # Convert years to numeric for polyfit # This is the x values in the graph
    prices_numeric = np.array(values)  # This is the y values in the graph

    # this code helps to create the red trend line
    # np.polyfit is fron numpy. It fits a polynmal
    coefficients = np.polyfit(years_numeric, prices_numeric, 2)  # Quadratic fit # polynomal 2 means this a^2+bx+c
    polynomial = np.poly1d(coefficients) # used to create the trend line

    # Calculate trend line values
    trend_values = polynomial(years_numeric)

    # Print trend line values to console
    print("Trend line values by year:")
    for year, trend_value in zip(years, trend_values):
        print(f"Year {year}: GWh Value {trend_value:.2f}")

    # plt.figure() creates a new canvas
    plt.figure(figsize=(10, 5))

    # this code add value in the graph to each data point
    # enumerate expands the values list into indexes and values
    for i, txt in enumerate(values):
        plt.annotate(f'{txt:.2f}', (years[i], values[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.plot(years, values, marker='o',color='blue', label=' GWh values')
    plt.plot(years, polynomial(years_numeric), color='red', label='Trend Line')

    plt.plot(years, values, marker='o')
    plt.title('Average Annual Energy Consumption by Industry')
    plt.xlabel('Year')  # Labesl the X axis
    plt.ylabel('Average Consumption (GWh)')
    plt.grid(True)  # adds a grid to the graph
    plt.legend()  # this shows the labls for each line
    plt.show()

