#ref:http://www.cnblogs.com/itogo/p/5635629.html
#ref:https://docs.python.org/3/library/queue.html

import queue

qFIFO = queue.Queue()

for i in range(5):
    qFIFO.put(i)

while not qFIFO.empty():
    print(qFIFO.get())