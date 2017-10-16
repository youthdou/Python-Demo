#http://www.cnblogs.com/feeland/p/4463682.html

import os
import shutil

strLogFile = '/mnt/hgfs/Share/log.csv'
strNewLogFile = '/mnt/hgfs/Share/log1.csv'

if os.path.exists(strLogFile):
    print('Exist file: %s.' % (strLogFile))
    if os.path.exists(strNewLogFile):
        os.remove(strNewLogFile)
    shutil.copyfile(strLogFile, strNewLogFile)
else:
    print('Not exist file.')

