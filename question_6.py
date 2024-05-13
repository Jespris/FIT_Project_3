import os
import json
import requests
import numpy as np
from matplotlib import pyplot as plt
from research_data_utils import load_json_data, DATA_FOLDER


def question_6():
    print("Fråga 6: Ökar elpris till hushåll snabbare än inflation?")
    print("Länk till data: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__ehi/statfin_ehi_pxt_13rb.px/")
    # Fetching data from research data
    el_price_data, inflation_data = get_data()

    # Getting the electricity price of c/kWh of households over 15 000kWh per month
    el_price = parse_el_price_data(el_price_data)
    show_el_price(el_price)

    inflation_rate = parse_inflation_data(inflation_data)
    compare_inflation_to_el_price(el_price, inflation_rate)


def compare_inflation_to_el_price(el_price, inflation_rate):

    el_price_2009 = el_price['2009M12'] / (inflation_rate['2009'] / 100)
    perdicted_el_price_from_inflation = {}

    # Predicting the inflation price
    for year, inflation in enumerate(inflation_rate.values()):
        perdicted_el_price_from_inflation[year] = int(el_price_2009 * (inflation / 100))

    predicted_years = np.array(list(map(str, inflation_rate.keys())))
    predicted_el_price = np.array(list(perdicted_el_price_from_inflation.values()))

    actual_years = np.array(list(map(str, el_price.keys())))
    # Tar bort M12 från året så att inflationen och verkliga kan synas på samma graf
    actual_years = np.char.replace(actual_years, "M12", "")
    actual_price = np.array(list(map(int, el_price.values())))

    # plot data
    plt.figure(figsize=(10, 6))
    plt.plot(predicted_years, predicted_el_price, marker='o', linestyle='-', label='Baserad på inflation')
    plt.plot(actual_years, actual_price, marker='o', linestyle='-', label='Faktiska priset')
    plt.title('El pris för samtliga hushåll med över 15 000 kWh jämfört med inflation 2009-2023')
    plt.xlabel('År')
    plt.ylabel('Pris (c/kWh)')
    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Visa plotten
    plt.show()

    return 0


def parse_el_price_data(data):

    years = data['dimension']['Kuukausi']['category']['label']

    price = data['value']

    # Extraherar priset för December av varje år från 2009 till 2023
    price_per_month = {year : price[i] for i, year in enumerate(years.values()) if price[i] is not None 
                       and "M12" in year}
        
    return price_per_month


def parse_inflation_data(inflation_data):
    # Extrahera årtalen och inflationsvärdena
    years = inflation_data['dimension']['Vuosi']['category']['label']
    inflation_values = inflation_data['value']

    # Skapa en dictionary för att lagra årtalen och inflationsvärdena
    year_inflation = {year: inflation_values[i] for i, year in enumerate(years.values()) if
                      inflation_values[i] is not None and int(year) >= 2009}

    return year_inflation


def show_el_price(el_price):
    # Extrahera tiden och priset
    months = np.array(list(map(str, el_price.keys())))
    price = np.array(list(map(int, el_price.values())))

    # Plotta data
    plt.figure(figsize=(10, 6))
    plt.plot(months, price, marker='o', linestyle='-')
    plt.title('El pris i slutet av året från 2009-2023 för hshåll med el konsumption över 15 000 kWh')
    plt.xlabel('Months')
    plt.ylabel('Price, c/kWh')
    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.tight_layout()

    # Visa plotten
    plt.show()


def get_data():
    # Hämtar datan från research data som är extraherade med retrieve_data() metoden
    return load_json_data('question_6_data.json'), load_json_data('inflation_data.json')


# Obsolete code, used when the json file in research data is somehow deleted
def retrieve_data():
    el_price_url = "https://pxdata.stat.fi:443/PxWeb/api/v1/sv/StatFin/ehi/statfin_ehi_pxt_13rb.px"
    el_price_json = {
        "query": [
            {
                "code": "Hintakomponentti",
                "selection": {
                "filter": "item",
                "values": [
                "SSS"
                ]
            }
        },
        {
            "code": "Sähkön kuluttajatyyppi",
            "selection": {
            "filter": "item",
            "values": [
            "E"
            ]
        }
        },
        {
            "code": "Tiedot",
            "selection": {
            "filter": "item",
            "values": [
            "hinta_snt_kwh"
            ]
        }
        }
    ],
        "response": {
        "format": "json-stat2"
        }
    }
    el_price_response = requests.post(el_price_url, json = el_price_json)

    if el_price_response.status_code == 200:
        print("Data request successful!")
        # save the data to the research data folder
        data_path = os.path.join(DATA_FOLDER, "question_6_data.json")
        # format the data for readability
        json_string = json.dumps(el_price_response.json(), indent=4)
        # write to the file
        with open(data_path, "w") as json_file:
            json_file.write(json_string)
        print(f"JSON file saved to {data_path}")
    else:
        print("Failed to get data :/")

