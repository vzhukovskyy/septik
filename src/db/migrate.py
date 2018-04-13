#!/usr/bin/python

from db import Db

with open('sensors.csv') as f:
    with Db() as db:
        db.empty()

        line_number = 1
        stored_count = 0
        rejected_count = 0

        for line in f:
            time, cputemp, temp, press, hum, flow, level = line.strip().split(',')

            if time == 'time' or time == '':
                #skip header and empty line
                continue

            data = dict(time=time,cpu_temperature=cputemp,outside_temperature=temp,pressure=press,humidity=hum,flow=flow,level=level)

            stored = db.store(data, commit=False)
            if stored:
                stored_count += 1
            else:
                rejected_count += 1

            line_number += 1
            if line_number % 1000 == 0:
                print 'line',line_number

        db.commit()

        print 'Stored', stored_count, 'rows'
        print 'Rejected', rejected_count, 'rows'
