import requests
import pprint
from configs import *

# This is the URL of the API request
url = "https://api.tomorrow.io/v4/timelines"

generic_querystring = {
    "location": "33, -84",
    "fields": ["temperature", "precipitationIntensity", "cloudCover"],
    "units": "imperial",
    "timesteps": "1h",
    "apikey": TOMIO_API
}

# response = requests.request("GET", url, params=generic_querystring)
# result = response.json()['data']['timelines'][0]['intervals']
#
# pprint.pprint(result)
# print("\n\n\n")
#
# for hourly in result:
#     date = hourly['startTime'][:10]
#     hour = hourly['startTime'][11:]
#     temp = round(hourly['values']['temperature'])
#     print("On the day " + date + " it will be " + str(temp) + "F at time ~" + hour)

    # Pretty much done with setting up the TomorrowAPI calls.

def weather_testing_action(city):
    response = requests.request("GET", url, params=generic_querystring)
    result = response.json()['data']['timelines'][0]['intervals']
    pprint.pprint(result)


def get_forecast(city):
    query = generic_querystring.copy()
    query["location"] = "33, -84"
    print("On the day " + date + " it will be " + str(temp) + "F at time ~" + hour)
