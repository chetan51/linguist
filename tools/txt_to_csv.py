#!/usr/bin/env python
# ----------------------------------------------------------------------
# Chetan Surpur
# Copyright (C) 2013
# ----------------------------------------------------------------------

"""A tool to convert text into csv format for Linguist."""

import sys
import re

def convert(datapath):
    data = file(datapath).read()
    data = re.sub(' +', ' ', data)
    data = re.sub('\n+', '\n', data)
    N = len(data)

    print "letter"
    print "string"
    print ""

    for i in xrange(0, N):
        c = data[i]
        if ord(c) > 31 and ord(c) < 127:
            print c
        if ord(c) == 10:
            print '|'

if __name__ == "__main__":
    if len(sys.argv) > 1:
        datapath = sys.argv[1]
        convert(datapath)
    else:
        print "Usage: python linguist.py [path/to/data.txt]"
