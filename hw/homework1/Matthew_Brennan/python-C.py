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

def findContinentLifeExpectancy():
    """Find, for each continent, the average life expectancy of all countries in the continent which has at least 5 countries whose GNP is more than 10000."""
    data_count = {}
    total = {}
    for country in country_data:
        if country['GNP'] > 10000:
            if country['Continent'] in data_count.keys():
                data_count[country['Continent']] = data_count[country['Continent']] + 1
            else:
                data_count[country['Continent']] = 1
    data_count = {k:v for k,v in data_count.items() if v >= 5}
    data_le = {}
    total = {}
    for country in country_data:
        if country['Continent'] in data_count.keys():
            if country['Continent'] in data_le.keys():
                data_le[country['Continent']] = data_le[country['Continent']] + country['LifeExpectancy']
                total[country['Continent']] = total[country['Continent']] + 1
            else:
                data_le[country['Continent']] = country['LifeExpectancy']
                total[country['Continent']] = 1
            
    data = {k:(v/total[k]) for k,v in data_le.items()}
    data = dict(sorted(data.items()))

    for k,v in data.items():
        str1 = k
        str1 += ", "
        str1 += str(v)
        print(str1)

    return None

findContinentLifeExpectancy()