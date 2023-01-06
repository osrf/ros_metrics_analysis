#!/usr/bin/env python

import time

expected_year = 2022
expected_month = 7


count = 0

with open('edit-log') as fh:
    for l in fh:
        elements = l.split()
        t = time.gmtime(int(elements[0])/1000000)

        if t.tm_year == expected_year and t.tm_mon == expected_month:
            # print t.tm_year, t.tm_mon
            count += 1


print "Count For %s-%s is %s"%(expected_year, expected_month, count)
print "Count/day %s"%(count/ 30.0)
