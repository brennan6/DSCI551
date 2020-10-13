import json
import sys

country_path = sys.argv[1]
city_path = sys.argv[2]
countryLang_path = sys.argv[3]

with open(country_path) as f:
    country_data = json.load(f)

with open(city_path) as f:
    city_data = json.load(f)

with open(countryLang_path) as f:
    countryLang_data = json.load(f)


def findCountriesCapitals():
    """Find names of countries and their capital cities for all countries in “North America”"""
    data = {}
    for country in country_data:
        if country['Continent'] == 'North America':
            capital_id = country['Capital']
            for city in city_data:
                if city['ID'] == capital_id:
                    data[country['Name']] = city['Name']
    data = dict(sorted(data.items()))

    for k,v in data.items():
        str1 = k
        str1 += ', '
        str1 += v
        print(str1)
    return None

findCountriesCapitals()