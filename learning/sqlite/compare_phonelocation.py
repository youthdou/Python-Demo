#https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432010494717e1db78cd172e4d52b853e7fd38d6985c000

import sqlite3
import xlrd
import time
import requests
#from bs4 import BeautifulSoup
#import html5lib

import threading
import queue
import random
import time
import multiprocessing


def queryNumber(strNumber):
    url = 'http://v.showji.com/Locating/showji.com2016234999234.aspx?m=%s&output=json&callback=querycallback&timestamp=%d' % (strNumber, time.time())
    r = requests.get(url)
    #print(r.url)
    #print(r.text)
    #print(r.status_code)
    result = {}
    if r.text.strip().startswith('querycallback('):
        result = eval(r.text.lstrip('querycallback(').rstrip(');'))
    else:
        print(r.url)
    #for key in result:
    #    print('%s:%s' % (key, result[key]))
    return result


def getTypes(details):
    if details.get('VNO', '') == '':
        return details.get('Corp', '')

    return details.get('Corp', '') + ' ' + details.get('VNO')


def updateRecord(cursor, strNumber, strInfos, file):
    details = queryNumber(strNumber)
    if details.get('QueryResult', 'False') == 'False':
        file.write(strNumber + ',' + strInfos + ',\n')
        return

    strProvince, strCity, strIsp = strInfos.split('#')
    if strProvince != details.get('Province', '').strip():
        file.write(strNumber + ',' + strInfos + ',\n')
        return
    if strCity != details.get('City', '').strip():
        file.write(strNumber + ',' + strInfos + ',\n')
        return
    if strIsp != details.get('Corp', '').strip().lstrip('中国'):
        file.write(strNumber + ',' + strInfos + ',\n')
        return

    cursor.execute('update T_PhoneLocation set prefix = ?, province = ?, city = ?, isp = ?, code = ?, zip = ?, types = ? where phone = ?;',
                   (strNumber[0:3],
                    strProvince,
                    strCity,
                    strIsp,
                    details.get('AreaCode', ''),
                    details.get('PostCode', ''),
                    getTypes(details),
                    strNumber))

#prefix, phone, province, city, isp, code, zip, types
def insertRecord(cursor, strNumber, strInfos, file):
    if len(strInfos.split('#')) != 3:
        strTypes = strInfos.strip().lstrip('【').rstrip('】')
        cursor.execute('insert into T_PhoneLocation values (?, ?, ?, ?, ?, ?, ?, ?);',
                       (strNumber, strNumber, '', '', '', '', '', strTypes))
        return

    details = queryNumber(strNumber)
    if details.get('QueryResult', 'False') == 'False':
        file.write(strNumber + ',' + strInfos + ',\n')
        return

    strProvince, strCity, strIsp = strInfos.split('#')
    if strProvince != details.get('Province', '').strip():
        file.write(strNumber + ',' + strInfos + ',\n')
        return
    if strCity != details.get('City', '').strip():
        file.write(strNumber + ',' + strInfos + ',\n')
        return
    if strIsp != details.get('Corp', '').strip().lstrip('中国'):
        file.write(strNumber + ',' + strInfos + ',\n')
        return
    cursor.execute('insert into T_PhoneLocation values (?, ?, ?, ?, ?, ?, ?, ?);',
                   (strNumber[0:3],
                    strNumber,
                    strProvince,
                    strCity,
                    strIsp,
                    details.get('AreaCode', ''),
                    details.get('PostCode', ''),
                    getTypes(details)))


bRunning = True

lock = threading.Lock()

class Producer(threading.Thread):
    def __init__(self, name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=name)

    def run(self):


        global lock
        global bRunning
        with lock:
            bRunning = False


if __name__ == '__main__':
    #queryNumber('1700529')
    #queryNumber('5700523')

    startTime = time.time()
    conn = sqlite3.connect('phonesqlite.db')
    print('Open database successfully')
    cursor = conn.cursor()

    cursor.execute('select count(*) from "T_PhoneLocation";')
    #print("Total: " % (cursor[0][0],))
    values = cursor.fetchall()
    print('Total DB Rows: ', values[0][0])

    file = open('log.csv', 'w')
    file.write('number,excel,db\n')

    data = xlrd.open_workbook('phonelocation.xlsx')
    table = data.sheets()[0]
    print('Total Excel Rows: ', table.nrows)
    for row in range(table.nrows):
    #for row in range(1):
        strNumber = table.cell(row, 0).value
        strInfos = table.cell(row, 1).value.replace('★', '#').strip()

        strSql = 'select province, city, isp from "T_PhoneLocation" where phone = "%s";' % (strNumber)
        cursor.execute(strSql)
        values = cursor.fetchall()

        if len(values) != 0:
            strDBInfos = "%s#%s#%s" % (values[0][0].strip(), values[0][1].strip(), values[0][2].strip())
            if strDBInfos != strInfos:
                #file.write(strNumber + ',' + strInfos + ',' + strDBInfos + '\n')
                updateRecord(cursor, strNumber, strInfos, file)
        else:
            #file.write(strNumber + ',' + strInfos + ',\n')
            insertRecord(cursor, strNumber, strInfos, file)

    file.close()
    conn.close()
    print('Run time: %fs' % (time.time() - startTime))
