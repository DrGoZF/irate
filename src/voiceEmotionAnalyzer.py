# 模型的训练过程
from pyAudioAnalysis import audioTrainTest as aT
import nn

# 模型的名称和文件名
model = "svn"
modelName = "emotionModelData1SVN"

# 直接调用pyAudioAnalysis的包
# https://github.com/tyiannak/pyAudioAnalysis/wiki/4.-Classification-and-Regression
aT.featureAndTrain(["/Users/aaa/Documents/python/wav/labels/angry",
                    "/Users/aaa/Documents/python/wav/labels/neutral"], 
                    1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, 
                    model, modelName, False)

# 训练神经网络模型的调用方法
#nn.trainNN(["/Users/aaa/Documents/python/wav/labels/angry",
#       "/Users/aaa/Documents/python/wav/labels/neutral"], 
#       1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, False)

# 验证模型的准确率、召回率等
import os
from os import listdir
from os.path import isfile, join

# 测试音频的地址（文件夹）
dataPath = "/Users/aaa/Documents/python/wav/labels/test/"
files = [join(dataPath, f) for f in listdir(dataPath) if isfile(join(dataPath, f))]
print f

yTrue = []
yPred = []

for f in files:
  print "processing ", f
  if f[-3:] == "wav":
    # 对测试音频进行分类，输出概率最大的标签
    result = aT.fileClassification(f, modelName, model)
    #result = nn.classifyNN(f, modelName)
    
    pro = result[1]
    label = result[2]
    max = 0
    maxLabel = 0
    for i in range(0,2):
      if (pro[i] > max):
        max = pro[i]
        maxLabel = i
    print pro
    print label
    print label[maxLabel]

    # 将模型输出的标签和测试音频实际的标签比较
    # yTrue为实际的标签list；yPred为预测的标签list
    result = f[44:][:5]

    if result == "angry":
	yTrue.append(1)
    else:
	yTrue.append(0)

    if label[maxLabel] == "angry":
	yPred.append(1)
    else:
	yPred.append(0)

  else:
    print "skipping ", f

# 输出模型的accuracy, recall和f1
from sklearn.metrics import accuracy_score, recall_score, f1_score

print accuracy_score(yTrue, yPred)
print recall_score(yTrue, yPred, labels=None, pos_label=1, average='macro', sample_weight=None)
print f1_score(yTrue, yPred, labels=None, pos_label=1, average='macro', sample_weight=None)
