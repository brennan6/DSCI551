from helper import listToString
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

def findCountriesLang():
    """Find names of countries and their official languages for all countries in “North America”"""
    data = {}
    for country in country_data:
        if country['Continent'] == 'North America':
            country_code = country['Code']
            name = country['Name']
            lang_true = []
            for countryLang in countryLang_data:
                if countryLang['CountryCode'] == country_code and countryLang['IsOfficial'] == 'T':
                    lang_true.append(countryLang['Language'])
            data[name] = lang_true
    
    #Change empty to 'None':
    for k,v in data.items():
        if len(v) == 0:
            data[k] = ['None']
    data = dict(sorted(data.items()))

    for k,v in data.items():
        str1 = k
        str1 += ', '
        str1 += listToString(v)
        print(str1)
    return None

findCountriesLang()