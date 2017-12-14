#from scrapy.conf import settings
import company_list_pro.settings

class Cookie:
    def __init__(self, strCookies):
        self.strCookies = strCookies
        self.cookies = {}
        self.parse()

    def parse(self):
        for strCookie in self.strCookies.split(';'):
            name, value = strCookie.strip().split('=', 1)
            self.cookies[name] = value

    def get(self):
        return self.cookies


if __name__ == '__main__':
    cookies = Cookie(settings['COOKIES'])
    print(cookies.get())