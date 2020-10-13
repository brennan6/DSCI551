import pandas as pd
import sys

country_path = sys.argv[1]
city_path = sys.argv[2]
countryLang_path = sys.argv[3]

country_df = pd.read_json(country_path)

def findContinentLifeExpectancy():
    """Find, for each continent, the average life expectancy of all countries in the continent which has at least 5 countries whose GNP is more than 10000."""
    count_df = country_df[country_df['GNP'] > 10000].groupby('Continent').count()[['Name']]
    qualifying_countries = count_df[count_df['Name'] >= 5].index.values
    vals = country_df.groupby(['Continent']).mean()[['LifeExpectancy']].loc[qualifying_countries, :].reset_index(drop=True).values
    results = pd.DataFrame({'Name': qualifying_countries, 'LifeExpectancy': vals.reshape(1,-1).flatten()}).values

    #For loop for sake of printing:
    for country in results:
        str1 = ''
        str1 += country[0]
        str1 += ", "
        str1 += str(country[1])
        print(str1)
    return None

findContinentLifeExpectancy()

