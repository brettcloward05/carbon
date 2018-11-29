#!/usr/bin/env python3
"""
Module Documentation Here
"""
from __future__ import print_function
import datetime
import sqlite3


def main(beg_date, end_date):
    """
    This module takes a beginning and ending date and queries hw8SQLite.db for
    all transactions in the date range
    param:  beg_date: the beginning date to be queried in the format YYYYMMDD
            end_date: the ending date to be queried in the format YYYYMMDD
    """
    if not (beg_date.isdigit() and len(beg_date) == 8):
        print("Beginning date is not in the correct format!")
        exit(1)
    if not (end_date.isdigit() and len(end_date) == 8):
        print("Ending date is not in the correct format !")
        exit(1)

    format_str = '%Y%m%d%H%M'

    b_date = datetime.datetime.strptime(beg_date+'0000', format_str)
    e_date = datetime.datetime.strptime(end_date+'2359', format_str)
    print(b_date)
    print(e_date)
    conn = sqlite3.connect('hw8SQLite.db')
    cur = conn.cursor()
    # TODO: finish formatting
    statement = """SELECT
                    SUBSTR('000000'||REPLACE(PRINTF("%.2f",t.total), '.', ''), -6),
                    substr('00000'||t.trans_id, -5),
                    strftime('%Y%m%d%H%M', t.trans_date),
                    substr(t.card_num, -6),
                    SUBSTR( '00'||PRINTF("%.0f",b.qty), -2),
                    SUBSTR('000000'||REPLACE(PRINTF("%.2f",b.amt), '.', ''), -6),
                    IFNULL(substr(b.prod_desc||'          ', 0, 11), '          ')
                FROM trans t
                LEFT JOIN
                    (SELECT *
                    FROM trans_line tl
                    INNER JOIN products p on p.prod_num = tl.prod_num
                    ) b ON t.trans_id = b.trans_id
                WHERE t.trans_date BETWEEN '"""+ str(b_date)+ """' AND '""" + str(e_date) + """';"""
    cur.execute(statement)
    data = cur.fetchall()
    #print(type(data[0]))
    transactions = list()

    for row in data:
        if int(row[1]) > len(transactions):
            transactions.append(list(row))
        else:
            transactions[int(row[1])-1].extend([row[4], row[5], row[6]])

    for trans in transactions:
        while len(trans) < 13:
            trans.extend(['00', '000000', '          '])
        trans.append(trans[0])
        trans.pop(0)

    for stuff in transactions:
        print(stuff)



if __name__ == "__main__":
    main('20170401', '20181130')
    exit(0)
