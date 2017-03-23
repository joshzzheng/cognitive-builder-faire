import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import TextToSpeechV1

def convert_to_audio(text):
  text_to_speech = TextToSpeechV1(
    username=os.environ.get("TTS_USERNAME"),
    password=os.environ.get("TTS_PASSWORD"),
    x_watson_learning_opt_out=True)  # Optional flag

  with open('output.wav', 'wb') as audio_file:
    audio_file.write(
      text_to_speech.synthesize(
        text, 
        accept="audio/wav",
        voice="en-US_AllisonVoice"))

def main():
  text = "Watson loves galvanize."
  convert_to_audio(text)

if __name__ == '__main__':
  dotenv_path = join(dirname(__file__), '.env')
  load_dotenv(dotenv_path)

  main()