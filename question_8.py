import matplotlib.pyplot as plt
import numpy as np
from research_data_utils import load_json_data
from matplotlib.ticker import FuncFormatter


def parse_rent_data(data):
    total_rent_per_quarter = {}
    total_houses_per_quarter = {}
    for value in data['data']:
        # print(f"{value=}")
        if value['key'][0] in total_houses_per_quarter.keys():
            total_houses_per_quarter[value['key'][0]] += int(value['values'][1])
            total_rent_per_quarter[value['key'][0]] += int(value['values'][0]) * int(value['values'][1])
        else:
            total_houses_per_quarter[value['key'][0]] = int(value['values'][1])
            total_rent_per_quarter[value['key'][0]] = int(value['values'][0]) * int(value['values'][1])

    median_rent_per_quarter = {}
    for key in total_houses_per_quarter.keys():
        median_rent_per_quarter[key] = total_rent_per_quarter[key] / total_houses_per_quarter[key]

    # print(f"{median_rent_per_quarter=}")
    return median_rent_per_quarter


def show_data(rent_income_dic):
    quarters = np.array(list(rent_income_dic.keys()))
    rent_over_income = np.array(list(rent_income_dic.values()))

    # plot data
    plt.figure(figsize=(10, 6))
    plt.plot(quarters, rent_over_income, marker='o', linestyle='-')
    plt.title('Medianhyrans andel av medianlönen i Åbo per kvartal 2018-2022')
    plt.xlabel('Kvartal')
    plt.ylabel('Hyrans andel av lönen')

    # Set the y-axis tick formatter, code copied from ChatGPT
    plt.gca().yaxis.set_major_formatter(FuncFormatter(percentage_formatter))

    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.tight_layout()

    plt.show()


# Function to format y-axis as percentage
def percentage_formatter(x, pos):
    return '{:.0f}%'.format(x * 100)


def parse_income_data(income_data):
    median_income_per_year = {int(datapoint['key'][0]): int(datapoint['values'][0]) for datapoint in income_data['data']}
    # print(f"{median_income_per_year=}")
    return median_income_per_year


def compare_income_to_rent(median_monthly_rent_per_quarter, median_income_per_year):
    rent_share_of_income = {}
    for key in median_monthly_rent_per_quarter.keys():
        year = int(key[:4])
        # print(f"{year=}")
        if year in median_income_per_year.keys():
            rent_share_of_income[key] = median_monthly_rent_per_quarter[key] / (median_income_per_year[year] / 12)

    return rent_share_of_income


def question_8():
    print("Fråga 8: Hur ökar den genomsnittliga hyreskostnaden i jämförelse med median-inkomsten i Åbo?")
    print("Länk: https://pxdata.stat.fi:443/PxWeb/api/v1/sv/StatFin/asvu/statfin_asvu_pxt_11x4.px")

    rent_cost_data = load_json_data("question_8_rent_data.json")
    income_data = load_json_data("question_8_income_data.json")

    median_rent_per_quarter = parse_rent_data(rent_cost_data)
    median_income_per_year = parse_income_data(income_data)
    rent_share_of_income = compare_income_to_rent(median_rent_per_quarter, median_income_per_year)
    show_data(rent_share_of_income)



