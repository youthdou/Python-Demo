import threading
import queue
import random
import time
import multiprocessing

bRunning = True

lock = threading.Lock()

class Producer(threading.Thread):
    def __init__(self, name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=name)

    def run(self):
        for i in range(10):
            num = random.randint(1, 99)
            self.queue.put(num)
            print("[%s]producing %d" % (threading.current_thread().name, num))
            time.sleep(random.random())
        global lock
        global bRunning
        with lock:
            bRunning = False



class Consumer(threading.Thread):
    def __init__(self, name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            global lock
            global bRunning
            with lock:
                if not bRunning:
                    break
            if self.queue.empty():
                continue
            val = self.queue.get()
            print("[%s]Consume %d" % (threading.current_thread().name, val))


if __name__ == '__main__':
    print("Max core: %d" % (multiprocessing.cpu_count()))
    q = queue.Queue()
    p = Producer(name='producer', queue=q)
    c = Consumer(name='consumer', queue=q)

    p.start()
    c.start()

    p.join()
    c.join()