import numpy as np
import requests
from matplotlib import pyplot as plt


def question_1():
    print("Fråga 1: Hur har nettoförmögenheten per hushåll ökat jämfört med inflation?")
    print("Länk till data: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__vtutk/statfin_vtutk_pxt_136m.px")

    household_income_data, inflation_data = retrieve_data()
    # print(household_income_data)
    year_net_assets = parse_household_data(household_income_data)
    # print(f"Nettoinkomst över år: {year_net_assets}")
    analyse_data(year_net_assets)

    # print(f"Inflation data: {inflation_data}")
    inflation_rate = parse_inflation_data(inflation_data)
    # print(f"Inflation över år: {inflation_rate}")
    show_inflation_rate(inflation_rate)

    compare_inflation_to_household_income(year_net_assets, inflation_rate)


def compare_inflation_to_household_income(year_net_assets, inflation_rate):
    # 1. Räkna ut netto_income 1985 mha inflation rate
    # 2. Multiplicera med inflation rate denna kostnad för varje år och visa på samma graf
    income_1985 = year_net_assets['1987'] / (inflation_rate['1987'] / 100)
    print(f"Inkomst 1985: {income_1985}")
    predicted_net_assets_from_inflation = {}
    for year, inflation in enumerate(inflation_rate.values()):
        predicted_net_assets_from_inflation[year] = int(income_1985 * (inflation / 100))

    # Create numpy arrays for inflation
    predicted_years = np.array(list(map(int, inflation_rate.keys())))
    predicted_net_assets = np.array(list(predicted_net_assets_from_inflation.values()))

    # Create numpy arrays for actual
    actual_years = np.array(list(map(int, year_net_assets.keys())))
    actual_net_assets = np.array(list(year_net_assets.values()))

    # plot data
    plt.figure(figsize=(10, 6))
    plt.plot(predicted_years, predicted_net_assets, marker='o', linestyle='-', label='Baserad på inflation')
    plt.plot(actual_years, actual_net_assets, marker='o', linestyle='-', label='Faktiska netto-inkomsten')
    plt.title('Nettinkomst för samtliga hushåll jämfört med inflation 1987-2019')
    plt.xlabel('År')
    plt.ylabel('Hushållets netto-inkomst (€)')
    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Visa plotten
    plt.show()


def show_inflation_rate(inflation_rate):
    # Create numpy arrays
    years = np.array(list(map(int, inflation_rate.keys())))
    inflation = np.array(list(inflation_rate.values()))

    # Plotta data
    plt.figure(figsize=(10, 6))
    plt.plot(years, inflation, marker='o', linestyle='-')
    plt.title('Inflationen jämfört med 1985 från 1985-2023')
    plt.xlabel('År')
    plt.ylabel('Procent-värde jämfört med 1985')
    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.tight_layout()

    # Visa plotten
    plt.show()


def parse_inflation_data(inflation_data):
    # Extrahera årtalen och inflationsvärdena
    years = inflation_data['dimension']['Vuosi']['category']['label']
    inflation_values = inflation_data['value']

    # Skapa en dictionary för att lagra årtalen och inflationsvärdena
    year_inflation = {year: inflation_values[i] for i, year in enumerate(years.values()) if
                      inflation_values[i] is not None}

    return year_inflation


def analyse_data(year_net_assets):
    # Create numpy arrays
    years = np.array(list(map(int, year_net_assets.keys())))
    net_assets = np.array(list(year_net_assets.values()))

    # Plotta data
    plt.figure(figsize=(10, 6))
    plt.plot(years, net_assets, marker='o', linestyle='-')
    plt.title('Nettoförmögenhet för samtliga hushåll 1987-2019')
    plt.xlabel('År')
    plt.ylabel('Nettoförmögenhet €')
    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.tight_layout()

    # Visa plotten
    plt.show()


def parse_household_data(data):
    # Using chatGPT to navigate the json data
    years = data['dimension']['Vuosi']['category']['label']
    net_assets = data['value']

    # Skapa en dictionary för att lagra årtalen och nettoförmögenhetstalen
    year_net_assets = {year: net_assets[i] for i, year in enumerate(years.values())}

    return year_net_assets


def retrieve_data():
    print("Requesting data...")
    household_url = "https://pxdata.stat.fi:443/PxWeb/api/v1/sv/StatFin/vtutk/statfin_vtutk_pxt_136m.px"
    house_json_data = {
        "query": [
            {
                "code": "Tunnusluku",
                "selection": {
                    "filter": "item",
                    "values": [
                        "Mediaani"
                    ]
                }
            },
            {
                "code": "Kotitalouden elinvaihe",
                "selection": {
                    "filter": "item",
                    "values": [
                        "SS"
                    ]
                }
            },
            {
                "code": "Tiedot",
                "selection": {
                    "filter": "item",
                    "values": [
                        "nettoae_DN3001"
                    ]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    # Send POST request with the json data
    house_response = requests.post(household_url, json=house_json_data)

    if house_response.status_code == 200:
        print("Data request successful!")
    else:
        print("Failed to get data :/")

    print("Requesting inflation data...")
    inflation_url = "https://pxdata.stat.fi:443/PxWeb/api/v1/sv/StatFin/khi/statfin_khi_pxt_11xt.px"
    inflation_json_data = {
        "query": [
            {
                "code": "Indeksisarja",
                "selection": {
                    "filter": "item",
                    "values": [
                        "0_1985"
                    ]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    inflation_response = requests.post(inflation_url, json=inflation_json_data)

    if inflation_response.status_code == 200:
        print("Data request successful!")
    else:
        print("Failed to get data :/")

    return house_response.json(), inflation_response.json()


