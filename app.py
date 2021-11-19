from os import pardir
import streamlit as st
import datetime
import requests

'''
# TaxiFareModel
### ***Predicting the Taxi Fare !***
---'''

columns = st.columns(3)
columns[0].write('##### Pickup Location')
columns[1].write('##### Dropoff Location')
columns[2].write('##### Date & Time Location')

pickup_longitude = columns[0].text_input('Longitude', 40.7614327)
pickup_latitude = columns[0].text_input('Latitude', 73.9798156)

dropoff_longitude = columns[1].text_input('Longitude', 40.6513111)
dropoff_latitude = columns[1].text_input('Latitude', 73.8803331)

pickup_date = columns[2].date_input('Date', datetime.datetime.now())
pickup_time = columns[2].time_input('Time', datetime.datetime.now())
# passenger_count = columns[2].text_input('No. of Passengers', 1)

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

prediction = response.json().get("prediction", "❌ No predicted Price found ❌")
if isinstance(prediction, float):
    prediction = "$"+str(round(prediction, 2))


'''---'''
columns2 = st.columns(3)
columns2[2].metric('Estimated fare price', prediction)
'''---'''
