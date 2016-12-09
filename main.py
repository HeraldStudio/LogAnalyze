#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 26, 2016
    Author: corvofeng@gmail.com
"""


import sys
from getopt import getopt
import analyze
from analyze import dir_analyze


def usage():
    print("help")


if __name__ == "__main__":
    opts, args = getopt(sys.argv[1:], "hi:l:d:")
    for op, value in opts:
        if op == "-l":
            analyze.dir_analyze.process_every_file(value, 'tmp')
        elif op == "-d":
            analyze.dir_analyze.process_dir(value)
        elif op == "-h":
            usage()
        else:
            usage()

    print("finish, have fun")
