#http://www.lfhacks.com/tech/python-read-specific-row-csv
#https://docs.python.org/3/library/csv.html#

import csv

with open('/mnt/hgfs/Share/phonelocation.csv', 'r') as f:
    #print('Total: %d' % (len(f.readlines()), ))
    reader = csv.reader(f)
    row = []
    for i,rows in enumerate(reader):
        if i == 2:
            row = rows
            #print(rows)

    print(row)