from helper import listToString
import sys
import json
import requests

def findCountriesLang():
    """Find names of countries and their official languages for all countries in “North America”"""
    urlCountry = 'https://hw1-dsci551-31309.firebaseio.com/world/country.json?orderBy="Continent"&equalTo="North America"&print=pretty' 
    response = requests.get(urlCountry)
    perf_file = open("performance.txt","a")
    perf_file.write("firebase-B: Requests Made - 2, Size of 1st Download (Bytes) - ")
    perf_file.write(str(len(response.content)))
    country_data = response.json()

    urlCountryLang = 'https://hw1-dsci551-31309.firebaseio.com/world/countryLanguage.json' 
    response = requests.get(urlCountryLang)
    perf_file.write(", Size of 2nd download (Bytes) - ")
    perf_file.write(str(len(response.content)))
    perf_file.write("\n\n")
    perf_file.close()
    countryLang_data = response.json()

    data = {}
    for code in country_data.keys():
        official = []
        lang_d = countryLang_data.pop(code)
        for lang in lang_d.keys():
            if lang_d[lang]['IsOfficial'] == 'T':
                official.append(lang)
        
        data[country_data[code]['Name']] = listToString(official)

    for k,v in data.items():
        if len(v) == 0:
            data[k] = 'None'
            
    data = dict(sorted(data.items()))

    for k,v in data.items():
        str1 = k
        str1 += ', '
        str1 += v
        print(str1)
    return None

findCountriesLang()