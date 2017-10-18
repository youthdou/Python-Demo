#http://www.jianshu.com/p/ebf2e5b34aad

import requests
from bs4 import BeautifulSoup

'''
proxies = {"http": "http://144.255.219.39:8118", "https": "https://120.78.15.63:80"}
r = requests.get("http://example.org", proxies=proxies)
#r = requests.get("http://example.org")
#print(r.content)
print(r.text)
'''

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy()
    print("proxy: %s" % (proxy))
    while retry_count > 0:
        try:
            html = requests.get('https://www.example.com', proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None

#getHtml()
#getHtml()

if __name__ == '__main__':
    for i in range(40):
        proxy = get_proxy()
        try:
            if len(proxy) == 0:
                print('Empty: ', i)
                continue
            proxies = {"http": "http://{}".format(proxy)}
            print(proxies)
            r = requests.get('http://icanhazip.com',
                             proxies=proxies, timeout=1)
            print(r.text)
        except Exception as e:
            delete_proxy(proxy)
            print("Failed: ", i)
            pass
