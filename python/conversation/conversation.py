import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import ConversationV1
from watson_developer_cloud import ToneAnalyzerV3

context = {}

def get_emotion(tone_analyzer, text):
  result = tone_analyzer.tone(text=text)
  tones = result['document_tone']['tone_categories'][0]['tones']
  
  max_score = 0
  max_emotion = ''
  for tone in tones:
    if float(tone['score']) > max_score:
      max_emotion = tone['tone_id']
      max_score = float(tone['score'])
  
  return max_emotion

def send_message(conversation, workspace_id, message, emotion):
  global context
  context['emotion'] = emotion
  
  response = conversation.message(
    workspace_id=workspace_id, 
    message_input={'text': message},
    context=context)
  context = response['context']
  print(response['output']['text'][0])

def main():
  dotenv_path = join(dirname(__file__), '.env')
  load_dotenv(dotenv_path)

  workspace_id = os.environ.get("WORKSPACE_ID")
  conversation = ConversationV1(
      username=os.environ.get("CONVERSATION_USERNAME"),
      password=os.environ.get("CONVERSATION_PASSWORD"),
      version='2016-09-20')

  tone_analyzer = ToneAnalyzerV3(
      username=os.environ.get("TONE_ANALYZER_USERNAME"),
      password=os.environ.get("TONE_ANALYZER_PASSWORD"),
      version='2016-02-11')

  while(True):
    message = input("User input: ")
    emotion = get_emotion(tone_analyzer, message)
    response = send_message(conversation, workspace_id, message, emotion)

if __name__ == '__main__':
  main()

