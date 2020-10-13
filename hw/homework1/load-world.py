import requests
import sys
import json

country_path = sys.argv[1]
city_path = sys.argv[2]
countryLang_path = sys.argv[3]

def loadToFirebase():
    """loads the data in the JSON files to your Firebase database, under a node “world"”"""
    url = 'https://hw1-dsci551-31309.firebaseio.com/.json'
    response = requests.delete(url)

    #Add Country Data:
    with open(country_path) as f:
        country_data = json.load(f)

    country = {}
    for val in country_data:
        country[val['Code']] = {k:v for k,v in val.items() if k != 'Code'}
        
    json_country = json.dumps(country)
    urlCountry = 'https://hw1-dsci551-31309.firebaseio.com/world/country.json'
    response = requests.put(urlCountry, json_country)

    #Add City Data:
    with open(city_path) as f:
        city_data = json.load(f)
        
    city = {}
    for val in city_data:
        city[val['ID']] = {k:v for k,v in val.items() if k != 'ID'}
        
    json_city = json.dumps(city)
    urlCity = 'https://hw1-dsci551-31309.firebaseio.com/world/city.json'
    response = requests.put(urlCity, json_city)

    #Add Country Language Data:
    with open(countryLang_path) as f:
        countryLang_data = json.load(f)
        
    country_lang = Dictlist()
    for val in countryLang_data:
        country_lang[val['CountryCode']] = {k:v for k,v in val.items() if k != 'CountryCode'}
        
    countryLangFinal = {}
    for key in country_lang.keys():
        med = {}
        for val in country_lang[key]:
            med[val['Language']] = {k:v for k,v in val.items() if k != 'Language'}
        countryLangFinal[key] = med  
        
    json_countryLang = json.dumps(countryLangFinal)
    urlCountryLang = 'https://hw1-dsci551-31309.firebaseio.com/world/countryLanguage.json'
    response = requests.put(urlCountryLang, json_countryLang)

    #Add County Nested Data:
    country_nested = country
    for key in country_nested.keys():
        nested = countryLangFinal.get(key)
        country_nested[key]['languages'] = nested
        
    json_countryNested = json.dumps(country_nested)
    urlCountryNested = 'https://hw1-dsci551-31309.firebaseio.com/world/country_nested.json'
    response = requests.put(urlCountryNested, json_countryNested)

    return None

# Helper Class to deal with multiple Languages:
class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


loadToFirebase()