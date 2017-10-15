#https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432010494717e1db78cd172e4d52b853e7fd38d6985c000

import sqlite3
import xlrd
import time
import requests
from bs4 import BeautifulSoup
import html5lib

import threading
import queue
import random
import time
import multiprocessing

bRunning = True

iMaxCnt = 0

lock = threading.Lock()

def queryNumberV2(strNumber):
    url = 'http://www.ip138.com:8080/search.asp?action=mobile&mobile=%s' % (strNumber)
    r = requests.get(url)
    content = r.content.decode('gb2312')
    bsObj = BeautifulSoup(content, 'html5lib')
    listInfos = bsObj.find_all('td', {'class':'tdc2'})
    result = {}
    result['QueryResult'] = 'False'
    if len(listInfos) != 5:
        print(r.url)
        return result

    result['Mobile'] = strNumber
    result['QueryResult'] = 'True'
    strLocation = listInfos[1].getText()
    #print(strLocation, ':', len(strLocation.split('\xa0')))
    #print(list(strLocation))

    result['Province'] = strLocation.split('\xa0')[0]
    result['City'] = strLocation.split('\xa0')[1].rstrip('市')
    result['AreaCode'] = listInfos[3].getText()
    result['PostCode'] = listInfos[4].getText().split(' ')[0]
    result['VNO'] = ''
    result['Corp'] = listInfos[2].getText()

    if listInfos[2].getText().find('联通') != -1:
        result['TO'] = '联通'
    elif listInfos[2].getText().find('电信') != -1:
        result['TO'] = '电信'
    elif listInfos[2].getText().find('移动') != -1:
        result['TO'] = '移动'
    else:
        result['TO'] = ''


    #print(result)
    return result


def queryNumber(strNumber):
    result = {}
    result['QueryResult'] = 'False'
    with lock:
        global iMaxCnt
        if iMaxCnt > 100:
            iMaxCnt = iMaxCnt + 1
            return result

    time.sleep(2)
    url = 'http://v.showji.com/Locating/showji.com2016234999234.aspx?m=%s&output=json&callback=querycallback&timestamp=%d' % (strNumber, time.time())
    r = requests.get(url)
    #print(r.url)
    #print(r.text)
    #print(r.status_code)

    if r.text.strip().startswith('querycallback('):
        result = eval(r.text.lstrip('querycallback(').rstrip(');'))
    else:
        print('[%d]%s' % (iMaxCnt, r.url))
        return queryNumberV2(strNumber)
    #for key in result:
    #    print('%s:%s' % (key, result[key]))
    return result


def getTypes(details):
    if details.get('VNO', '') == '':
        return details.get('Corp', '')

    return details.get('Corp', '') + ' ' + details.get('VNO')


def updateRecord(strNumber, strInfos):
    details = queryNumber(strNumber)
    if details.get('QueryResult', 'False') == 'False':
        #file.write(strNumber + ',' + strInfos + ',\n')
        return (False, 'update,' + strNumber + ',' + strInfos + ',\n')

    #print(strInfos)
    strProvince, strCity, strIsp = strInfos.split('#')
    if strProvince != details.get('Province', '').strip():
        return (False, 'update,' + strNumber + ',' + strInfos + ',\n')
    if strCity != details.get('City', '').strip():
        return (False, 'update,' + strNumber + ',' + strInfos + ',\n')
    #if strIsp != details.get('TO', '').strip().lstrip('中国'):
    #    return (False, 'update,' + strNumber + ',' + strInfos + ',\n')

    strSql = "update T_PhoneLocation set prefix = '%s', province = '%s', city = '%s', isp = '%s', code = '%s', zip = '%s', types = '%s' where phone = '%s';" % (strNumber[0:3],
                 strProvince,
                 strCity,
                 strIsp,
                 details.get('AreaCode', ''),
                 details.get('PostCode', ''),
                 getTypes(details),
                 strNumber)

    return (True, strSql)

#prefix, phone, province, city, isp, code, zip, types
def insertRecord(strNumber, strInfos):
    if len(strInfos.split('#')) != 3:
        strTypes = strInfos.strip().lstrip('【').rstrip('】')
        strSql = "insert into T_PhoneLocation values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (strNumber, strNumber, '', '', '', '', '', strTypes)
        return (True, strSql)

    details = queryNumber(strNumber)
    if details.get('QueryResult', 'False') == 'False':
        #file.write(strNumber + ',' + strInfos + ',\n')
        return (False, 'insert,' + strNumber + ',' + strInfos + ',\n')

    strProvince, strCity, strIsp = strInfos.split('#')
    if strProvince != details.get('Province', '').strip():
        return (False, 'insert,' + strNumber + ',' + strInfos + ',\n')
    if strCity != details.get('City', '').strip():
        return (False, 'insert,' + strNumber + ',' + strInfos + ',\n')
    #if strIsp != details.get('Corp', '').strip().lstrip('中国'):
    #    return (False, 'insert,' + strNumber + ',' + strInfos + ',\n')

    strSql = "insert into T_PhoneLocation values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (strNumber[0:3],
                    strNumber,
                    strProvince,
                    strCity,
                    strIsp,
                    details.get('AreaCode', ''),
                    details.get('PostCode', ''),
                    getTypes(details))

    return (True, strSql)




class Producer(threading.Thread):
    def __init__(self, name, inQ, outQ):
        self.inQ = inQ
        self.outQ = outQ
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            with lock:
                if not bRunning:
                    break
            if self.inQ.empty():
                continue
            #print('[%s]Size of inQ: %d' % (threading.current_thread().name, self.inQ.qsize()))
            qData = self.inQ.get()
            strNumber = qData[0]
            strInfos = qData[1]
            values = qData[2]
            #strExcelInfos = "%s#%s" % (strInfos.split('#')[0], strInfos.split('#')[1])
            if len(values) != 0:
                strDBInfos = "%s#%s#%s" % (
                    values[0][0].strip(), values[0][1].strip(), values[0][2].strip())
                if strDBInfos != strInfos:
                    if len(strInfos.split('#')) == 3:
                        #file.write(strNumber + ',' + strInfos + ',' + strDBInfos + '\n')
                        self.outQ.put(updateRecord(strNumber, strInfos))

            else:
                #file.write(strNumber + ',' + strInfos + ',\n')
                self.outQ.put(insertRecord(strNumber, strInfos))





if __name__ == '__main__':
    #queryNumber('1700529')
    #queryNumber('5700523')

    startTime = time.time()
    inQ = queue.Queue()
    outQ = queue.Queue()

    producerList = []
    for i in range(2):
        p = Producer(name='producer %d' % (i + 1,), inQ=inQ, outQ=outQ)
        p.start()
        producerList.append(p)

    conn = sqlite3.connect('/mnt/hgfs/Share/phonesqlite.db')
    print('Open database successfully')
    cursor = conn.cursor()

    cursor.execute('select count(*) from "T_PhoneLocation";')
    #print("Total: " % (cursor[0][0],))
    values = cursor.fetchall()
    print('Total DB Rows: ', values[0][0])

    file = open('/mnt/hgfs/Share/log-%d.csv' % (time.time(),), 'w')
    file.write('type,number,excel,db\n')

    data = xlrd.open_workbook('phonelocation.xlsx')
    #data = xlrd.open_workbook('/mnt/hgfs/Share/test.xlsx')
    table = data.sheets()[0]
    print('Total Excel Rows: ', table.nrows)

    for row in range(table.nrows):
    #for row in range(1):
        strNumber = table.cell(row, 0).value
        strInfos = table.cell(row, 1).value.replace('★', '#').strip()

        strSql = 'select province, city, isp from "T_PhoneLocation" where phone = "%s";' % (strNumber)
        cursor.execute(strSql)
        values = cursor.fetchall()

        qData = [strNumber, strInfos, values]

        inQ.put(qData)

        '''
        if len(values) != 0:
            strDBInfos = "%s#%s#%s" % (values[0][0].strip(), values[0][1].strip(), values[0][2].strip())
            if strDBInfos != strInfos:
                #file.write(strNumber + ',' + strInfos + ',' + strDBInfos + '\n')
                updateRecord(cursor, strNumber, strInfos, file)
        else:
            #file.write(strNumber + ',' + strInfos + ',\n')
            insertRecord(cursor, strNumber, strInfos, file)
        '''


    while True:
        if inQ.empty():
            with lock:
                bRunning = False
                break

        if outQ.empty():
            continue

        ret = outQ.get()

        if not ret[0]:
            #print(ret[1])
            file.write(ret[1])
        else:
            #print(ret[1])
            cursor.execute(ret[1])


    while not outQ.empty():
        ret = outQ.get()

        if not ret[0]:
            #print(ret[1])
            file.write(ret[1])
        else:
            #print(ret[1])
            cursor.execute(ret[1])


    for producer in producerList:
        producer.join()

    file.close()
    conn.commit()
    conn.close()
    print('Run time: %fs' % (time.time() - startTime))
