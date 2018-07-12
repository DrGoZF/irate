from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from os import listdir
from os.path import isfile, join
import wave

dataPath = "/Users/aaa/Documents/python/wav/Singapore/demo2"
files = [join(dataPath, f) for f in listdir(dataPath) if isfile(join(dataPath, f))]
print files

data = []
outfile = join(dataPath, "demo.wav")
for f in files:
    if f[-3:] == "wav":
    	w = wave.open(f, 'rb')
    	data.append( [w.getparams(), w.readframes(w.getnframes())] )
    	w.close()

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
for i in range(0,10):
    output.writeframes(data[i][1])
output.close()
