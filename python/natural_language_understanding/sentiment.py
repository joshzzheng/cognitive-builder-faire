import os
import json
from dotenv import load_dotenv, find_dotenv
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features

def main():
    load_dotenv(find_dotenv())
    nlu_username = os.environ.get('NLU_USERNAME')
    nlu_password = os.environ.get('NLU_PASSWORD')
    nlu = NLU(username=nlu_username, password=nlu_password, version='2017-02-27')

    result = nlu.analyze(text='I hate galvanize', features=[features.Sentiment()])['sentiment']['document']

    print(result['label'], result['score'])

if __name__ == '__main__':
    main()
