#!/usr/bin/env python
# get wiki edit log from
# scp ros@ros1.osuosl.org:/var/www/wiki.ros.org/data/edit-log .
# Set the year and month below

import time

expected_year = 2023
expected_month = 7


count = 0

with open('edit-log') as fh:
    for l in fh:
        elements = l.split()
        t = time.gmtime(int(elements[0])/1000000)

        if t.tm_year == expected_year and t.tm_mon == expected_month:
            # print t.tm_year, t.tm_mon
            count += 1


print("Count For {0}-{1} is {2}".format(expected_year, expected_month, count))
print("Count/day {0}".format(count/ 30.0))
