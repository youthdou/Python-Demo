import requests
import html5lib
import re
from bs4 import BeautifulSoup


s = requests.Session()
url_login = 'https://accounts.douban.com/login'


formdata = {
    'source':'index_nav',
    'form_email': 'username',
    'form_password': 'password',
    'login': u'登录'
}
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

r = s.post(url_login, data = formdata, headers = headers)
content = r.text
soup = BeautifulSoup(content, 'html5lib')
captcha = soup.find('img', id = 'captcha_image')
if captcha:
    captcha_url = captcha['src']
    re_captcha_id = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
    captcha_id = re.findall(re_captcha_id, content)
    print(captcha_id)
    print(captcha_url)
    captcha_text = input('Please input the captcha:')
    formdata['captcha-solution'] = captcha_text
    formdata['captcha-id'] = captcha_id
    r = s.post(url_login, data = formdata, headers = headers)

r = s.get('https://www.douban.com/')
#print(r.text)
soup = BeautifulSoup(r.text, 'html5lib')
print(soup.find('a', {'class':'bn-more'}).span.getText())
print(soup.find('div', {'id':'friend'}).h2)

