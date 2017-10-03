import requests
from bs4 import BeautifulSoup

from PIL import Image
from io import BytesIO


r = requests.get('http://d.hiphotos.baidu.com/image/pic/item/09fa513d269759eeb651cb7ab8fb43166d22df7a.jpg', stream = True)
print(r.status_code)
image = Image.open(BytesIO(r.content))
image.save('meinv.jpg')

'''

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

try:
    r = requests.get('http://www.meizitu.com/a/5553.html', headers = headers)
    print(r.status_code)
    soup = BeautifulSoup(r.text)

    for img in soup.find('div',{'id':'picture'}).p.findAll('img'):
        print(img['src'])
except Exception as e:
    print("Exception: %s" % e)


print(r.status_code)
soup = BeautifulSoup(r.text)

for img in soup.find('div',{'id':'picture'}).p.findAll('img'):
    print(img['src'])
    
'''