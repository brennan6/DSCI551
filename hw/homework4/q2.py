from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('q2').getOrCreate()

country_df = spark.read.json('country.json')
city_df = spark.read.json('city.json')
city_df = city_df.withColumnRenamed("Name", "City_Name")

north_american_df = country_df[country_df["Continent"] == 'North America'][["Name", "Capital"]]
na_country_capital = north_american_df.join(city_df, north_american_df.Capital == city_df.ID)[["Name", "City_Name"]]
na_country_capital = na_country_capital.withColumnRenamed("City_Name", "Capital")
na_country_capital.orderBy("Name").limit(10).show()