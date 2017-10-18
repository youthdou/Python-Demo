#http://www.jianshu.com/p/ebf2e5b34aad
#https://segmentfault.com/q/1010000009677441

import requests
import os
from bs4 import BeautifulSoup
import random
import time

m_proxies = list()

m_strIPFile = '/mnt/hgfs/Share/proxy-ip.csv'

def collectIPs():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    fp = open(m_strIPFile, 'w')
    for i in range(2):
        url = 'http://www.xicidaili.com/nn/%d' % (i + 1,)
        s = requests.get(url,headers = headers)
        soup = BeautifulSoup(s.text, 'lxml')
        ips = soup.select('#ip_list tr')
        for i in ips:
            try:
                ipp = i.select('td')
                ip = ipp[1].text
                host = ipp[2].text
                fp.write(ip)
                fp.write(',')
                fp.write(host)
                fp.write('\n')
            except Exception as e :
                print ('no ip !')

    fp.close()

def checkIPs():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    #url = 'https://www.baidu.com'
    url = 'http://v.showji.com/Locating/showji.com2016234999234.aspx?m=1700529&output=json&callback=querycallback&timestamp=1507878395204'
    fp = open(m_strIPFile,'r')
    ips = fp.readlines()
    global m_proxies
    for p in ips:
        ip = p.strip('\n').split(',')
        proxy = 'http://' +  ip[0] + ':' + ip[1]
        proxies = {'http': proxy}

        try :
            startTime = time.time()
            s = requests.get(url, proxies = proxies, timeout=1)
            #print(s.text)
            if s.text.startswith('querycallback(') == False:
                continue

            #print(proxies)
            costTime = time.time() - startTime
            #print('[%f]%s' %(costTime, s.status_code))
            if costTime < 1.0:
                m_proxies.append(proxies)


        except Exception as e:
            pass
            #print(e)

def checkIPsAgain():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    url = 'http://v.showji.com/Locating/showji.com2016234999234.aspx?m=1700529&output=json&callback=querycallback&timestamp=1507878395204'

    proxy_list = m_proxies
    m_proxies.clear()
    for proxies in proxy_list:
        try:
            startTime = time.time()
            r = requests.get(url, proxies=proxies, timeout=1)
            # print(r.text)
            if r.text.startswith('querycallback(') == False:
                continue

            #print(proxies)
            costTime = time.time() - startTime
            # print('[%f]%s' %(costTime, r.status_code))
            if costTime < 1.0:
                m_proxies.append(proxies)


        except Exception as e:
            pass

def getProxy():
    if len(m_proxies) == 0:
        collectIPs()
        checkIPs()
        print(m_proxies)
        checkIPsAgain()
        print(m_proxies)
        print('Total Number: ', len(m_proxies))

    #print("Total IPs: %d" % (len(m_proxies), ))
    return random.choice(m_proxies)

def test():
    proxies = getProxy()
    print(proxies)
    p = requests.get('http://icanhazip.com', proxies=proxies)
    #p = requests.get('http://icanhazip.com')
    print(p.text)


if __name__ == '__main__':
    #print(getProxy())
    test()

    '''
    
    url = ('http://v.showji.com/Locating/showji.com2016234999234.aspx?'
           'm=1491467&output=json&callback=querycallback&timestamp=%d') % (time.time(), )
    i = 0
    iSuccess = 0
    iFailed = 0
    while i < 40:
        r = requests.get(url, proxies=getProxy())
        #r = requests.get(url)

        if r.text.strip().startswith('querycallback('):
            result = eval(r.text.lstrip('querycallback(').rstrip(');'))
            print('[%d]Successful' % (i,))
            iSuccess += 1
        else:
            time.sleep(10)
            print('[%d]Failed.' % (i,))
            iFailed += 1
        i += 1

    print('Success: %d, Failed: %d' % (iSuccess, iFailed))
    
    '''