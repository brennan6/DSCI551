from mysql.connector import Error
import mysql.connector
import json
import sys

date = sys.argv[1]
output_file_name = sys.argv[2]

cnx = mysql.connector.connect(user = 'dsci551', password = 'dsci551', database = 'covid19')

def create_report(date, output_file_name):
    global cnx

    date_formatted = date[3:] + '-' + date[0:2] + '%'
    prev_month = int(date[0:2])
    if prev_month < 10:
        prev_month_str  = '0' + str(prev_month-1)
    else:
        prev_month_str = str(prev_month-1)
    previous_date_formatted = date[3:] + '-' + prev_month_str + '%'

    args = [date_formatted, previous_date_formatted, date_formatted, previous_date_formatted, previous_date_formatted]
    #practice = "select date, sex, confirmed, deceased from (select * from timegender where date like '2020-03%' OR date like '2020-02%') as t where date >= ALL (select date from timegender where date like '2020-03%') OR (date like '2020-02%' and date >= ALL (select date from timegender where date like '2020-02%'));"
    cursor = cnx.cursor()
    gender_query = ("select date, sex, confirmed, deceased from (select * from timegender where date like '{}' OR date like '{}') as t" +
            " where date >= ALL (select date from timegender where date like '{}')" +
            " OR (date like '{}' and date >= ALL (select date from timegender where date like '{}')) order by date desc;").format(*args)
    cursor.execute(gender_query)
    vals = cursor.fetchall()
    #format_dict(vals)


    for row in vals:
        print(row)


    return

def format_dict(vals):
    output_dict = {}
    group_dict = {}
    for row in vals:
        cd_dict = {}
        date, group, confirmed, deceased = row[0], row[1], row[2], row[3]
        cd_dict["confirmed"] = confirmed
        cd_dict["deceased"] = deceased
        if group in group_dict:
            group_dict[group] = cd_dict
        else:
            group_dict[group]["confirmed"] = group_dict[group]["confirmed"] - cd_dict["confirmed"]
            group_dict[group]["deceased"] = group_dict[group]["deceased"] - cd_dict["deceased"]
        
    output_dict["gender"] = group_dict
    with open(output_file_name, 'w') as fp:
        json.dump(output_dict, fp)

create_report(date, output_file_name)
    

