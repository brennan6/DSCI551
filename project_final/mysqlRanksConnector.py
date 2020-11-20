from mysql.connector import Error
import mysql.connector
import json

cnx = mysql.connector.connect(host = 'project-dsci551-ranks.c8u9e3pxnupz.us-east-1.rds.amazonaws.com',
                            user = 'mbrennan6', password = 'songdsci551', database = 'songRanks')

def pull_down_ranks():
    """ (2) Pull down all of the necessary data from the Ranks MySQL Database in RDS """
    global cnx
    ranks_dict = {}
    ranks_dict["ranks"] = []
    cursor = cnx.cursor()
    query = "select * from ranks;"
    cursor.execute(query)
    rows = cursor.fetchall()

    for rank in rows:
        ranks_dict["ranks"].append({"song": rank[0], "score": rank[1]})

    return ranks_dict

def write_json_file(dict_ranks):
    with open('ranks_data.json', 'w') as outfile:
        json.dump(dict_ranks["ranks"], outfile)

ranks_d = pull_down_ranks()
write_json_file(ranks_d)

