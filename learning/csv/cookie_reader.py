import csv


with open("cookies.txt", 'r') as fCsv:
    csvReader  = csv.reader(fCsv)
    f = open("cookies.dat", 'w')
    next(csvReader)
    for row in csvReader:
        #print(row)
        if row[0] == 'acw_tc':
            continue
        strCookie = "%s=%s; expires=%s; domain=%s; path=%s\n" % (row[0], row[1], row[4], row[2], row[3])
        print(strCookie)
        f.write(strCookie)
    f.close()
    fCsv.close()