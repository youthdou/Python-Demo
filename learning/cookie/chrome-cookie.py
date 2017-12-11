#http://blog.csdn.net/chennudt/article/details/76726580

#http://www.jianshu.com/p/cd2117b931e3

import os
import sqlite3
import requests
import datetime
from win32.win32crypt import CryptUnprotectData

GMT_FORMAT = '%a, %d-%b-%Y %H:%M:%S GMT'

def getExpires(iTimeStamp):
    iTimeStamp = iTimeStamp / 1000000.0
    iTimeStamp -= 11644473600
    dt = datetime.datetime.fromtimestamp(iTimeStamp)
    #print(dt.strftime(GMT_FORMAT))
    return dt.strftime(GMT_FORMAT)

def getcookiefromchrome(host='.oschina.net'):
    f = open("cookies.dat", 'w')
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql="select host_key,name,encrypted_value,path,expires_utc from cookies where host_key like '%%%s%%'" % host
    print(sql)
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()
        #cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        for host_key, name, encrypted_value, path, expires_utc in cu.execute(sql).fetchall():
            #print(CryptUnprotectData(encrypted_value)[1].decode())
            strValue = CryptUnprotectData(encrypted_value)[1].decode()
            #acw_tc
            if expires_utc == 0:
                continue

            strCookie = "%s=%s; expires=%s; domain=%s; path=%s\n" % (name, strValue, getExpires(expires_utc), host_key, path)
            f.write(strCookie)
            print(strCookie)
        #print(cookies)
        #return cookies
    f.close()

getcookiefromchrome('.qichacha.com')