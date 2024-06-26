import matplotlib.pyplot as plt
import numpy as np
from research_data_utils import load_json_data


def year_month_to_numeric(year_month):
    year, month = year_month.split('M')
    return int(year) + (int(month) - 1) / 12  # this gives the code the numeric values that are used in the backend.
    # For example 3/12 comes after 2/12
    # -1 to help convert months into years


def question_7():  # main function for question 7
    # question 7
    print("Fråga 7: Hur mycket har priset för att värma hem ändrats de senaste 3 åren? Varför har priset ändrats?")
    print("Länk:  https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__ehi/statfin_ehi_pxt_13nl.px/")
    data_question_7 = load_json_data('question_7_data.json')
    prices_by_year_question_7 = extract_and_process_data_question_7(data_question_7)
    plot_data_question_7(prices_by_year_question_7)


# Extract and process the energy price data
def extract_and_process_data_question_7(data):

    prices_by_year = {}
    # prices_by_year is a dictionary not an array
    # Iterate over the data
    for item in data['data']:

        year_month = item['key'][0]
        price = float(item['values'][0])  # Convert price to float
        # float(item['values'][0])  accesses the first value element in key 'values'

        print("year month " + year_month + " price: " + str(price))

        if year_month in prices_by_year:
            prices_by_year[year_month].append(price)  # if the year is in the dictionary this appends price to year
        else:  # the year is not in the dictionary -> add new entry as list of prices
            prices_by_year[year_month] = [price]

    prices_by_year_question_7 = {year: sum(prices) / len(prices) for year, prices in prices_by_year.items()}
    print("Data Loaded:", data)  # Debug: Print the whole data structure
    return prices_by_year_question_7


# Plot the results
def plot_data_question_7(prices_by_year_question_7):
    # sorts the years and months in chronological order
    sorted_years = sorted(prices_by_year_question_7.keys(), key=lambda x: year_month_to_numeric(x))
    # Sorted years sets 2020M01 2020M02 etc
    prices = [prices_by_year_question_7[ym] for ym in sorted_years]  # this tells the code what order the years are in
    years_numeric = np.array([year_month_to_numeric(ym) for ym in sorted_years])  # converts years into numeric values
    # Years numeric is the x-axis

    coefficients = np.polyfit(years_numeric, prices, 2)
    polynomial = np.poly1d(coefficients)

    plt.figure(figsize=(16, 8))
    plt.plot(years_numeric, prices, marker='o', label='Average Price')
    plt.plot(years_numeric, polynomial(years_numeric), color='red', label='Trend Line')

    for i, txt in enumerate(prices):
        plt.annotate(
            f'{txt:.2f}',
            (years_numeric[i], prices[i]),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center',
            va='center',
            fontsize=7
        )

    plt.title('Fråga 7: Genomsnittliga månatliga energipriser för uppvärmning av bostäder')
    plt.xlabel('År och månad')
    plt.ylabel('Genomsnittligt pris (euro/MWh)')

    # Adjust x-ticks to show year-month labels
    plt.xticks(years_numeric, sorted_years, rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

