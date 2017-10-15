import requests
from bs4 import BeautifulSoup

'''
from PIL import Image
from io import BytesIO


r = requests.get('http://d.hiphotos.baidu.com/image/pic/item/09fa513d269759eeb651cb7ab8fb43166d22df7a.jpg', stream = True)
print(r.status_code)
image = Image.open(BytesIO(r.content))
image.save('meinv.jpg')
'''



headers = {
            'host': 'www.meizitu.com',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': 'safedog-flow-item=; UM_distinctid=15eb2730b49297-083fa28ae61def-38694646-100200-15eb2730b4c48a; CNZZDATA30056528=cnzz_eid%3D1275941178-1506231149-http%253A%252F%252Fwww.meizitu.com%252F%26ntime%3D1507002568; bdshare_firstime=1506232437863',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://www.meizitu.com/'

           }

urlMeiZiTu = 'http://www.meizitu.com/'
#urlMeiZiTu = 'http://www.meizitu.com/a/5553.html'

try:
    #print(headers)
    r = requests.get(urlMeiZiTu)
    print(r.status_code)
    print(r.text)
    soup = BeautifulSoup(r.text, 'html5lib')

    for img in soup.find('div',{'id':'picture'}).p.findAll('img'):
        print(img['src'])
except Exception as e:
    print("Exception: %s" % e)

'''
print(r.status_code)
soup = BeautifulSoup(r.text)

for img in soup.find('div',{'id':'picture'}).p.findAll('img'):
    print(img['src'])
'''
