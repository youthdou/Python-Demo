import requests
from io import StringIO
import csv

data = requests.get('http://pythonscraping.com/files/MontyPythonAlbums.csv')
dataFile = StringIO(data.content.decode('utf-8'))

#csvReader = csv.reader(dataFile)
dictReader = csv.DictReader(dataFile)
print(dictReader.fieldnames)

#for row in csvReader:
for row in dictReader:
    print(row)

