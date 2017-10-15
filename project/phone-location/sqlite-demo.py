import sqlite3
import sys

if __name__ == '__main__':
    conn = sqlite3.connect('phonesqlite.db')
    print('Open database successfully')
    cursor = conn.cursor()

    if len(sys.argv) >= 2:
        strNumber = sys.argv[1]
        #strSql = 'select province, city, isp from "T_PhoneLocation" where phone = "%s";' % (strNumber)
        cursor.execute('select province, city, isp from "T_PhoneLocation" where phone = ?;', (strNumber,))
        values = cursor.fetchall()

        if len(values) > 0:
            print(strNumber, ':', values[0])
        else:
            print(strNumber, ':', 'None')

    conn.close()