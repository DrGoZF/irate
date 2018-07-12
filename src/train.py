from pyAudioAnalysis import audioTrainTest as aT
aT.featureAndTrain(["/Users/aaa/Documents/python/wav/labels/angry",
					"/Users/aaa/Documents/python/wav/labels/neutral"], 
					1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, 
					"svm", "emotionModelData1SVM", False)