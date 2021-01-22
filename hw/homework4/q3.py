from pyspark.sql import SparkSession
import pyspark.sql.functions as f
spark = SparkSession.builder.appName('q3').getOrCreate()

country_df = spark.read.json('country.json')
countrylanguage_df = spark.read.json('countrylanguage.json')

north_american_df = country_df[country_df["Continent"] == 'North America'][["Name", "Code"]]
lang_official_df = countrylanguage_df[countrylanguage_df["IsOfficial"] == 'T'][["CountryCode", "Language"]]

country_lang = north_american_df.join(lang_official_df, north_american_df.Code == lang_official_df.CountryCode)[["Name", "Language"]].orderBy("Name")
country_lang.groupby("Name").agg(f.concat_ws(", ", f.collect_list(country_lang["Language"])).alias('Language')).limit(10).show()