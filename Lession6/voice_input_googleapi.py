from google.cloud import speech
import os
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "cbotvoice-ec175f40ed8d.json"

# Creates google client
client = speech.SpeechClient()

# Full path of the audio file, Replace with your file name
file_name = os.path.join(os.path.dirname(__file__),"hello2.wav")

#Loads the audio file into memory
with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    audio_channel_count=1,
    language_code="vi-VN",
    sample_rate_hertz=24000,
)

operation = client.long_running_recognize(config=config, audio=audio)

print("Waiting for operation to complete...")
response = operation.result(timeout=90)
# Sends the request to google to transcribe the audio
# response = client.recognize(request={"config": config, "audio": audio})

# Reads the response
for result in response.results:
    # The first alternative is the most likely one for this portion.
    print(u"Transcript: {}".format(result.alternatives[0].transcript))
    print("Confidence: {}".format(result.alternatives[0].confidence))
    
