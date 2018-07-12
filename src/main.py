import Queue
import threading
import sys
import time
from translate import translate
from classification import process_data
from record import record_data
from play import play_data
#from plot import plot_data

class workThread(threading.Thread):
    def __init__(self, threadID, name, q, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q, MODEL, RECORD_SECONDS, PARTS, queueLock)
        print "Exiting " + self.name

class recordThread(threading.Thread):
    def __init__(self, threadID, name, q, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        record_data(self.name, self.q, RECORD_SECONDS, PARTS, queueLock)
        print "Exiting " + self.name

class playThread(threading.Thread):
    def __init__(self, threadID, name, q, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        play_data(self.name, self.q, RECORD_SECONDS, PARTS, queueLock, fileName)
        print "Exiting " + self.name

class plotThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        time.sleep(5)
        plot_data()
        print "Exiting " + self.name

mode = sys.argv[1]
fileName = sys.argv[2]
threadList = ["Thread-1", "Thread-2"]
queueLock = threading.Lock()
dataLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []

MODEL = "emotionModelData1SVM"
PARTS = 15
RECORD_SECONDS = 5

file = open("data.txt","w+")
file.close()

if mode == "play":
    thread1 = playThread(1, "Thread-1", workQueue, queueLock)
else:
    thread1 = recordThread(1, "Thread-1", workQueue, queueLock)
thread2 = workThread(2, "Thread-2", workQueue, queueLock)
#thread3 = plotThread(3, "Thread-3")

thread1.start()
thread2.start()
#thread3.start()
threads.append(thread1)
threads.append(thread2)
#threads.append(thread3)

for t in threads:
    t.join()
print "finished"
