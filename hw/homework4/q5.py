from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('q5').getOrCreate()

country_df = spark.read.json('country.json')
countrylanguage_df = spark.read.json('countrylanguage.json')

french_countries = countrylanguage_df[(countrylanguage_df["IsOfficial"] == 'T') & (countrylanguage_df["Language"] == 'French')][["CountryCode"]]

country_df = country_df.join(french_countries, country_df.Code == french_countries.CountryCode, how = 'inner')[["Name", "Continent"]]

country_grpd = country_df.groupby("Continent").agg({'*': 'count'})
country_grpd.withColumnRenamed("Count(1)", "Count").show()