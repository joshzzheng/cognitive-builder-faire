import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText

from recorder.recorder import Recorder
def transcribe_audio(stt, path_to_audio_file):
  with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
    return stt.recognize(audio_file,
      content_type='audio/wav')

def main():
  dotenv_path = join(dirname(__file__), '.env')
  load_dotenv(dotenv_path)
  
  stt = SpeechToText(
          username=os.environ.get("STT_USERNAME"),
          password=os.environ.get("STT_PASSWORD"))

  recorder = Recorder("speech.wav")

  print("Please say something into the microphone\n")
  recorder.record_to_file()

  print("Transcribing audio....\n")
  result = transcribe_audio(stt, 'speech.wav')
  
  text = result['results'][0]['alternatives'][0]['transcript']
  print("Text: " + text + "\n")

if __name__ == '__main__':
  try:
    main()
  except:
    print("IOError detected, restarting...")
    main()


