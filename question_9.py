import matplotlib.pyplot as plt
import numpy as np

from research_data_utils import load_json_data


#9: Hur har energiförbrukning inom industri i finland ändrats från 2010 till 2023? Länk: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__ehk/statfin_ehk_pxt_12vk.px/



def question_9():
    # question 9
    data_question_9 = load_json_data('question_9_data.json')
    average_prices_by_year = extract_and_process_data_question_9(data_question_9)
    plot_data_question_9(average_prices_by_year)


# Extract and process the energy price data
def extract_and_process_data_question_9(data):
    values_by_year = {}
    # values_by_year is a dictionary not an array
    # Iterate over the data
    for item in data['data']:
        # [0][:4] extract a substring from a string located at a specific index in a list
        # extracts the first four characters of the string.
        year = item['key'][0]  # Extract the year from the 'key' which is in the format 'YYYYMM'
        value = float(item['values'][0])  # Convert value to float

        # checks if yearMonth is in values_by_year.
        # The if-else structure checks if the extracted yearMonth already exists as a key in the values_by_year dictionary.
        if year in values_by_year:
            values_by_year[year].append(value)
        else:
            values_by_year[year] = [value]

    # Calculate the average price for each year
    # values_by_year.items() is a tuple
    average_values_by_year = {year: sum(values) / len(values) for year, values in values_by_year.items()}
    print("Data Loaded:", data)  # Debug: Print the whole data structure
    return average_values_by_year


# Plot the results
def plot_data_question_9(average_values_by_year):
    years = list(average_values_by_year.keys())
    values = list(average_values_by_year.values())
    years_numeric = np.array(list(map(int, years)))  # Convert years to numeric for polyfit
    prices_numeric = np.array(values)

    coefficients = np.polyfit(years_numeric, prices_numeric, 2)  # Quadratic fit
    polynomial = np.poly1d(coefficients)

    plt.figure(figsize=(10, 5))
    plt.plot(years, values, marker='o', label='Average values')
    plt.plot(years, polynomial(years_numeric), color='red', label='Trend Line')
    plt.plot(years, values, marker='o')
    plt.title('Average Annual Energy Consumption by Sector')
    plt.xlabel('Year')
    plt.ylabel('Average Consumption (GWh)')
    plt.grid(True)
    plt.show()

