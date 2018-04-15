import sys
import os.path
from db import Db


def print_and_rewind(s):
    sys.stdout.write("\r"+s)
    sys.stdout.flush()


def migrate(csv_file):
    with open(csv_file) as f:
        with Db() as db:
            print 'Emptying database'
            db.drop()
            db.create_table()

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
                    print_and_rewind("Processed lines: %i" % line_number)

            db.commit()

            print_and_rewind("Added lines: %i\n" % line_number)
            print 'Stored', stored_count, 'rows'
            print 'Rejected', rejected_count, 'rows'


csv_file = sys.argv[1]
if not os.path.isfile(csv_file):
    print 'File',csv_file,'does not exist'
    exit(1)

answer = raw_input('This will erase the database and import data from CSV file. Are you sure? (yes/no):')
if answer != 'yes':
    exit(2)

migrate(csv_file)
