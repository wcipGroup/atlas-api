import json

class debugResponse():
    def __init__(self, source):
        self.status_code = 200
        if source == "openweathermap":
            self.text = json.dumps(openweathermap)
        elif source == "weatherapi":
            self.text = json.dumps(weatherapi)
        elif source == "weatherstack":
            self.text = json.dumps(weatherstack)


openweathermap = {
    "base": "stations",
    "clouds": {
        "all": 0
    },
    "cod": 200,
    "coord": {
        "lat": 40.64,
        "lon": 22.94
    },
    "dt": 1595588181,
    "id": 734077,
    "main": {
        "feels_like": 303.88,
        "humidity": 45,
        "pressure": 1010,
        "temp": 304.62,
        "temp_max": 307.04,
        "temp_min": 303.15
    },
    "name": "Thessaloniki",
    "sys": {
        "country": "GR",
        "id": 6658,
        "sunrise": 1595560665,
        "sunset": 1595613085,
        "type": 1
    },
    "timezone": 10800,
    "visibility": 10000,
    "weather": [
        {
            "description": "clear sky",
            "icon": "01d",
            "id": 800,
            "main": "Clear"
        }
    ],
    "wind": {
        "deg": 270,
        "speed": 5.1
    }
}

weatherapi = {
    "location": {
        "name": "Thessaloniki",
        "region": "Central Macedonia",
        "country": "Greece",
        "lat": 40.64,
        "lon": 22.93,
        "tz_id": "Europe/Athens",
        "localtime_epoch": 1595598720,
        "localtime": "2020-07-24 16:52"
    },
    "current": {
        "last_updated_epoch": 1595598343,
        "last_updated": "2020-07-24 16:45",
        "temp_c": 33.0,
        "temp_f": 91.4,
        "is_day": 1,
        "condition": {
            "text": "Partly cloudy",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
            "code": 1003
        },
        "wind_mph": 6.9,
        "wind_kph": 11.2,
        "wind_degree": 230,
        "wind_dir": "SW",
        "pressure_mb": 1009.0,
        "pressure_in": 30.3,
        "precip_mm": 0.0,
        "precip_in": 0.0,
        "humidity": 34,
        "cloud": 25,
        "feelslike_c": 34.0,
        "feelslike_f": 93.1,
        "vis_km": 10.0,
        "vis_miles": 6.0,
        "uv": 8.0,
        "gust_mph": 12.3,
        "gust_kph": 19.8
    }
}

weatherstack = {
  "request":{
    "type":"City",
    "query":"Thessaloniki, Greece",
    "language":"en",
    "unit":"m"
  },
  "location":{
    "name":"Thessaloniki",
    "country":"Greece",
    "region":"Central Macedonia",
    "lat":"40.644",
    "lon":"22.931",
    "timezone_id":"Europe\/Athens",
    "localtime":"2020-07-24 17:13",
    "localtime_epoch":1595610780,
    "utc_offset":"3.0"
  },
  "current":{
    "observation_time":"02:13 PM",
    "temperature":33,
    "weather_code":116,
    "weather_icons":["https:\/\/assets.weatherstack.com\/images\/wsymbols01_png_64\/wsymbol_0002_sunny_intervals.png"],
    "weather_descriptions":["Partly cloudy"],
    "wind_speed":11,
    "wind_degree":230,
    "wind_dir":"SW",
    "pressure":1009,
    "precip":0,
    "humidity":34,
    "cloudcover":25,
    "feelslike":34,
    "uv_index":8,
    "visibility":10,
    "is_day":"yes"
  }
}