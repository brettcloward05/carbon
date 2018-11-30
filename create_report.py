#!/usr/bin/env python3
"""
Module Documentation Here
"""
from __future__ import print_function
import datetime
import sqlite3
import sys


def usage_function():
    """
    Shows the usage of the program
    """
    print("Usage:", sys.argv[0], " beg_date end_date")
    print("param:beg_date: the starting date to query for transactions in the "
          "format: YYYYMMDD")
    print("param:end_date: the ending date to query for transactions in the "
          "format: YYYYMMDD")



def main(beg_date, end_date):
    """
    This module takes a beginning and ending date and queries hw8SQLite.db for
    all transactions in the date range
    param:  beg_date: the beginning date to be queried in the format YYYYMMDD
            end_date: the ending date to be queried in the format YYYYMMDD
    """
    # Check that the dates provided are in the correct format
    if not (beg_date.isdigit() and len(beg_date) == 8):
        print("Beginning date is not in the correct format!")
        exit(1)
    if not (end_date.isdigit() and len(end_date) == 8):
        print("Ending date is not in the correct format !")
        exit(1)

    # Format the dates provided so they can be used for the sql query
    format_str = '%Y%m%d%H%M'

    b_date = datetime.datetime.strptime(beg_date+'0000', format_str)
    e_date = datetime.datetime.strptime(end_date+'2359', format_str)

    # connect to sql database
    conn = sqlite3.connect('hw8SQLite.db')
    cur = conn.cursor()

    # Statement to retrieve the data in the date range provided, this statement
    # will grab all of the data and format it
    # Note: it does not fill in missing info, but it does correctly
    # format NULL values
    statement = """SELECT
                    SUBSTR('000000'||REPLACE(PRINTF("%.2f",t.total), '.', ''), -6),
                    SUBSTR('00000'||t.trans_id, -5),
                    STRFTIME('%Y%m%d%H%M', t.trans_date),
                    SUBSTR(t.card_num, -6),
                    SUBSTR( '00'||PRINTF("%.0f",b.qty), -2),
                    SUBSTR('000000'||REPLACE(PRINTF("%.2f",b.amt), '.', ''), -6),
                    IFNULL(SUBSTR(b.prod_desc||'          ', 0, 11), '          ')
                FROM trans t
                LEFT JOIN
                    (SELECT *
                    FROM trans_line tl
                    INNER JOIN products p on p.prod_num = tl.prod_num
                    ) b ON t.trans_id = b.trans_id
                WHERE t.trans_date BETWEEN '"""+ str(b_date)+ """' AND '""" + str(e_date) + """';"""
    cur.execute(statement)
    data = cur.fetchall()

    transactions = list()

    # Takes all of the transaction lines from the same transaction and puts them
    # all in one list
    for row in data:
        if int(row[1]) > len(transactions):
            transactions.append(list(row))
        else:
            transactions[int(row[1])-1].extend([row[4], row[5], row[6]])

    # Fills in the transactions so they will be the correct length
    # For instance if a transaction only had 1 transaction line it will fill
    # in blank values so that the transaction will be long enough
    # Afterwords it takes the total, which was stored at the front, and moves it
    # to the end
    for trans in transactions:
        while len(trans) < 13:
            trans.extend(['00', '000000', '          '])
        trans.append(trans[0])
        trans.pop(0)

    # If we got no data from our query then it will let you know and exit the
    # program with exit code 2
    if not transactions:
        print("No transactions recorded between", b_date, "and", e_date)
        exit(2)
    if transactions:
        print(transactions)

    # Creates a file and stores each transaction on their own line
    with open('company_trans_%s_%s.dat'%(beg_date, end_date), mode='w+',
              encoding='utf-8') as my_file:
        for trans in transactions:
            my_file.write(''.join(trans)+"\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage_function()
    else:
        main(sys.argv[1], sys.argv[2])
    exit(0)
