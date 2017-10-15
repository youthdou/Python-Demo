#http://blog.csdn.net/u011659379/article/details/48133121


import requests
from bs4 import BeautifulSoup
import html5lib


myCookie = '''ll="108169"; bid=JphbrrAvfys; _pk_id.100001.8cb4=578ae01b44893577.1506780794.2.1506783320.1506780920.; 
ps=y; ue="alisww@gmail.com"; dbcl2="52709063:CvqfKaYTxpY"; ck=fD59; __yadk_uid=gvSyNFd6hnmejxfCcbVsOOjLautq8NlS; 
push_noty_num=0; push_doumail_num=0; __utma=30149280.293933648.1506780923.1506780923.1506783323.2; __utmc=30149280; 
__utmz=30149280.1506780923.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=30149280.5270;
 _pk_ses.100001.8cb4=*; __utmb=30149280.2.10.1506783323; __utmt=1'''

'''
cookies = {}

for cookieItem in myCookie.split(';'):
    cookieItem = cookieItem.strip()
    print(cookieItem)
    listItems = cookieItem.split('=')
    cookies[listItems[0]] = cookieItem.lstrip(listItems[0]+'=')

print(cookies)
'''

cookies = {'cookie':'ll="108169"; bid=JphbrrAvfys; _pk_id.100001.8cb4=578ae01b44893577.1506780794.2.1506783320.1506780920.; ps=y; ue="alisww@gmail.com"; dbcl2="52709063:CvqfKaYTxpY"; ck=fD59; __yadk_uid=gvSyNFd6hnmejxfCcbVsOOjLautq8NlS; push_noty_num=0; push_doumail_num=0; __utma=30149280.293933648.1506780923.1506780923.1506783323.2; __utmc=30149280; __utmz=30149280.1506780923.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=30149280.5270; _pk_ses.100001.8cb4=*; __utmb=30149280.2.10.1506783323; __utmt=1'}

r = requests.get('https://www.douban.com/',cookies=cookies)
soup = BeautifulSoup(r.text, 'html5lib')
print(soup.find('a', {'class':'bn-more'}).span.getText())
print(soup.find('div', {'id':'friend'}).h2)