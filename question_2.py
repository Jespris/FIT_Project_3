import numpy as np
from matplotlib import pyplot as plt

from research_data_utils import load_json_data


def question_2():
    print("Fråga 2: Vad är andelen som fortsätter studier efter studentexamen jämfört med de som inte studerar")
    print("Länk till data: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__khak/statfin_khak_pxt_13tq.px")

    data = load_json_data("question_2_data.json")
    print(data)
    stud_dict, icke_stud_dict = parse_data(data)
    analyse_data(stud_dict, icke_stud_dict)


def analyse_data(stud_dict, icke_stud_dict):
    # Sätt x-axel och y-värden i olika np arrays
    years = list(stud_dict.keys())

    stud_status = {}
    immediate = []
    first_year = []
    second_year = []
    third_year = []
    not_immediate = []
    not_first_year = []
    not_second_year = []
    not_third_year = []
    for value in stud_dict.values():
        # we now have a tuple, example (nr, nr, None, None)
        immediate.append(value[0])
        first_year.append(value[1])
        second_year.append(value[2])
        third_year.append(value[3])

    for value in icke_stud_dict.values():
        # we now have a tuple, example (nr, nr, None, None)
        not_immediate.append(value[0])
        not_first_year.append(value[1])
        not_second_year.append(value[2])
        not_third_year.append(value[3])

    immediate = tuple(map(lambda x: x if x is not None else 0, immediate))
    first_year = tuple(map(lambda x: x if x is not None else 0, first_year))
    second_year = tuple(map(lambda x: x if x is not None else 0, second_year))
    third_year = tuple(map(lambda x: x if x is not None else 0, third_year))
    not_immediate = tuple(map(lambda x: x if x is not None else 0, not_immediate))
    not_first_year = tuple(map(lambda x: x if x is not None else 0, not_first_year))
    not_second_year = tuple(map(lambda x: x if x is not None else 0, not_second_year))
    not_third_year = tuple(map(lambda x: x if x is not None else 0, not_third_year))

    stud_status['Studerar omedelbart'] = immediate
    stud_status['1 år efter'] = first_year
    stud_status['2 år efter'] = second_year
    stud_status['3 år efter'] = third_year
    stud_status['Studerar inte omedelbart'] = not_immediate
    stud_status['inte 1 år efter'] = not_first_year
    stud_status['inte 2 år efter'] = not_second_year
    stud_status['inte 3 år efter'] = not_third_year

    x_loc = np.arange(len(years))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')
    bottom = np.zeros(8)

    active_statuses = ['Studerar omedelbart', '1 år efter', '2 år efter', '3 år efter']
    comparison_status = {'Studerar omedelbart': 'Studerar inte omedelbart',
                         '1 år efter': 'inte 1 år efter',
                         '2 år efter': 'inte 2 år efter',
                         '3 år efter': 'inte 3 år efter'
                         }

    for status, amount in stud_status.items():
        if status not in active_statuses:
            offset = width * multiplier
            ax.bar(x_loc + offset, amount, width, label=status, bottom=bottom)
            # ax.bar_label(rects, padding=3)
            multiplier += 1
            # bottom += amount
            # show the comparison bar on top
            # compared_status = comparison_status[status]
            # compared_amount = stud_status[compared_status]
            # ax.bar(x_loc + offset, compared_amount, width, label=compared_status, bottom=bottom)
            # bottom -= (amount + compared_amount)
        else:
            print("TODO: show non studying on top")

    plt.xlabel('År')
    plt.ylabel('Antal')
    plt.title('Situation efter studentexamen')
    ax.set_xticks(x_loc + width, years)
    plt.legend(ncols=2)
    ax.set_ylim(0, 50000)

    plt.show()


def parse_data(data):
    # Using chatGPT to navigate the json data
    # Skapa dictionarys för att lagra antal studerande och icke-studerande
    studerande_dict = {}
    icke_studerande_dict = {}

    # Loopa igenom data och fyll i dictionarys för studerande och icke-studerande
    for point in data['data']:
        year = int(point['key'][0])  # Extrahera året
        status = int(point['key'][3])  # Extrahera studiestatus (0, 1, 2, 3) samt (00, 10, 20, 30)
        try:
            antal = int(point['values'][0])  # Extrahera antalet
        except ValueError:
            antal = None

        # Lägg till antalet i rätt dictionary och position baserat på studiestatus
        index = status
        if status >= 10:
            index = status // 10

        assert 0 <= index <= 3

        if status < 10 and point['key'][3] != '00':  # studiestatus (0, 1, 2, 3)
            if year in studerande_dict:
                og_tuple = studerande_dict[year]
            else:
                og_tuple = (None, None, None, None)  # året har inte initialiseras
            studerande_dict[year] = og_tuple[:index] + (antal,) + og_tuple[index+1:]
        else:  # studiestatus 00, 10, 20, 30
            if year in icke_studerande_dict:
                og_tuple = icke_studerande_dict[year]
            else:
                og_tuple = (None, None, None, None)
            icke_studerande_dict[year] = og_tuple[:index] + (antal,) + og_tuple[index+1:]

    print(f"Studerande dict: {studerande_dict}")
    print(f"Icke-studerande dict: {icke_studerande_dict}")

    return studerande_dict, icke_studerande_dict



