import csv
import xlrd
import time
import sqlite3
import os
import shutil

def savAsCommonFile(strLogFile):
    strCommoneFile = '/mnt/hgfs/Share/log.csv'

    if os.path.exists(strCommoneFile):
        os.remove(strCommoneFile)

    shutil.copy(strLogFile, strCommoneFile)

if __name__ == '__main__':
    #queryNumber('1700529')
    #queryNumber('5700523')

    startTime = time.time()


    conn = sqlite3.connect('/mnt/hgfs/Share/phonesqlite.db')
    print('Open database successfully')
    cursor = conn.cursor()

    cursor.execute('select count(*) from "T_PhoneLocation";')
    values = cursor.fetchall()
    print('Total DB Rows: ', values[0][0])

    strLogFileName = '/mnt/hgfs/Share/log-%d.csv' % (time.time(),)
    file = open(strLogFileName, 'w')
    file.write('type,number,excel,db\n')

    data = xlrd.open_workbook('/mnt/hgfs/Share/phonelocation.xlsx')
    #data = xlrd.open_workbook('/mnt/hgfs/Share/test.xlsx')
    table = data.sheets()[0]
    print('Total Excel Rows: ', table.nrows)

    for row in range(table.nrows):
    #for row in range(1):
        strNumber = table.cell(row, 0).value
        strInfos = table.cell(row, 1).value.replace('★', '#').strip()

        strSql = 'select province, city, isp, types from "T_PhoneLocation" where phone = "%s";' % (strNumber)
        cursor.execute(strSql)
        values = cursor.fetchall()

        if len(values) != 0:
            strDBInfos = ''
            if len(strInfos.split('#')) == 3:
                strDBInfos = "%s#%s#%s" % (values[0][0].strip(), values[0][1].strip(), values[0][2].strip())
            else:
                strInfos = strInfos.strip().lstrip('【').rstrip('】')
                strDBInfos = values[0][3]

            if strDBInfos != strInfos:
                file.write('update,' + strNumber + ',' + strInfos + ',' + strDBInfos + '\n')
        else:
            file.write('insert,' + strNumber + ',' + strInfos + ',\n')

    file.close()
    conn.commit()
    conn.close()

    savAsCommonFile(strLogFileName)

    print('Run time: %fs' % (time.time() - startTime))