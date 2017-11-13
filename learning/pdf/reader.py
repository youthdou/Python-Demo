import requests
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

import os
import sys

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

r = requests.get('http://pythonscraping.com/pages/warandpeace/chapter1.pdf')

with open('./test.pdf', 'wb') as f:
    f.write(r.content)
    f.close()

if not os.path.exists('./test.pdf'):
    sys.exit(0)

pdfFile = open('./test.pdf', 'rb')
outputString = readPDF(pdfFile)
print(outputString)
pdfFile.close()
