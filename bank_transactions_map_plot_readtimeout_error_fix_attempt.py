#Importing modules and dataset
import pandas as pd
from urllib3.exceptions import ReadTimeoutError

data = pd.read_csv("bank_transactions.csv")

#Cleaning data
data.drop(["TransactionID"],axis=1,inplace=True)
custgender_mode = data.CustGender.mode().values[0]

data.CustGender.fillna(custgender_mode,inplace=True)
custlocation_mode = data.CustLocation.mode().values[0]
data.CustLocation.fillna(custlocation_mode,inplace=True)
custAB_median = data.CustAccountBalance.median()
data.CustAccountBalance.fillna(custAB_median,inplace=True)

data[["Birthdate", "Birthmonth", "Birthyear"]] = data["CustomerDOB"].str.split("/", expand = True)
data[["Tdate", "Tmonth", "Tyear"]] = data["TransactionDate"].str.split("/", expand = True)

data.Birthyear.fillna(data.Birthyear.median(),inplace=True)
age = []
difference = 0
for i in data.Birthyear.values:
    if int(i) < 16:
        difference = 16 - int(i)
    elif int(i) == 1800: #one observation with Birthyear 1800
        difference = 216
    else:
        difference = 100 - int(i) + 16
    age.append(difference)

data["Age"] = age

data[["Birthdate", "Birthmonth", "Birthyear"]] = data[["Birthdate", "Birthmonth", "Birthyear"]].astype(float)
data[["Tdate", "Tmonth", "Tyear"]] = data[["Tdate", "Tmonth", "Tyear"]].astype(float)

times = []
for i in data.TransactionTime.values:
    hour = i//10000
    times.append(hour)

data["TransactionHour"] = times

data.drop(["CustomerDOB"],inplace=True,axis=1)
data.drop(["TransactionDate"],inplace=True,axis=1)
data.drop(["TransactionTime"],inplace=True,axis=1)

data

from geopy.geocoders import Nominatim
import folium
import statistics
from retry import retry

import requests
import time

# Increase the timeout to 10 seconds (adjust the value as needed)
response = requests.get("https://nominatim.openstreetmap.org/search?q=SOUTH+24+PARGANAS&format=json&limit=1", timeout=100)


@retry(ReadTimeoutError, delay=2, backoff=2, tries=10)
def geocode_location(place):
    location = geolocator.geocode(place)
    return location

latitudes = []
longitudes = []
count_nonetype = 0
geolocator = Nominatim(user_agent="geoapiExercises")


for place in data['CustLocation']:
    try:
        location = geocode_location(place)
        if location is None:
            latitudes.append(0)
            longitudes.append(0)
            count_nonetype+=1
        else:
            latitudes.append (location.latitude)
            longitudes.append(location.longitude)
    except ReadTimeoutError:
        count_nonetype += 1
        latitudes.append(0)
        longitudes.append(0)
    time.sleep(5)


print("There exist", count_nonetype, "NoneType objects that have been excluded")

mean_latitude = statistics.mean(latitudes)
mean_longitude = statistics.mean(longitudes)

m = folium.Map(location= [mean_latitude, mean_longitude], zoom_start=12)

for city, lat, lon in zip(data["CustLocation"], latitudes, longitudes):
    folium.Marker(
        location=[lat, lon],
        popup=city
    ).add_to(m)

# Display the map
m.save('map.html')


'''
for city, lat, lon, amount in zip(data["CustLocation"], latitude, longitude, data["CustAccountBalance"]):
    folium.Marker(
        location=[lat, lon],
        popup=f"{city}: ${amount}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
 adds info to popup
'''
