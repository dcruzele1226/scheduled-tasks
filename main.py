import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

latitude = 41.809405
longitude = -71.426234

weather_params = {
    "lat": latitude,
    "lon": longitude,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_date = response.json()

will_rain = False
for hour_data in weather_date["list"]:
    cond_codes = hour_data["weather"][0]["id"]
    if int(cond_codes) < 700:
        will_rain = True
    print(cond_codes)

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain. Bring an umbrella!",
        from_="+18554496471",
        to="+14015561621",
    )
    print(message.status)

