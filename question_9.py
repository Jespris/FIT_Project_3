import matplotlib.pyplot as plt
from research_data_utils import load_json_data


# 7: Hur ökar den genomsnitta hyreskostnaden per m^2 i jämförelse med inkomst
# Länk: https://pxdata.stat.fi:443/PxWeb/api/v1/sv/StatFin/asvu/statfin_asvu_pxt_11x4.px


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
    return average_values_by_year


# Plot the results
def plot_data_question_9(average_values_by_year):
    years = list(average_values_by_year.keys())
    values = list(average_values_by_year.values())

    plt.figure(figsize=(10, 5))
    plt.plot(years, values, marker='o')
    plt.title('Average Annual Energy Consumption by Sector')
    plt.xlabel('Year')
    plt.ylabel('Average Consumption (GWh)')
    plt.grid(True)
    plt.show()

