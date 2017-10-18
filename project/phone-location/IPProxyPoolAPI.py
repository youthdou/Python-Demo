#https://github.com/qiyeboy/IPProxyPool

import requests
import json
import random
import csv
import time

def getProxies():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=10&country=国内')
    ip_ports = json.loads(r.text)
    #print(ip_ports)
    #ip = ip_ports[0][0]
    #port = ip_ports[0][1]
    ip_port = random.choice(ip_ports)
    ip = ip_port[0]
    port = ip_port[1]
    proxies = {
        'http':'http://%s:%s'%(ip,port),
        'https':'http://%s:%s'%(ip,port)
    }
    return proxies

#r = requests.get('http://ip.chinaz.com/',proxies=proxies)
#r = requests.get('http://icanhazip.com', proxies=proxies)
#r.encoding='utf-8'
#print(r.text)

if __name__ == '__main__':
    iCount = 0
    with open('/mnt/hgfs/Share/log.csv', 'r') as f:
        reader = csv.reader(f)
        #for i in range(40):
        for row in reader:
            proxies = getProxies()
            print(proxies)
            iCount += 1

            if iCount > 200:
                break

            try:
                if len(proxies) == 0:
                    print('Empty: ', iCount)
                    continue

                url = ('http://v.showji.com/Locating/showji.com2016234999234.aspx?'
                       'm=%s&output=json&callback=querycallback&timestamp=%d') % (row[1], time.time())
                r = requests.get(url, proxies=proxies, timeout=1)
                if r.text.startswith('querycallback(') == False:
                    print("Failed: ", iCount)
                    continue
                print(r.text)


                '''
                r = requests.get('http://icanhazip.com', proxies=proxies, timeout = 1)
                print(r.text)
                '''

            except Exception as e:
                print("Failed: ", iCount)
                pass