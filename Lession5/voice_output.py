from gtts import gTTS
import os
from playsound import playsound
import pyttsx3 as pt

from pydub import AudioSegment
from pydub.playback import play

# voice output-----
engine = pt.init()


def speak(sent):
    engine.say(sent)
    engine.runAndWait()
    print(sent)
    return sent

tts = gTTS('Xin chào các bạn tôi rất ngu và không chạy được', tld='com.vn', lang='vi')

tts.save('hello.wav')
# playsound('hello.wav')

# song = AudioSegment.from_wav("hello.wav")
# play(song)
