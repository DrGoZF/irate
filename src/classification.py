from pyAudioAnalysis import audioTrainTest as aT
from translate import translate
import time

def classify(data, model):
    result = aT.fileClassification(data, model, "svm")
    pro = result[1]
    label = result[2]
    max = 0
    maxLabel = 0
    for i in range(0,2):
        if (pro[i] > max):
            max = pro[i]
            maxLabel = i
    print label[maxLabel]
    return pro[0]

def process_data(threadName, q, model, record_seconds, parts, queueLock):
    for i in range(0, int(record_seconds * (parts + 1))):
        queueLock.acquire()
        if not q.empty():
            data = q.get()
            queueLock.release()
            #print "%s processing %s" % (threadName, data)
            pro = classify(data, model)
            file = open("data.txt","a")
            print pro
            file.write("%.2f" % (pro * 100))
            file.write(",")
            file.close()
            #translate(data)
        else:
            queueLock.release()
            time.sleep(1)
    print "finish processing"
