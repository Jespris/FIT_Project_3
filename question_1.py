import requests


def question_1():
    print("Fråga 1: Hur har nettoförmögenheten per hushåll ökat jämfört med inflation?")
    print("Länk till data: https://pxdata.stat.fi/PxWeb/pxweb/sv/StatFin/StatFin__vtutk/statfin_vtutk_pxt_136m.px")

    household_income_data = retrieve_data()
    print(household_income_data)


def retrieve_data():
    print("Requesting data...")
    url = "https://pxdata.stat.fi:443/PxWeb/api/v1/sv/StatFin/vtutk/statfin_vtutk_pxt_136m.px"
    json_data = {
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
    response = requests.post(url, json=json_data)

    if response.status_code == 200:
        print("Data request successful!")
        return response.json()
    else:
        print("Failed to get data :/")
