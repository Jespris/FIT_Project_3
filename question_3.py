import json
import csv
import requests
import matplotlib.pyplot as plt
import numpy as np


def question_3():
    print("Fråga 3: Hur snabbt har Finlands CO2-utsläpp minskat?")
    print("Länk till data: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__khki/statfin_khki_pxt_122d.px/chart/chartViewLine/")

    emission_data = get_stats()
    print(f"Data: {emission_data}")
    emission_over_year = parse_data(emission_data)  # dictionary of emissions over year
    show_data(emission_over_year)
    analyse_data(emission_over_year)


def analyse_data(emission_over_year):
    pass


def show_data(emission_over_year: {str: int}):
    years = emission_over_year.keys()
    emissions = emission_over_year.values()

    # plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(years, emissions, marker='o', linestyle='-')
    plt.title('Växthusgasutsläpp i Finland, 1990-2022')
    plt.xlabel('År')
    plt.ylabel('Utsläpp (tusen ton CO2-ekv.)')
    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.tight_layout()

    plt.show()


def parse_data(data) -> {str: int}:
    # Använde ChatGPT för att snabbt hitta rätta keys
    years = data['dimension']['Vuosi']['category']['label']
    values = data['value']

    """    
    # testing
    for year, value in zip(years.values(), values):
        print(f"År: {year}, Utsläpp: {value}")
    """
    # create a dict of year: emission and return it
    return {year: value for year, value in zip(years.values(), values)}


def get_stats():
    print("Requesting data...")
    stats_url = "https://pxdata.stat.fi:443/PxWeb/api/v1/sv/StatFin/khki/statfin_khki_pxt_138v.px"
    json_data = {
        "query": [
            {
                "code": "Päästöluokka",
                "selection": {
                    "filter": "item",
                    "values": [
                        "0A"
                    ]
                }
            },
            {
                "code": "Kasvihuonekaasu",
                "selection": {
                    "filter": "item",
                    "values": [
                        "SS"
                    ]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    # Send POST request with the json data
    response = requests.post(stats_url, json=json_data)

    if response.status_code == 200:
        print("Data request successful!")
        return response.json()
    else:
        print("Failed to get data :/")
