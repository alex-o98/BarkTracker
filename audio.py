import pyaudio
import wave
import time
import numpy as np
from datetime import datetime
from notify_run import Notify
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
TIME_LIMIT = 60
THRESHOLD = 100
notify = Notify()
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []
start = time.time()
record = 0
start_record = None

while(True):
    data = stream.read(CHUNK)
    samples = np.fromstring(data, dtype = np.int16)



    if  record==1:
        frames.append(data)
        if time.time()-start_record>TIME_LIMIT:
            name = datetime.utcfromtimestamp(start_record).strftime('%Y-%m-%d_%H-%M-%S')
            file = wave.open(name+".wav", 'wb')
            file.setnchannels(CHANNELS)
            file.setsampwidth(p.get_sample_size(FORMAT))
            file.setframerate(RATE)
            file.writeframes(b''.join(frames))
            file.close()
            print("file saved",name)
            start = time.time()
            record = 0
            start_record = 0
            frames=[]

    if max(samples) > THRESHOLD:
		
        if time.time()-start > TIME_LIMIT:#

            # start recording for `THREHSOLD` seconds
            start_record=time.time()
            start = time.time()
            record = 1

            found_at = datetime.utcfromtimestamp(start_record).strftime('%H:%M:%S')
            print("Loud noise "+str(max(samples))+" found today at "+found_at)
            notify.send("Loud noise "+str(max(samples))+" found today at "+found_at)