from helper import listToString
import sys
import json
import requests

def findCountriesLang():
    """Find names of countries and their official languages for all countries in “North America”"""
    url = 'https://hw1-dsci551-31309.firebaseio.com/world/country_nested.json?orderBy="Continent"&equalTo="North America"&print=pretty' 
    response = requests.get(url)
    perf_file = open("performance.txt","a")
    perf_file.write("firebase-B-nested: Requests Made - 1, Size of Download (Bytes) - ")
    perf_file.write(str(len(response.content)))
    perf_file.write("\n\n")
    perf_file.close()
    countryNested_data = response.json()

    data = {}
    for code in countryNested_data.keys():
        lang_d =  countryNested_data[code]['languages']
        official = []
        for lang in lang_d.keys():
            if lang_d[lang]['IsOfficial'] == "T":
                official.append(lang)
        
        data[countryNested_data[code]['Name']] = listToString(official)
        
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