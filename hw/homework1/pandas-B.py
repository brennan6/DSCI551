from helper import listToString
import pandas as pd
import numpy as np
import sys

country_path = sys.argv[1]
city_path = sys.argv[2]
countryLang_path = sys.argv[3]

country_df = pd.read_json(country_path)
countryLang_df = pd.read_json(countryLang_path)

def findCountriesLang():
    """Find names of countries and their official languages for all countries in “North America”"""
    officialLang_df = countryLang_df[countryLang_df['IsOfficial'] == 'T']
    merged_df = country_df.merge(officialLang_df, how = 'left', left_on = "Code", right_on = "CountryCode")
    merged_df = merged_df[(merged_df['Continent'] == 'North America')].loc[:, ['Name', 'Language']].sort_values(by=['Name'])
    merged_df['Language'] = merged_df['Language'].fillna('None')

    langaugeLists = merged_df.groupby(['Name'])['Language'].apply(list)
    formatted_df = pd.DataFrame({'Name': np.unique(merged_df['Name']), 'languages': langaugeLists})
    vals = formatted_df.values

    #For loop for sake of printing:
    for country in vals:
        str1 = ''
        str1 += country[0]
        str1 += ', '
        str1 += listToString(country[1])
        print(str1)
    return None

findCountriesLang()