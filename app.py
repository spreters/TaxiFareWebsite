# from os import pardir
import streamlit as st
import datetime
import requests
import pandas as pd
from geopy.geocoders import Nominatim


def find_coordinates(address):
    geolocator = Nominatim(user_agent="my_request")
    location = geolocator.geocode(address, addressdetails=True)
    # return (location.address, location.latitude, location.longitude)
    if location is None:
        return None, None, None
    raw, lat, lon = location.raw, location.latitude, location.longitude
    road = raw['address'].get('road')
    house_no = raw['address'].get('house_number', '')
    postcode = raw['address'].get('postcode')
    town = raw['address'].get('town', '')
    city = raw['address'].get('city', town)
    address_ = f"{road} {house_no} 👉[ {city} ]"
    return address_, lat, lon


## HEADER TEXT & IMAGE
h1, h2 = st.columns((2, 1))
h1.markdown('''
    # ⚙️ TaxiFareModel
    ### 🚖*** Predicting a Taxi Fare in New York ***🚖
''')
h2.image(
    'https://upload.wikimedia.org/wikipedia/commons/c/cc/Taxi_picture.png')
'''---'''


## INPUT FIELDS
c1, c2 = st.columns((2, 1))
c1.write('##### Travel Route')
c2.write('##### Date & Time Location')
address_from = c1.text_input('Traveling From...', 'Empire State Building')
travel_from, pickup_latitude, pickup_longitude = find_coordinates(address_from)
if travel_from is None:
    c1.error('Could not find address ❌')
else:
    c1.success(travel_from)

address_to = c1.text_input('Traveling to...', 'Soho NY', help='test help')
travel_to, dropoff_latitude, dropoff_longitude = find_coordinates(address_to)
if travel_to is None:
    c1.error('Could not find address ❌')
else:
    c1.success(travel_to)

pickup_date = c2.date_input('Date', datetime.datetime.now())
pickup_time = c2.time_input('Time', datetime.datetime.now())


## PREPARE INPUT DATA & REQUEST PRICE PREDICTION FROM API
pickup_datetime = str(pickup_date) + " " + str(pickup_time)
url = 'https://taxi-fare-predict-api2-rxitzlhk7a-lz.a.run.app/predict'
params = {
    'pickup_datetime': pickup_datetime,
    'pickup_longitude': pickup_longitude,
    'pickup_latitude': pickup_latitude,
    'dropoff_longitude': dropoff_longitude,
    'dropoff_latitude': dropoff_latitude,
    'passenger_count': 2
}
response = requests.get(url, params=params)
prediction = response.json().get("prediction", "❌ No Price ❌")

if isinstance(prediction, float):
    prediction = "$"+str(round(prediction, 2))
    taxi_price = f'<b style="color:LightGreen; font-size: 50px;">{prediction}</b>'
    map_df = pd.DataFrame([[pickup_latitude, pickup_longitude],
                           [dropoff_latitude, dropoff_longitude]],
                          columns=['lat', 'lon'])
else:
    taxi_price = f'<b style="color:Red; font-size: 30px;">{prediction}</b>'
    map_df = None


## PLOT MAP & PRINTOUT PRICE
'''---'''
r1, r2 = st.columns((2, 1))
r1.map(map_df)
r2.write('Estimated fare price')
r2.markdown(taxi_price, unsafe_allow_html=True)
'''---'''
