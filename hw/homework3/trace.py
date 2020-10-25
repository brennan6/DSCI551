from mysql.connector import Error
import mysql.connector
import json
import sys

id_ = sys.argv[1]

cnx = mysql.connector.connect(user = 'dsci551', password = 'dsci551', database = 'covid19')
trace_list = []

def trace_infection(id_):
    global cnx, trace_list
    trace_list.append(id_)
    cursor = cnx.cursor()
    infected_query = "select infected_by from patientinfo where patient_id like '{}'".format(id_)
    cursor.execute(infected_query)
    infected_id = cursor.fetchall()
    next_id = infected_id[0][0].replace(",", "")
    if next_id == '': # Deals with dead end.
        print(trace_list)
        return
    else: # Deals with normal 1-1 and 1-2 case.
        print(next_id)
        if next_id in trace_list: # Deals with loop.
            trace_list.append(next_id)
            print("Found Cycle: ", trace_list)
            return
        else:
            trace_infection(next_id) # Keeps the search going
        
trace_infection(id_)