import matplotlib.pyplot as plt
import numpy as np
from research_data_utils import load_json_data


def question_4():
    print("Fråga 4: Har inkomst något samband med användningen av rösträtten i politiska val såsom Presidentvalet 2024?")
    print("Länk till data: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__pvaa/statfin_pvaa_pxt_14nn.px")

    voting_data = get_stats()
    # print(f"Data: {voting_data}")
    votes_by_income = parse_data(voting_data)  # dictionary of votes per income quantile
    analyse_data(votes_by_income)


def analyse_data(votes_by_income):
    # Extrahera inkomstkvintilerna och andelarna för varje omgång
    income_quantiles = list(votes_by_income.keys())
    ratio_round_one = [value[0] for value in votes_by_income.values()]
    ratio_round_two = [value[1] for value in votes_by_income.values()]

    # Plotta diagrammet
    bar_width = 0.35
    index = np.arange(len(income_quantiles))

    fig, ax = plt.subplots()
    bars1 = ax.bar(index, ratio_round_one, bar_width, label='Omgång 1')
    bars2 = ax.bar(index + bar_width, ratio_round_two, bar_width, label='Omgång 2')

    ax.set_xlabel('Inkomstkvintil')
    ax.set_ylabel('Andel använda rösträtter (%)')
    ax.set_title('Andel använda rösträtter per inkomstkvintil och omgång i presidentvalet 2024')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(income_quantiles)
    ax.legend()

    # Lägg till text på varje stapel med exakta värden, ChatGPT har använts för att generera denna kod
    for i in range(len(income_quantiles)):
        ax.text(bars1[i].get_x() + bars1[i].get_width() / 2, bars1[i].get_height(), f'{ratio_round_one[i]:.1f}%',
                ha='center', va='bottom')
        ax.text(bars2[i].get_x() + bars2[i].get_width() / 2, bars2[i].get_height(), f'{ratio_round_two[i]:.1f}%',
                ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def parse_data(data) -> {str: int}:
    # Använde ChatGPT för att snabbt hitta rätta keys i json filen
    # Extrahera data för inkomstkvintiler och använda rösträtter
    vote_ratio_per_income = {}
    # dictionary with structure {income_quantile: (ratio_of_voters_first_round, ratio_of_voters_second_round)}

    for item in data['data']:
        income_quantile = int(item['key'][3])
        # print("Inkomst kvintil:", income_quantile)
        eligible_voters = int(item['values'][0])
        # print("Röstberättiga:", eligible_voters)
        actual_voters = int(item['values'][1])
        # print("Använda rösträtter:", income_quantile)
        ratio = actual_voters / eligible_voters * 100  # Multiply by 100 to get percentages
        if income_quantile in vote_ratio_per_income.keys():
            first_round = vote_ratio_per_income[income_quantile]
            vote_ratio_per_income[income_quantile] = (first_round, ratio)  # andra omgången
        else:
            vote_ratio_per_income[income_quantile] = ratio

    print(f"Extracted data: {vote_ratio_per_income}")
    return vote_ratio_per_income


def get_stats():
    try:
        return load_json_data("question_4_data.json")
    except Exception as e:
        print(f"ERROR: could not find data: {e}")
