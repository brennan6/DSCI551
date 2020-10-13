from helper import listToString
import pandas as pd
import sys

country_path = sys.argv[1]
city_path = sys.argv[2]
countryLang_path = sys.argv[3]

country_df = pd.read_json(country_path)
city_df = pd.read_json(city_path)

def findCountriesCapitals():
    """Find names of countries and their capital cities for all countries in “North America”"""
    merged_df = country_df.merge(city_df, how = 'left', left_on = "Capital", right_on = "ID").rename(columns = {'Name_x': 'CountryName', 'Name_y': 'CapitalName'})
    merged_df = merged_df.loc[:, ['CountryName', 'CapitalName', 'Continent']]
    vals = merged_df[merged_df['Continent'] == 'North America'][['CountryName', 'CapitalName']].sort_values(by=['CountryName']).values
    
    #For loop for sake of printing:
    for country in vals:
        print(listToString(country))
    return vals

findCountriesCapitals()