#http://www.cnblogs.com/lhj588/archive/2012/01/06/2314181.html

import xlrd

data = xlrd.open_workbook('phonelocation.xlsx')
table = data.sheets()[0]
print('%d:%d' % (table.nrows, table.ncols))
print('%s' % (table.cell(0, 0).value,))
for strValue in table.cell(0, 1).value.split('★'):
    print(',' , strValue)