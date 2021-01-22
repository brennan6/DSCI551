from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('q1').getOrCreate()

country_df = spark.read.json('country.json')

europe_gnp = country_df[(country_df['Continent'] == 'Europe') & (country_df['GNP'] >= 100000) & (country_df['GNP'] <= 500000)]
europe_gnp[['Name']].show()