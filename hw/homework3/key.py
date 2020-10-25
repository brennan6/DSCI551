from mysql.connector import Error
import mysql.connector
import json
import sys

table = sys.argv[1]
potential_key = sys.argv[2]

cnx = mysql.connector.connect(user = 'dsci551', password = 'dsci551', database = 'covid19')

def check_key(table, potential_key):
    global cnx
    cursor = cnx.cursor()
    key_query = "select {}, count(*) from dsci551.{} group by {} having count(*) > 1 order by count(*) desc limit 5;".format(potential_key, table, potential_key)
    cursor.execute(key_query)
    duplicate_rows = cursor.fetchall()
    if len(duplicate_rows) == 0:
        print('yes')
    else:
        result_len = len(duplicate_rows[0])
        for result in duplicate_rows:
            formatted_result = ''
            i = 0
            while i < result_len:
                formatted_result += str(result[i]) + ' '
                i += 1
            print(formatted_result)
            
check_key(table, potential_key)