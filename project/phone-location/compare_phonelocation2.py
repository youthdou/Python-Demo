#https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432010494717e1db78cd172e4d52b853e7fd38d6985c000

#Exception:
#http://www.cnblogs.com/klchang/p/4635040.html

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

import csv
import os
import shutil
#import ProxyPool
import IPProxyPoolAPI

import traceback

bRunning = True

iMaxCnt = 0

lock = threading.Lock()



def queryNumberV2(strNumber):
    result = {}
    result['QueryResult'] = 'False'

    iIndex = 0
    with lock:
        global iMaxCnt
        iMaxCnt = iMaxCnt + 1
        iIndex = iMaxCnt
    proxies = IPProxyPoolAPI.getProxies()
    url = 'http://www.ip138.com:8080/search.asp?action=mobile&mobile=%s' % (strNumber)

    try:
        r = requests.get(url, proxies=proxies, timeout=1)
        content = r.content.decode('gb2312')
        bsObj = BeautifulSoup(content, 'html5lib')
        listInfos = bsObj.find_all('td', {'class':'tdc2'})

        if len(listInfos) != 5:
            print('[%s][%d]%s' % (threading.current_thread().name, iIndex, url))
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
        print('[%s][%d]Successful!' % (threading.current_thread().name, iIndex))
    except Exception as e:
        print(e)
        #print(traceback.format_exc())
        print('[%s][%d]%s' % (threading.current_thread().name, iIndex, url))
    finally:
        #print(result)
        return result


def queryNumber(strNumber):
    result = {}
    result['QueryResult'] = 'False'


    iIndex = 0
    with lock:
        global iMaxCnt
        iMaxCnt = iMaxCnt + 1
        iIndex = iMaxCnt

        '''
        if iMaxCnt > 500:
            return result
        '''

        '''
        else:
            strMsg = '[%s:%d]' % (threading.current_thread().name, iMaxCnt)
            print(strMsg)
        '''

    #time.sleep(2)
    headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')}

    url = ('http://v.showji.com/Locating/showji.com2016234999234.aspx?'
           'm=%s&output=json&callback=querycallback&timestamp=%d') % (strNumber, time.time())


    #url = 'http://v.showji.com/Locating/showji.com2016234999234.aspx?m=1701552&output=json&callback=querycallback&timestamp=1508289534'

    '''
    proxies = {}
    with lock:
        #proxies = ProxyPool.getProxy()
        proxies = IPProxyPoolAPI.getProxies()
    '''

    proxies = IPProxyPoolAPI.getProxies()
    try:
        #print(threading.current_thread().name, ':', proxies)
        r = requests.get(url, proxies=proxies, timeout=1)
        if r.text.strip().startswith('querycallback('):
            print('[%s][%d]Successful!' % (threading.current_thread().name, iIndex))
            result = eval(r.text.lstrip('querycallback(').rstrip(');'))
        else:
            print('[%s][%d]%s' % (threading.current_thread().name, iIndex, r.url))
    except Exception as e:
        print(e)
        print('[%s][%d]%s' % (threading.current_thread().name, iIndex, url))
    finally:
        return result

    '''
    
    r = requests.get(url, headers=headers)
    if r.text.strip().startswith('querycallback('):
        result = eval(r.text.lstrip('querycallback(').rstrip(');'))
    else:
        print('[%s][%d]%s' % (threading.current_thread().name, iIndex, r.url))
        time.sleep(10)

    return result
    
    '''

    '''
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            r = requests.get(url, proxies={"http": "http://{}".format(proxy)})
            #print(r.url)
            #print(r.text)
            #print(r.status_code)

            if r.text.strip().startswith('querycallback('):
                result = eval(r.text.lstrip('querycallback(').rstrip(');'))
            else:
                print('[%s][%d]%s' % (threading.current_thread().name, iIndex, r.url))
            #return queryNumberV2(strNumber)
            #for key in result:
            #    print('%s:%s' % (key, result[key]))
            return result
        except Exception:
            retry_count -= 1

    delete_proxy(proxy)
    print('[%s][%d]%s' % (threading.current_thread().name, iIndex, url))
    return result
    '''


def record2String(record):
    str = ''
    for field in record[1:]:
        str += field + '#'

    str.rstrip('#')

    return str


def detail2String(detail):
    if detail.get('QueryResult') == 'False':
        return ''

    str = detail.get('Province') + '#'
    str += detail.get('City') + '#'
    str += detail.get('TO') + '#'
    str += detail.get('AreaCode') + '#'
    str += detail.get('PostCode')

    return str

#phone, province, city, isp, code, zip
#{"Mobile":"1701552","QueryResult":"True","TO":"中国电信","Corp":"中国电信","Province":"安徽","City":"合肥","AreaCode":"0551","PostCode":"230000","VNO":"","Card":""}

def checkRecord(record):
    strNumber = record[0]
    detail = queryNumberV2(strNumber)
    strRecord = record2String(record)
    strDetail = detail2String(detail)
    strRet = strNumber + ',' + strRecord + ',' + strDetail + '\n'
    if detail.get('QueryResult', 'False') == 'False':
        #file.write(strNumber + ',' + strInfos + ',\n')
        return (False, strRet)

    #print(strInfos)
    if record[1] != detail.get('Province', '').strip():
        return (False, strRet)
    if record[2] != detail.get('City', '').strip():
        return (False, strRet)
    if record[3] != detail.get('TO', '').strip():
        return (False, strRet)
    if record[4] != detail.get('AreaCode').strip():
        return (False, strRet)
    if record[5] != detail.get('PostCode').strip():
        return (False, strRet)

    return (True, strRet)




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

            for record in qData:
                self.outQ.put(checkRecord(record))

def savAsCommonFile(strLogFile):
    strCommoneFile = '/mnt/hgfs/Share/log.csv'

    if os.path.exists(strCommoneFile):
        os.remove(strCommoneFile)

    shutil.copy(strLogFile, strCommoneFile)

def processResult(ret, file):
    #print(ret[1])
    if not ret[0]:
        # print(ret[1])
        file.write(ret[1])

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
    values = cursor.fetchall()
    iTotalCount = values[0][0]
    print('Total DB Rows: ', iTotalCount)

    strLogFileName = '/mnt/hgfs/Share/log-%d.csv' % (time.time(),)
    file = open(strLogFileName, 'w')
    file.write('number,db,network\n')

    #data = xlrd.open_workbook('/mnt/hgfs/Share/phonelocation.xlsx')
    #data = xlrd.open_workbook('/mnt/hgfs/Share/test.xlsx')
    #table = data.sheets()[0]
    #print('Total Excel Rows: ', table.nrows)

    #for row in range(table.nrows):
    #for row in range(1):
        #strNumber = table.cell(row, 0).value
        #strInfos = table.cell(row, 1).value.replace('★', '#').strip()

    iOffset = 0
    while True:
        #if iOffset >= 200:
        #    break;
        if iOffset >= iTotalCount:
            break
        if (iTotalCount - iOffset) > 10000:
            iLimit = 10000
        else:
            iLimit = iTotalCount - iOffset

        cursor.execute('select phone, province, city, isp, code, zip from "T_PhoneLocation" limit ? offset ?;', (iLimit, iOffset))
        values = cursor.fetchall()
        inQ.put(values)

        iOffset += iLimit

    while True:
        if inQ.empty():
            time.sleep(5)
            with lock:
                if iMaxCnt >= iTotalCount:
                    bRunning = False
                    break
        if outQ.empty():
            time.sleep(5)
            continue

        ret = outQ.get()
        processResult(ret, file)

    while not outQ.empty():
        #print("Size of OutQ: %d" % (outQ.qsize(),))
        ret = outQ.get()
        processResult(ret, file)

    for producer in producerList:
        producer.join()

    file.close()
    conn.commit()
    conn.close()

    savAsCommonFile(strLogFileName)

    print('Run time: %fs' % (time.time() - startTime))
