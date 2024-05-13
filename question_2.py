import numpy as np
from matplotlib import pyplot as plt

from research_data_utils import load_json_data


def question_2():
    print("Fråga 2: Vad är andelen som fortsätter studier efter studentexamen jämfört med de som inte studerar")
    print("Länk till data: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__khak/statfin_khak_pxt_13tq.px")

    # Load the data from the json file
    data = load_json_data("question_2_data.json")
    # print(data)
    # parse the json data into two different dictionaries, one for keeping track of those that resume studying,
    # and the other one for keeping track of those who choose not to continue studying
    stud_dict, icke_stud_dict = parse_data(data)
    # display this data in a complicated grouped, stacked bar graph format
    analyse_data(stud_dict, icke_stud_dict)


def analyse_data(stud_dict, icke_stud_dict):
    # Sätt x-axel och y-värden i olika np arrays
    years = list(stud_dict.keys())

    # initialisera variabler som skall fyllas med data
    stud_status = {}  # dict har formen {'status': [lista med värden]}
    immediate = []
    first_year = []
    second_year = []
    third_year = []
    not_immediate = []
    not_first_year = []
    not_second_year = []
    not_third_year = []
    for value in stud_dict.values():
        # value is a tuple, example (nr, nr, None, None)
        immediate.append(value[0])
        first_year.append(value[1])
        second_year.append(value[2])
        third_year.append(value[3])

    for value in icke_stud_dict.values():
        # value is a tuple, example (nr, nr, None, None)
        not_immediate.append(value[0])
        not_first_year.append(value[1])
        not_second_year.append(value[2])
        not_third_year.append(value[3])

    # fix_tuples function refactors the lists to tuples and replaces None values with 0 to not get errors
    immediate = fix_tuples(immediate)
    first_year = fix_tuples(first_year)
    second_year = fix_tuples(second_year)
    third_year = fix_tuples(third_year)
    not_immediate = fix_tuples(not_immediate)
    not_first_year = fix_tuples(not_first_year)
    not_second_year = fix_tuples(not_second_year)
    not_third_year = fix_tuples(not_third_year)

    # map the statuses to the tuples
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
    multiplier = 0  # multiplier used with the bar width to update the x_loc of the bars

    fig, ax = plt.subplots(layout='constrained')

    active_statuses = ['Studerar omedelbart', '1 år efter', '2 år efter', '3 år efter']
    # Keep track of the relation between active and non-active study statuses
    comparison_status = {'Studerar omedelbart': 'Studerar inte omedelbart',
                         '1 år efter': 'inte 1 år efter',
                         '2 år efter': 'inte 2 år efter',
                         '3 år efter': 'inte 3 år efter'
                         }

    for active_status in active_statuses:
        offset = width * multiplier  # the x-offset in the graph
        compared_status = comparison_status[active_status]  # the inverse status
        # show the non-studying amount below in red, and studying on top in green
        # get the values for the graph bars
        non_amount = stud_status[compared_status]
        amount = stud_status[active_status]
        # display the non-studying bar
        ax.bar(x_loc + offset, non_amount, width, color='red', edgecolor='black', linewidth=1)
        # display the studying bar on top of the previous bar
        ax.bar(x_loc + offset, amount, width, bottom=non_amount, color='green', edgecolor='black', linewidth=1)

        # increment the x-location of bars offset
        multiplier += 1

    plt.xlabel('Utexamineringsår')
    plt.ylabel('Antal')
    plt.title('Studerande-situation hos studenter up till 3 år efter studentexamen')
    ax.set_xticks(x_loc + width, years)

    # Custom legend made by ChatGPT
    # Define custom legend labels and colors
    legend_labels = {'(red)': 'Studerar inte', '(green)': 'Studerar'}
    legend_colors = {'(red)': 'red', '(green)': 'green'}

    # Create custom legend handles
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors.values()]

    # Create the legend with custom labels and handles
    plt.legend(legend_handles, legend_labels.values(), loc='upper right')
    ax.set_ylim(0, 40000)  # constrain the y-axis for it to make sense

    plt.show()


def fix_tuples(my_list):
    # Helper function to replace Null values with 0 when mapping data in the analyse_data function
    return tuple(map(lambda x: x if x is not None else 0, my_list))


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
            antal = None  # we set antal to None to keep consistent list sizes, None values get handled later

        # Lägg till antalet i rätt dictionary och position baserat på studiestatus
        index = status
        if status >= 10:
            index = status // 10

        assert 0 <= index <= 3

        if status < 10 and point['key'][3] != '00':  # studiestatus (0, 1, 2, 3)
            if year in studerande_dict:
                og_tuple = studerande_dict[year]  # året har initialiseras, get the tuple
            else:
                og_tuple = (None, None, None, None)  # året har inte initialiseras, create a None tuple

            studerande_dict[year] = og_tuple[:index] + (antal,) + og_tuple[index+1:]  # update the tuple
        else:  # studiestatus 00, 10, 20, 30, same structure as above but now add to the non-studying dictionary
            if year in icke_studerande_dict:
                og_tuple = icke_studerande_dict[year]
            else:
                og_tuple = (None, None, None, None)

            icke_studerande_dict[year] = og_tuple[:index] + (antal,) + og_tuple[index+1:]

    # print(f"Studerande dict: {studerande_dict}")
    # print(f"Icke-studerande dict: {icke_studerande_dict}")

    return studerande_dict, icke_studerande_dict



