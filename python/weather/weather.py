import requests
import os
import pprint
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

################################################################################
# Get credentials from .env
################################################################################
USERNAME = os.environ.get("WEATHER_USERNAME")
PASSWORD = os.environ.get("WEATHER_PASSWORD")

################################################################################
# Get latude and longitude coordinates for given address
################################################################################
address = input("Please enter your address: ")
payload = {'query': address, 'locationType': 'address', 'language': 'en-US'}
r = requests.get(
  'https://' + 
  USERNAME + ':' + PASSWORD + 
  '@twcservice.mybluemix.net/api/weather/v3/location/search', 
  params=payload)

location = r.json()['location']['address'][0]

lat = r.json()['location']['latitude'][0]
lon = r.json()['location']['longitude'][0]

################################################################################
# Get 7 day forcast from latude and longitude coordinates
################################################################################
payload = {'units':'e'}
r = requests.get('https://' + 
  USERNAME + ':' + PASSWORD + 
  '@twcservice.mybluemix.net/api/weather/v1/geocode/' + 
  str(lat) + '/' + str(lon) + 
  '/forecast/daily/7day.json',
   params=payload)

print()
print('7 day forcast for ' + location + ':')
for thing in r.json()['forecasts']:
  if 'day' in thing:
    print(thing['dow'] + ': ' + str(thing['day']['temp']))
  elif 'night' in thing:
    print(thing['dow'] + ': ' + str(thing['night']['temp']))

################################################################################
# Get historical hourly forcast up to 23 hours into the past
################################################################################
payload = {'hours': 23}
r = requests.get(
  'https://' + USERNAME + ':' + PASSWORD + 
  '@twcservice.mybluemix.net/api/weather/v1/geocode/' + 
  str(lat) + '/' + str(lon) + '/observations/timeseries.json', 
  params=payload)

min_temp = sys.maxsize
max_temp = 0
chart = [0 for x in range(200)]
index = 0
for thing in r.json()['observations']:
  if 'temp' in thing:
    if chart[thing['temp']] != 0:
      chart[thing['temp']][index] = 1
    else:
      row = [0 for x in range(24)]
      row[index] = 1
      chart[thing['temp']] = row
    index += 1
    if thing['temp'] < min_temp:
      min_temp = thing['temp']
    elif thing['temp'] > max_temp:
      max_temp = thing['temp']
print()
print('Historical hourly forcast (23 hours into the past):')
print('_________________________ ' + str(max_temp) + '° ___________________')
for y in chart:
  if y == 0:
    if y > min_temp and y < max_temp:
      print()
  else:
    for x in y:
      if x == 0:
        print('   ', end='')
      else:
        print('***', end='')
    print()
print('____________________ ' + str(min_temp) + '° _____________________')
