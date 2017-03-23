import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText

from recorder.recorder import Recorder

def transcribe_audio(path_to_audio_file):
  username = os.environ.get("STT_USERNAME")
  password = os.environ.get("STT_PASSWORD")
  speech_to_text = SpeechToText(username=username,
                                password=password)

  with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
    return speech_to_text.recognize(audio_file,
      content_type='audio/wav')

def main():
  recorder = Recorder("speech.wav")

  print("Please say something into the microphone\n")
  recorder.record_to_file()

  print("Transcribing audio....\n")
  result = transcribe_audio('speech.wav')
  
  text = result['results'][0]['alternatives'][0]['transcript']
  print("Text: " + text + "\n")

if __name__ == '__main__':
  dotenv_path = join(dirname(__file__), '.env')
  load_dotenv(dotenv_path)

  try:
    main()
  except:
    print("IOError detected, restarting...")
    main()


