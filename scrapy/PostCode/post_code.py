import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import multiprocessing
import threading
from xml.parsers.expat import ParserCreate


class DefaultSaxHandler(object):
    def __init__(self, provinces):
        self.provinces = provinces


    def start_element(self, name, attrs):
        if name != 'map':
            name = attrs['title']
            number = attrs['href']
            self.provinces.append((name, number))

    def end_element(self, name):
        pass

    def char_data(self, text):
        pass

def get_province_entry(url):
    content = requests.get(url).content.decode('gb2312')
    #print(content)
    start = content.find('<map name=\"map_86\" id=\"map_86\">')
    end = content.find('</map>')
    content = content[start:end + len('</map>')].strip()
    provinces = []
    handler = DefaultSaxHandler(provinces)

    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data

    parser.Parse(content)

    return provinces

def get_city_code(listCities):
    print("[%s]Running" % threading.current_thread().name)
    for cityInfo in listCities:
        cityUrl = "http://www.ip138.com" + cityInfo[1]
        #print(cityUrl)
        r = requests.get(cityUrl)
        bsObj = BeautifulSoup(r.content.decode('gbk'), 'html5lib')
        table = bsObj.find('table', {'class': 't12'})
        print(table)

        print('City:%s' %(cityInfo[0]))
        for tr in table.findAll('tr')[1:]:
            iCol = 0
            list1 = []
            list2 = []
            for td in tr.findAll('td'):
                strText = td.getText()
                strText = strText.strip()
                if iCol < 3:
                    if len(strText) > 0:
                        list1.append(strText)
                else:
                    if len(strText) > 0:
                        list2.append(strText)
                iCol = iCol + 1

            if len(list1) > 2:
                print(list1)
            if len(list2) > 2:
                print(list2)




if __name__ == "__main__":
    provinces = get_province_entry('http://www.ip138.com/post')
    print(provinces)
    iThreadCount = multiprocessing.cpu_count()
    iStep = int(len(provinces) / iThreadCount + 1)
    ThreadPool = []

    for i in range(iThreadCount):
        iCount = iStep
        if (i + 1) * iStep > len(provinces):
            iCount = len(provinces) - i * iStep
        listCities = provinces[(i * iStep):(i * iStep + iCount)]
        print(listCities)
        ThreadPool.append(threading.Thread(target=get_city_code, args=(listCities,)))

    for thread in ThreadPool:
        thread.start()

    for thread in ThreadPool:
        thread.join()