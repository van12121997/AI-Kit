#!/usr/bin/env python3
# coding: utf-8

from gtts import gTTS
from playsound import playsound

from audio import list_audio_devices
from audio import AudioInput
from soundfile import SoundFile

import pyttsx3 as pt
import speech_recognition as sr
from google.cloud import speech
import os
import io

from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2






GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=(string)NV12, framerate=20/1 ! nvvidconv flip-method=0 ! video/x-raw, width=640, height=480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "cbotvoice-330303-6a7f0d4b95d9.json"

# Creates google client
client = speech.SpeechClient()

# voice input-----
r = sr.Recognizer()

# voice output-----
engine = pt.init()

input_mic = AudioInput(mic=11, sample_rate=44100, chunk_size=16000)

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open("face.pickle", "rb").read())

scale_percent = 60

list_audio_devices()

print("[INFO] starting video stream...")

writer = None
time.sleep(2.0)



def speak(sent):
    tts = gTTS(sent, tld='com.vn', lang='vi')
    tts.save('voice.mp3')
    playsound('voice.mp3')

def face_reg(frame, model):

    # convert the input frame from BGR to RGB then resize it to have
    # a width of 750px (to speedup processing)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    rgb = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    r = frame.shape[1] / float(rgb.shape[1])
    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input frame, then compute
    # the facial embeddings for each face
    boxes = face_recognition.face_locations(rgb,
                                            model=model)
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

    return names

print("start")
sample_count_end = 44100*5 #record 5s
sample_count = 0

record = True

output_wav = SoundFile('test.wav', mode='w', samplerate=44100, channels=1)

while record:
	print("1")
	samples = input_mic.next()
	print("1")
	output_wav.write(samples)
	sample_count += len(samples)
	print("xxx")
	if sample_count > sample_count_end:
		record=False

output_wav.close()
print("Check: ")
filename = 'test.wav'

with sr.AudioFile(filename) as source:
	audio_data = r.record(source)
	audio = speech.RecognitionAudio(content=audio_data.get_wav_data(convert_rate=44100, convert_width=2))

config = speech.RecognitionConfig(
	encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
	audio_channel_count=1,
	language_code="vi-VN",
	sample_rate_hertz=44100,
)

operation = client.long_running_recognize(config=config, audio=audio)

print("Waiting for operation to complete...")
response = operation.result(timeout=90)

for result in response.results:
	print(u"Transcript: {}".format(result.alternatives[0].transcript))
	print("Confidence: {}".format(result.alternatives[0].confidence))

	if result.alternatives[0].transcript == "Xin chào":
		speak("Xin chào")
	elif result.alternatives[0].transcript == "bạn là ai":
		speak("Tôi là AI kit")

count = 0
count_ = 0

masterName = "Van"
notMaster = True
vs = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
while notMaster:
    ret, frame = vs.read()

    count_ = count_ + 1
    # print(count_)

    if count_ > 100:

        names = face_reg(frame, model="hog")

        for name in names:
                if name == masterName:
                    count = count + 1
                    if count > 10:
                        print("Hello master")
                        speak("Xin chào master")
                        notMaster = False
vs.release()
cv2.destroyAllWindows()

#    cv2.imshow("Frame", frame)
#    key = cv2.waitKey(1) & 0xFF



print("Check: " + str(count_))

time.sleep(2.0)
#recordVoice()
   # print(answer)





