import sys
import json
import requests

def findContinentLifeExpectancy():
    """Find, for each continent, the average life expectancy of all countries in the continent which has at least 5 countries whose GNP is more than 10000."""
    url = 'https://hw1-dsci551-31309.firebaseio.com/world/country.json?orderBy="GNP"&startAt=10000&print=pretty' 
    response = requests.get(url)
    perf_file = open("performance.txt","a")
    perf_file.write("firebase-C: Requests Made - 2, Size of 1st Download (Bytes) - ")
    perf_file.write(str(len(response.content)))
    filteredGNP = response.json()

    counts_GNP = {}
    for key in filteredGNP.keys():
        continent = filteredGNP[key]['Continent']
        if continent in counts_GNP.keys():
            counts_GNP[continent] = counts_GNP[continent] + 1
        else:
            counts_GNP[continent] = 1
    counts_GNP = {k:v for k,v in counts_GNP.items() if v >= 5}

    url = 'https://hw1-dsci551-31309.firebaseio.com/world/country.json'
    response = requests.get(url)
    perf_file.write(", Size of 2nd download (Bytes) - ")
    perf_file.write(str(len(response.content)))
    perf_file.write("\n\n")
    perf_file.close()
    country_data = response.json()

    data_le = {}
    total = {}
    for key in country_data.keys():
        continent = country_data[key]['Continent']
        if continent in counts_GNP.keys():
            if continent in data_le.keys():
                data_le[continent] = data_le[continent] + country_data[key]['LifeExpectancy']
                total[continent] = total[continent] + 1
            else:
                data_le[continent] = country_data[key]['LifeExpectancy']
                total[continent] = 1
                
    data = {k:(v/total[k]) for k,v in data_le.items()}
    data = dict(sorted(data.items()))

    for k,v in data.items():
        str1 = k
        str1 += ", "
        str1 += str(v)
        print(str1)

    writeAnalysis()
    return None

def writeAnalysis():
    """Writes the final Analysis of why certain queries were choosen."""
    perf_file = open("performance.txt","a")
    perf_file.write("Analysis: The download URL's choosen were done so with the intent of limiting the number of bytes \n"
                + "that are shown for each individual table. I found that the easist means to accomplish this was to \n"
                + "utilize the filtration of North America for parts A, B, and B-nested. This could be done using the orderBy and equalTo methods. \n"
                + "Additionally, for part C I found that I could filter on GNP by starting at the threshold value of 10000. \n"
                + "This was accomplished by using the orderBy and startAt methods.")
    perf_file.close()

findContinentLifeExpectancy()