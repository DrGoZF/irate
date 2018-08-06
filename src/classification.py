# 分类相关代码

from pyAudioAnalysis import audioTrainTest as aT
from translate import translate
import time

# 根据选择的模型输出分类结果
# data: 需要分类的音频片段
# model: 选择的分类模型
# return: 分类结果
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

# 获取音频片段并处理：如果queue中有数据，取出并判断类型；否则sleep一秒。
def process_data(threadName, q, model, record_seconds, parts, queueLock):
    for i in range(0, int(record_seconds * (parts + 1))):
        queueLock.acquire()
        if not q.empty():
            data = q.get()
            queueLock.release()
            pro = classify(data, model)
            file = open("data.txt","a")
            print pro
            file.write("%.2f" % (pro * 100))
            file.write(",")
            file.close()
            # 将音频转换为文字
            #translate(data)
        else:
            queueLock.release()
            time.sleep(1)
    print "finish processing"
