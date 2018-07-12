from pyAudioAnalysis import audioTrainTest as aT
import nn

model = "svn"
modelName = "emotionModelData1SVN"

aT.featureAndTrain(["/Users/aaa/Documents/python/wav/labels/angry",
                    "/Users/aaa/Documents/python/wav/labels/neutral"], 
                    1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, 
                    model, modelName, False)

#nn.trainNN(["/Users/aaa/Documents/python/wav/labels/angry",
#       "/Users/aaa/Documents/python/wav/labels/neutral"], 
#       1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, False)

import os
from os import listdir
from os.path import isfile, join

dataPath = "/Users/aaa/Documents/python/wav/labels/test/"
files = [join(dataPath, f) for f in listdir(dataPath) if isfile(join(dataPath, f))]
print f

yTrue = []
yPred = []

for f in files:
  print "processing ", f
  if f[-3:] == "wav":
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

from sklearn.metrics import accuracy_score, recall_score, f1_score

print accuracy_score(yTrue, yPred)
print recall_score(yTrue, yPred, labels=None, pos_label=1, average='macro', sample_weight=None)
print f1_score(yTrue, yPred, labels=None, pos_label=1, average='macro', sample_weight=None)
