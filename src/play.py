# 播放一段音频文件，并分段放入queue - demo使用

import pyaudio  
import wave  
   
CHUNK = 2
WAVE_OUTPUT_FILENAME = "output{0}.wav"

def play_data(threadName, q, record_seconds, parts, queueLock, name):
    f = wave.open(name, "rb")
    p = pyaudio.PyAudio()
    FORMAT = p.get_format_from_width(f.getsampwidth())
    CHANNELS = f.getnchannels()
    RATE = f.getframerate()
    stream = p.open(format = FORMAT,  
                    channels = CHANNELS,  
                    rate = RATE,
                    output = True)

    for part in range(0, parts):
        frames = []
        for i in range(0, int(RATE / CHUNK * record_seconds)):
            data = f.readframes(CHUNK)
            stream.write(data)
            frames.append(data)

        fileName = WAVE_OUTPUT_FILENAME.format(str(part))
        print "writting to file: ", fileName
        wf = wave.open(fileName, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        queueLock.acquire()
        q.put(fileName)
        queueLock.release() 

    stream.stop_stream()  
    stream.close()  

    p.terminate()
