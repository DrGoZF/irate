import numpy as np
import cPickle
import os
import numpy
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from pyAudioAnalysis import audioFeatureExtraction as aF
from pyAudioAnalysis import audioTrainTest as aT
from pyAudioAnalysis import audioBasicIO

modelName = "emotionModelData1NNO"

def train(featuresNew, param):
	[X, Y] = aT.listOfFeatures2Matrix(featuresNew)
	clf = MLPClassifier(solver = 'lbfgs', alpha = 1e-5, hidden_layer_sizes = (5,param), random_state = 1)
	clf.fit(X, Y)
	return clf

def trainNN(listOfDirs, mtWin, mtStep, stWin, stStep, computeBEAT=False):
	#Feature Extraction
	[features, classNames, _] = aF.dirsWavFeatureExtraction(listOfDirs, mtWin, mtStep, stWin, stStep, computeBEAT=computeBEAT)

	if len(features) == 0:
		print "feature ERROR"
		return

	numOfFeatures = features[0].shape[1]
	featureNames = ["features" + str(d + 1) for d in range(numOfFeatures)]
	aT.writeTrainDataToARFF(modelName, features, classNames, featureNames)
	for i, f in enumerate(features):
		if len(f) == 0:
			print "feature ERROR"
			return

	C = len(classNames)
	[featuresNorm, MEAN, STD] = aT.normalizeFeatures(features)        # normalize features
	MEAN = MEAN.tolist()
	STD = STD.tolist()
	featuresNew = featuresNorm

	bestParam = evaluate(featuresNew, classNames, 100, numpy.array([1,2,3,4,5,6]), 0, perTrain=0.80)
	clf = train(featuresNew, bestParam)

	with open(modelName, 'wb') as fid:
		cPickle.dump(clf, fid)
	fo = open(modelName + "MEANS", "wb")
	cPickle.dump(MEAN, fo, protocol=cPickle.HIGHEST_PROTOCOL)
	cPickle.dump(STD, fo, protocol=cPickle.HIGHEST_PROTOCOL)
	cPickle.dump(classNames, fo, protocol=cPickle.HIGHEST_PROTOCOL)
	cPickle.dump(mtWin, fo, protocol=cPickle.HIGHEST_PROTOCOL)
	cPickle.dump(mtStep, fo, protocol=cPickle.HIGHEST_PROTOCOL)
	cPickle.dump(stWin, fo, protocol=cPickle.HIGHEST_PROTOCOL)
	cPickle.dump(stStep, fo, protocol=cPickle.HIGHEST_PROTOCOL)
	cPickle.dump(computeBEAT, fo, protocol=cPickle.HIGHEST_PROTOCOL)
	fo.close()

def evaluate(features, ClassNames, nExp, Params, parameterMode, perTrain=0.80):
	(featuresNorm, MEAN, STD) = aT.normalizeFeatures(features)
	nClasses = len(features)
	CAll = []
	acAll = []
	F1All = []
	PrecisionClassesAll = []
	RecallClassesAll = []
	ClassesAll = []
	F1ClassesAll = []
	CMsAll = []

    # compute total number of samples:
	nSamplesTotal = 0
	for f in features:
		nSamplesTotal += f.shape[0]
	if nSamplesTotal > 1000 and nExp > 50:
		nExp = 50
		print "Number of training experiments changed to 50 due to high number of samples"
	if nSamplesTotal > 2000 and nExp > 10:
		nExp = 10
		print "Number of training experiments changed to 10 due to high number of samples"

	for Ci, C in enumerate(Params):                # for each param value
		CM = numpy.zeros((nClasses, nClasses))
		for e in range(nExp):              # for each cross-validation iteration:
			print "Param = {0:.5f} - Classifier Evaluation Experiment {1:d} of {2:d}".format(C, e+1, nExp)
			featuresTrain, featuresTest = aT.randSplitFeatures(featuresNorm, perTrain)
			Classifier = train(featuresTrain, C)

			CMt = numpy.zeros((nClasses, nClasses))
			for c1 in range(nClasses):
				nTestSamples = len(featuresTest[c1])
				Results = numpy.zeros((nTestSamples, 1))
				for ss in range(nTestSamples):
					[Results[ss], _] = classify(Classifier, featuresTest[c1][ss])
				for c2 in range(nClasses):
					CMt[c1][c2] = float(len(numpy.nonzero(Results == c2)[0]))
			CM = CM + CMt
		CM = CM + 0.0000000010
		Rec = numpy.zeros((CM.shape[0], ))
		Pre = numpy.zeros((CM.shape[0], ))

		for ci in range(CM.shape[0]):
			Rec[ci] = CM[ci, ci] / numpy.sum(CM[ci, :])
			Pre[ci] = CM[ci, ci] / numpy.sum(CM[:, ci])
		PrecisionClassesAll.append(Pre)
		RecallClassesAll.append(Rec)
		F1 = 2 * Rec * Pre / (Rec + Pre)
		F1ClassesAll.append(F1)
		acAll.append(numpy.sum(numpy.diagonal(CM)) / numpy.sum(CM))

		CMsAll.append(CM)
		F1All.append(numpy.mean(F1))

	print ("\t\t"),
	for i, c in enumerate(ClassNames):
		if i == len(ClassNames)-1:
			print "{0:s}\t\t".format(c),
		else:
			print "{0:s}\t\t\t".format(c),
	print ("OVERALL")
	print ("\tC"),
	for c in ClassNames:
		print "\tPRE\tREC\tF1",
	print "\t{0:s}\t{1:s}".format("ACC", "F1")
	bestAcInd = numpy.argmax(acAll)
	bestF1Ind = numpy.argmax(F1All)
	for i in range(len(PrecisionClassesAll)):
		print "\t{0:.3f}".format(Params[i]),
		for c in range(len(PrecisionClassesAll[i])):
			print "\t{0:.1f}\t{1:.1f}\t{2:.1f}".format(100.0 * PrecisionClassesAll[i][c], 100.0 * RecallClassesAll[i][c], 100.0 * F1ClassesAll[i][c]),
		print "\t{0:.1f}\t{1:.1f}".format(100.0 * acAll[i], 100.0 * F1All[i]),
		if i == bestF1Ind:
			print "\t best F1",
		if i == bestAcInd:
			print "\t best Acc",
		print
	return Params[bestF1Ind]

def classifyNN(inputFile, modelName):

	[Classifier, MEAN, STD, classNames, mtWin, mtStep, stWin, stStep, computeBEAT] = loadModel(modelName)
	[Fs, x] = audioBasicIO.readAudioFile(inputFile)
	x = audioBasicIO.stereo2mono(x)

	if isinstance(x, int):
		return (-1, -1, -1)
	if x.shape[0] / float(Fs) <= mtWin:
		return (-1, -1, -1)

	[MidTermFeatures, s] = aF.mtFeatureExtraction(x, Fs, mtWin * Fs, mtStep * Fs, round(Fs * stWin), round(Fs * stStep))
	MidTermFeatures = MidTermFeatures.mean(axis=1)        # long term averaging of mid-term statistics
	if computeBEAT:
		[beat, beatConf] = aF.beatExtraction(s, stStep)
		MidTermFeatures = numpy.append(MidTermFeatures, beat)
		MidTermFeatures = numpy.append(MidTermFeatures, beatConf)
	curFV = (MidTermFeatures - MEAN) / STD                # normalization

	[Result, P] = classify(Classifier, curFV)
	return Result, P, classNames

def classify(Classifier, testSample):
	Result = Classifier.predict(testSample.reshape(1,-1))[0]   # classification        
	P = Classifier.predict_proba(testSample.reshape(1,-1))[0]
	return [Result, P]

def loadModel(modelName):
	try:
		fo = open(modelName + "MEANS", "rb")
	except IOError:
		print "Load Model: Didn't find file"
		return
    
	try:
		MEAN = cPickle.load(fo)
		STD = cPickle.load(fo)
		classNames = cPickle.load(fo)
		mtWin = cPickle.load(fo)
		mtStep = cPickle.load(fo)
		stWin = cPickle.load(fo)
		stStep = cPickle.load(fo)
		computeBEAT = cPickle.load(fo)

	except:
		fo.close()
	fo.close()

	MEAN = numpy.array(MEAN)
	STD = numpy.array(STD)

	COEFF = []
	with open(modelName, 'rb') as fid:
		RF = cPickle.load(fid)    

	return(RF, MEAN, STD, classNames, mtWin, mtStep, stWin, stStep, computeBEAT)