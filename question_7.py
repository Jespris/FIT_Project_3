import matplotlib.pyplot as plt
import numpy as np
from research_data_utils import load_json_data

def year_month_to_numeric(year_month):
    year, month = year_month.split('M')
    return int(year) + (int(month) - 1) / 12 # this gives the code the numeric values that are used in the backend. For example 3/12 comes after 2/12
# -1 to help convert months into years


def question_7(): # main function for question 7
    # question 7
    data_question_7 = load_json_data('question_7_data.json')
    average_prices_by_year = extract_and_process_data_question_7(data_question_7)
    plot_data_question_7(average_prices_by_year)
    # print(dir(year_month))
  #  feb_2020_prices = prices_by_year.get('202102')
   # print(feb_2020_prices)


# Extract and process the energy price data
def extract_and_process_data_question_7(data):

    #years = []
    #prices = []

    prices_by_year = {}
    # prices_by_year is a dictionary not an array
    # Iterate over the data
    for item in data['data']:
        # [0][:4] extract a substring from a string located at a specific index in a list
        # extracts the first four characters of the string.
     #   year_month = item['key'][0][:4]  # Extract the year from the 'key' which is in the format 'YYYYMM'
        #  year_month = item['key'][0][:4] takes out 202002 from "2020M02"

        year_month = item['key'][0]
        price = float(item['values'][0])  # Convert price to float
        # float(item['values'][0])  accesses the first value element in key 'values'



        print("year month " + year_month + " price: " + str(price))



        # checks if yearMonth is in prices_by_year.
        # The if-else structure checks if the extracted yearMonth already exists as a key in the prices_by_year dictionary.
       # if year_month in prices_by_year:  # checks if yearMonth key exists in the prices_by_year dictionary
        #    prices_by_year[year_month].append(price)
            # if the year is in prices_by_year dictionary this appends price to year
       # else:
        #    prices_by_year[year_month] = [price]

        if year_month in prices_by_year:
            prices_by_year[year_month].append(price)
        else:
            prices_by_year[year_month] = [price]

    # Calculate the average price for each year
    # prices_by_year.items() is a tuple
   # average_prices_by_year = {year: sum(prices) / len(prices) for year, prices in prices_by_year.items()}

    average_prices_by_year = {year: sum(prices) / len(prices) for year, prices in prices_by_year.items()}
    print("Data Loaded:", data)  # Debug: Print the whole data structure
    return average_prices_by_year




# Plot the results
def plot_data_question_7(average_prices_by_year):
  #  sorted_years = sorted(average_prices_by_year.keys())
    #years = list(average_prices_by_year.keys())
   # prices = list(average_prices_by_year.values())
   # years_numeric = np.array(list(map(int, years)))  # Convert years to numeric for polyfit
   # prices_numeric = np.array(prices)

# sorts the years and months in chronological order
    sorted_years = sorted(average_prices_by_year.keys(), key=lambda x: year_month_to_numeric(x)) #Sorted years sets 2020M01 2020M02 etc
    prices = [average_prices_by_year[ym] for ym in sorted_years] # this tells the code what order the years are in
    years_numeric = np.array([year_month_to_numeric(ym) for ym in sorted_years]) # converts years into numeric values
  # Years numeric is the x axis

   # coefficients = np.polyfit(years_numeric, prices_numeric, 2)  # Quadratic fit
    #polynomial = np.poly1d(coefficients)
  #  coefficients = np.polyfit(years_numeric, prices, 2)
  #  polynomial = np.poly1d(coefficients)

   # plt.figure(figsize=(12, 6))
   # plt.plot(years, prices, marker='o', label='Average Price')
    #plt.plot(years, polynomial(years_numeric), color='red', label='Trend Line')
    #plt.plot(years, prices, marker='o')


    coefficients = np.polyfit(years_numeric, prices, 2)
    polynomial = np.poly1d(coefficients)

    plt.figure(figsize=(12, 6))
    plt.plot(years_numeric, prices, marker='o', label='Average Price')
    plt.plot(years_numeric, polynomial(years_numeric), color='red', label='Trend Line')


    for i, txt in enumerate(prices):
        plt.annotate(f'{txt:.2f}', (years_numeric[i], prices[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.title('Average Monthly Energy Prices for Home Heating')
    plt.xlabel('Year and Month')
    plt.ylabel('Average Price (euro/MWh)')

    # Adjust x-ticks to show year-month labels
    plt.xticks(years_numeric, sorted_years, rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

