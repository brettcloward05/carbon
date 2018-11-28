#!/usr/bin/env python3
"""
Module Documentation Here
"""
from __future__ import print_function
import datetime


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
    print(date)


if __name__ == "__main__":
    main('20181128', '20181130')
    exit(0)
