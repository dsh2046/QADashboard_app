#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""命令行火车票查看器

Usage:
     tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
from docopt import docopt
from stations import stations
import requests
from prettytable import *


def pretty_print():
    pt = PrettyTable()
    pt._set_field_names(['name','age','gender'])
    for x in range(3):
        pt.add_row(['q','r','o'])
    print(pt)

if __name__ == '__main__':
    pretty_print()