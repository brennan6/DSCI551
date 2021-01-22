from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('q4').getOrCreate()

country_df = spark.read.json('country.json')

country_df = country_df[country_df["GNP"] > 10000]

country_df.groupby("Continent").agg({"LifeExpectancy": 'avg'}).show()