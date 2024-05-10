from matplotlib import pyplot as plt
from research_data_utils import load_json_data


def question_5():
    print("Fråga 5:")
    print("Länk till data: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__merek/statfin_merek_pxt_11cb.px/")

    new_cars_data, total_cars_data = get_data()
    # getting and showing the relevant data for new cars
    new_cars = parse_new_cars(new_cars_data)
    compare_new = show_new_cars(new_cars)

    # getting and showing the relevant data for total cars
    total_cars = parse_total_cars(total_cars_data)
    compare_total = show_total_cars(total_cars)

    compare_new_cars_to_total(compare_new, compare_total)


def compare_new_cars_to_total(new_cars, total_cars):
    # getting all the data used so far in the program and comparing the total amount to the new cars
    new_cars_years = new_cars[0]
    new_cars_amount = new_cars[1]

    total_cars_years = total_cars[0]
    total_cars_amount = total_cars[1]

    plt.figure(figsize=(10, 6))
    plt.plot(new_cars_years, new_cars_amount, label = "New cars", linestyle = "-")
    plt.plot(total_cars_years, total_cars_amount, label = "Total cars", linestyle = "--")
    plt.title("Comparsion between new and total amount of cars")
    plt.xlabel("Years")
    plt.ylabel("Amount")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def parse_new_cars(new_cars_data):
    amount_per_year = []
    # Extracting the data and appending it into an array for new cars
    for point in new_cars_data['data']:
        year = int(point['key'][1])
        amount = int(point['values'][0])

        amount_per_year.append((year,amount))
    return amount_per_year


def show_new_cars(new_cars):
    # Showing the data and saving it into a tuple that is used later int the comparison
    years = []
    amount = []
    for i in new_cars:
        years.append(i[0])
        amount.append(i[1])

    plt.figure(figsize=(10, 6))
    plt.plot(years,amount, marker = 'o', linestyle = '-')
    plt.title("New cars")
    plt.xlabel("years")
    plt.ylabel("amount")
    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return years, amount


def parse_total_cars(total_cars_data):
    # Extracting the data and appending it into an array for the total cars
    amount_per_year = []
    for point in total_cars_data['data']:
        year = int(point['key'][0])
        amount = int(point['values'][0])

        amount_per_year.append((year,amount))
    return amount_per_year


def show_total_cars(total_cars):
    # Showing the data and saving it into a tuple that is used later int the comparison
    years = []
    amount = []
    for i in total_cars:
        years.append(i[0])
        amount.append(i[1])

    plt.figure(figsize=(10, 6))
    plt.plot(years, amount, linestyle='-')
    plt.title("Total cars")
    plt.xlabel("years")
    plt.ylabel("amount")
    plt.xticks(rotation=45)  # Rotera x-axelns tick-märken för bättre läsbarhet
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return years, amount


def get_data():
    return load_json_data("question_5_new_cars_data.json"), load_json_data("question_5_total_cars_data.json")
