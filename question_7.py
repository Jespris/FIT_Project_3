import json
import matplotlib.pyplot as plt


# Load the JSON data from the file
def load_data_question_7(filepath):
    # open opens files
    # r tells open to read data
    with open(filepath, 'r', encoding='utf-8') as file:
        # json.load converts json into python dictonary
        data_question_7 = json.load(file)
    return data_question_7


# Extract and process the energy price data
def extractAndProcessData_question_7(data):
    prices_by_year = {}
    #prices_by_year is an dictonary not an array
    # Iterate over the data
    for item in data['data']:
        # [0][:4] extract a substring from a string located at a specific index in a list
        # extracts the first four characters of the string.
        yearMonth = item['key'][0][:4]  # Extract the year from the 'key' which is in the format 'YYYYMM'
        price = float(item['values'][0])  # Convert price to float

        # checks if yearMonth is in prices_by_year
        # The if-else structure checks if the extracted yearMonth already exists as a key in the prices_by_year dictionary.
        if yearMonth in prices_by_year: # checks if yearMonth key exists in the prices_by_year dictionary
            prices_by_year[yearMonth].append(price) # if the year is in prices_by_year dictionary the this appends price to year
        else:
            prices_by_year[yearMonth] = [price]

    # Calculate the average price for each year
    #prices_by_year.items() is a touple
    average_prices_by_year = {year: sum(prices) / len(prices) for year, prices in prices_by_year.items()}
    return average_prices_by_year


# Plot the results
def plot_data_question_7(average_prices_by_year):
    years = list(average_prices_by_year.keys())
    prices = list(average_prices_by_year.values())

    plt.figure(figsize=(10, 5))
    plt.plot(years, prices, marker='o')
    plt.title('Average Annual Energy Prices for Home Heating Between 2020-2023')
    plt.xlabel('Year')
    plt.ylabel('Average Price (euro/MWh)')
    plt.grid(True)
    plt.show()

