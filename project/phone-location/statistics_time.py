import xlrd
import sys
import time
import calendar
from calendar import Calendar
import datetime

def statistics_time(excelName):
    data = xlrd.open_workbook(excelName)
    table = data.sheets()[0]
    print('%d:%d' % (table.nrows, table.ncols))
   # print('%s' % (table.cell(0, 0).value,))
    #for strValue in table.cell(0, 1).value.split('★'):
    #    print(',', strValue)
    #print('%s' % (table.cell(1, 3).value,))

    '''
    strDateTime = table.cell(1, 3).value
    timestamp = time.mktime(time.strptime(strDateTime, "%Y/%m/%d %H:%M:%S"))
    print(time.localtime(timestamp))
    '''
    year = 2017
    listMonths = [7, 8, 9]
    dicDays = {}

    for month in listMonths:
        for d in Calendar().itermonthdates(year, month):
            if month != d.month:
                continue
            if d.weekday() in [0, 1, 3]:
                #strDate = "%d/%d/%d" % (year, month, day)
                print(d)
                dicDays[d] = False
    print("All valid date: ", len(dicDays))
    #print(dicDays)

    #return

    iTotalTime = 0
    for iRow in range(table.nrows)[1:]:
        strDateTime = table.cell(iRow, 3).value
        strDate = strDateTime.split(" ")[0].strip()
        timestamp = time.mktime(time.strptime(strDateTime, "%Y/%m/%d %H:%M:%S"))
        localtime = time.localtime(timestamp)
        d = datetime.date(localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
        if d not in dicDays:
            continue
        if dicDays.get(d, False):
            continue
        if localtime.tm_hour > 19:
            print(strDateTime)
            #iTotalTime += localtime.tm_hour - 19
            iTotalTime += 2
            dicDays[d] = True
    print("[%s]Total time: [%d]" % (excelName.strip('.xlsx'), iTotalTime))

    print('Lost date:')
    for d in dicDays:
        if not dicDays[d]:
            print(d)

if __name__ == '__main__':

    if len(sys.argv) > 2:
        statistics_time(sys.argv[1])
    else:
        statistics_time('沈伟伟.xlsx')