from mysql.connector import Error
import mysql.connector
import json
import sys

id_ = sys.argv[1]

cnx = mysql.connector.connect(user = 'dsci551', password = 'dsci551', database = 'covid19')
trace_list = []

def trace_infection(id_):
    """ Trace the origins of the infection from one positive case to the next until a loop or dead end emerges. """
    global cnx, trace_list
    trace_list.append(id_)
    cursor = cnx.cursor()
    infected_query = "select infected_by from patientinfo where patient_id like '{}'".format(id_)
    cursor.execute(infected_query)
    infected_id = cursor.fetchall()
    
    if not infected_id:                             # Deals with dead end.
        format_print(trace_list, False)
        return
    else:                                           # Deals with normal 1-1 and 1-2 case.
        next_id = infected_id[0][0].split(",")[0]
        if next_id == '':                           # Also deals with dead end.
            format_print(trace_list, False)
            return
        elif next_id in trace_list:                 # Deals with loop.
            trace_list.append(next_id)
            format_print(trace_list, True)
            return
        else:
            trace_infection(next_id)                # Keeps the search going

def format_print(id_list, cycle):
    if cycle:
        formatted_str = 'Cycle Found: '
    else:
        formatted_str = ''
    count = 0
    for id_ in id_list:
        if count < (len(id_list) - 1):
            formatted_str += id_ + ", "
            count += 1
        else:
            formatted_str += id_
            print(formatted_str)

trace_infection(id_)