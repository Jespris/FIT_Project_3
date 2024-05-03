import matplotlib.pyplot as plt
import numpy as np
from research_data_utils import load_json_data




def question_7(): # main function for question 7
    # question 7
    data_question_7 = load_json_data('question_7_data.json')
    average_prices_by_year = extract_and_process_data_question_7(data_question_7)
    plot_data_question_7(average_prices_by_year)


# Extract and process the energy price data
def extract_and_process_data_question_7(data):
    prices_by_year = {}
    # prices_by_year is a dictionary not an array
    # Iterate over the data
    for item in data['data']:
        # [0][:4] extract a substring from a string located at a specific index in a list
        # extracts the first four characters of the string.
        year_month = item['key'][0][:4]  # Extract the year from the 'key' which is in the format 'YYYYMM'
        #  year_month = item['key'][0][:4] takes out 202002 from "2020M02"
        price = float(item['values'][0])  # Convert price to float
        # float(item['values'][0])  accesses the first value element in key 'values'

        # checks if yearMonth is in prices_by_year.
        # The if-else structure checks if the extracted yearMonth already exists as a key in the prices_by_year dictionary.
        if year_month in prices_by_year:  # checks if yearMonth key exists in the prices_by_year dictionary
            prices_by_year[year_month].append(price)
            # if the year is in prices_by_year dictionary this appends price to year
        else:
            prices_by_year[year_month] = [price]

    # Calculate the average price for each year
    # prices_by_year.items() is a tuple
    average_prices_by_year = {year: sum(prices) / len(prices) for year, prices in prices_by_year.items()}
    print("Data Loaded:", data)  # Debug: Print the whole data structure
    return average_prices_by_year


# Plot the results
def plot_data_question_7(average_prices_by_year):
    years = list(average_prices_by_year.keys())
    prices = list(average_prices_by_year.values())
    years_numeric = np.array(list(map(int, years)))  # Convert years to numeric for polyfit
    prices_numeric = np.array(prices)

    coefficients = np.polyfit(years_numeric, prices_numeric, 2)  # Quadratic fit
    polynomial = np.poly1d(coefficients)

    plt.figure(figsize=(10, 5))
    plt.plot(years, prices, marker='o', label='Average Price')
    plt.plot(years, polynomial(years_numeric), color='red', label='Trend Line')
    plt.plot(years, prices, marker='o')
    plt.title('Average Annual Energy Prices for Home Heating Between 2020-2023')
    plt.xlabel('Year')
    plt.ylabel('Average Price (euro/MWh)')
    plt.grid(True)
    plt.show()

