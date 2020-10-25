from mysql.connector import Error
import mysql.connector
import json
import sys

date = sys.argv[1]
output_file_name = sys.argv[2]

cnx = mysql.connector.connect(user = 'dsci551', password = 'dsci551', database = 'covid19')
output_dict = {}

def create_report(date, output_file_name):
    """ Find the number of confirmed and deceased cases by gender, age, and province."""
    global cnx
    date_formatted = date[3:] + '-' + date[0:2] + '%'
    prev_month = int(date[0:2])
    if prev_month < 10:
        prev_month_str  = '0' + str(prev_month-1)
    else:
        prev_month_str = str(prev_month-1)
    previous_date_formatted = date[3:] + '-' + prev_month_str + '%'

    args = [date_formatted, previous_date_formatted, date_formatted, previous_date_formatted, previous_date_formatted]

    # Gender Query:
    cursor = cnx.cursor()
    gender_query = ("select date, sex, confirmed, deceased from (select * from timegender where date like '{}' OR date like '{}') as t" +
            " where date >= ALL (select date from timegender where date like '{}')" +
            " OR (date like '{}' and date >= ALL (select date from timegender where date like '{}')) order by date desc;").format(*args)
    cursor.execute(gender_query)
    vals = cursor.fetchall()
    format_dict(vals, "gender")
    cursor.close()

    # Age Query:
    cursor = cnx.cursor()
    age_query = ("select date, age, confirmed, deceased from (select * from timeage where date like '{}' OR date like '{}') as t" +
            " where date >= ALL (select date from timeage where date like '{}')" +
            " OR (date like '{}' and date >= ALL (select date from timeage where date like '{}')) order by date desc;").format(*args)
    cursor.execute(age_query)
    vals = cursor.fetchall()
    format_dict(vals, "age")
    cursor.close()

    # Province Query:
    cursor = cnx.cursor()
    province_query = ("select date, province, confirmed, deceased from (select * from timeprovince where date like '{}' OR date like '{}') as t" +
            " where date >= ALL (select date from timeprovince where date like '{}')" +
            " OR (date like '{}' and date >= ALL (select date from timeprovince where date like '{}')) order by date desc;").format(*args)
    cursor.execute(province_query)
    vals = cursor.fetchall()
    format_dict(vals, "province")
    cursor.close()

    with open(output_file_name, 'w') as fp:
        json.dump(output_dict, fp, indent=4)
    return

def format_dict(vals, key):
    global output_dict
    group_dict = {}
    for row in vals:
        cd_dict = {}
        date, group, confirmed, deceased = row[0], row[1], row[2], row[3]
        cd_dict["confirmed"] = confirmed
        cd_dict["deceased"] = deceased
        if group not in group_dict:
            group_dict[group] = cd_dict
        else:
            group_dict[group]["confirmed"] = group_dict[group]["confirmed"] - cd_dict["confirmed"]
            group_dict[group]["deceased"] = group_dict[group]["deceased"] - cd_dict["deceased"]
        
    output_dict[key] = group_dict
    return

create_report(date, output_file_name)
    

