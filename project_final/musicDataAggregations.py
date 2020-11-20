from pyspark.sql import SparkSession
import json

""" (3) Spark Aggregation of Song Data and Rank Data prior to Upload to Firebase """
spark = SparkSession.builder.appName('musicDataAggregation').getOrCreate()

song_df = spark.read.json('./artist_data.json')
rank_df = spark.read.json('./ranks_data.json')

rank_grpd = rank_df.groupby("song").agg({"score": 'avg', "*": "count"})
song_agg_df = song_df.join(rank_grpd, song_df.title == rank_grpd.song, how = 'left').fillna({"avg(score)": '0', "count(1)": 0})
song_agg_df = song_agg_df.withColumnRenamed("count(1)", "count")
song_agg_df = song_agg_df.withColumnRenamed("avg(score)", "avg_score")

def create_firebase_dict(df):
    artists_dict = {}
    artists_dict["songs"] = []
    for row in df.collect():
        artists_dict['songs'].append({
            'title': row['title'],
            'artist': row['artist'],
            'album': row['album'],
            'year': row['year'],
            'avg_rank': row['avg_score'],
            'count_ranks': row['count'],
            'featured_artists': row['featured_artists'],
            'writer_artists': row['writer_artists'],
            'image_url': row['image_url'],
            'image_height': row['image_height'],
            'image_width': row['image_width'],
            'lyrics': row['lyrics']
        })
    return artists_dict


artists_dict = create_firebase_dict(song_agg_df)

def write_json_file(results):
    with open('pyspark_output.json', 'w') as outfile:
        json.dump(results, outfile)


write_json_file(artists_dict)
