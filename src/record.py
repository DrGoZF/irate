# 从麦克风中获取音频数据，并分成5秒一段的样本，加入queue

import pyaudio
import wave

# 音频设置
CHUNK = 2
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
WAVE_OUTPUT_FILENAME = "output{0}.wav"

def record_data(threadName, q, record_seconds, parts, queueLock):
    # 开始音频流
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    # 截取5秒一段的文件，并保存成wav文件
    frame0 = []
    frame1 = []
    frame2 = []
    frame3 = []
    frame4 = []
    for parts in range(0, parts):
        for i in range(0, record_seconds):
            sec = parts * 5 + i
            #print sec
            for j in range(0, int(RATE / CHUNK)):
                data = stream.read(CHUNK, exception_on_overflow = False)
                frame0.append(data)
                if sec >= 1:
                    frame1.append(data)
                if sec >= 2:
                    frame2.append(data)
                if sec >= 3:
                    frame3.append(data)
                if sec >= 4:
                    frame4.append(data)

            if sec >= 5:
                fileName = WAVE_OUTPUT_FILENAME.format(str(sec - 5))
                wf = wave.open(fileName, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                if sec % 5 == 0:
                    wf.writeframes(b''.join(frame0))
                    frame0 = []
                    #print "writing frame0 to ", fileName
                if sec % 5 == 1:
                    wf.writeframes(b''.join(frame1))
                    frame1 = []
                    #print "writing frame1 to ", fileName
                if sec % 5 == 2:
                    wf.writeframes(b''.join(frame2))
                    frame2 = []
                    #print "writing frame2 to ", fileName
                if sec % 5 == 3:
                    wf.writeframes(b''.join(frame3))
                    frame3 = []
                    #print "writing frame3 to ", fileName
                if sec % 5 == 4:
                    wf.writeframes(b''.join(frame4))
                    frame4 = []
                    #print "writing frame4 to ", fileName
                wf.close()

                queueLock.acquire()
                q.put(fileName)
                queueLock.release()

    print("* done recording")

    # 关闭音频流
    stream.stop_stream()
    stream.close()
    p.terminate()
