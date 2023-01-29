from gtts import gTTS
import playsound

import pyaudio
#import aifc
import wave

print("play sound")
#file = "./input/notas/do.aiff"
file = "./input/notas/A4.mp3"
#playsound.playsound("./input/notas/A4.mp3")

wf = wave.open(file, 'rb')
p = pyaudio.PyAudio()
chunk=1024

# open stream based on the wave object which has been input.
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# read data (based on the chunk size)
data = wf.readframes(chunk)

# read data (based on the chunk size)
data = wf.readframes(chunk)

# play stream (looping from beginning of file to the end)
while data:
    # writing to the stream is what *actually* plays the sound.
    stream.write(data)
    data = wf.readframes(chunk)

# cleanup stuff.
wf.close()
stream.close()    
p.terminate()

print("end sound")