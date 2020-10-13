import sys
import json
import requests

def findCountriesCapitals():
    """Find names of countries and their capital cities for all countries in “North America”"""
    urlCountry = 'https://hw1-dsci551-31309.firebaseio.com/world/country.json?orderBy="Continent"&equalTo="North America"&print=pretty'
    response = requests.get(urlCountry)
    perf_file = open("performance.txt","w")
    perf_file.write("firebase-A: Requests Made - 2, Size of 1st Download (Bytes) - ")
    perf_file.write(str(len(response.content)))
    country_data = response.json()

    urlCity = 'https://hw1-dsci551-31309.firebaseio.com/world/city.json?orderBy="$key"' 
    response = requests.get(urlCity)
    perf_file.write(", Size of 2nd download (Bytes) - ")
    perf_file.write(str(len(response.content)))
    perf_file.write("\n\n")
    perf_file.close()
    city_data = response.json()

    city_data = city_data[1:len(city_data)]
    city_data_fixed = {i+1:{k:v for k,v in city_data[i].items()} for i in range(len(city_data))}

    data = {}
    for key in country_data.keys():
        capital_val = country_data[key]['Capital']
        city_d = city_data_fixed.pop(capital_val)
        data[country_data[key]['Name']] = city_d['Name']
    data = dict(sorted(data.items()))

    for k,v in data.items():
        str1 = k
        str1 += ', '
        str1 += v
        print(str1)
    return None

findCountriesCapitals()