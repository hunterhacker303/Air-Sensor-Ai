from flask import Flask,render_template,url_for,redirect,request,jsonify
import requests
import random
from datetime import datetime, timedelta
app=Flask(__name__)

API_KEY = "e986662eae274cd194f70404251112"
BASE_URL = "http://api.weatherapi.com/v1/current.json"


# app.py (add these helper functions)

def get_aqi_level(aqi: float | int) -> str:
    """
    Convert a numeric AQI value into a textual category.
    Uses common breakpoints (0-500).
    """
    try:
        aqi = float(aqi)
    except (TypeError, ValueError):
        return "Unknown"

    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    if aqi <= 500:
        return "Hazardous"
    return "Unknown"

def get_aqi_color(level: str) -> str:
    """
    Map textual AQI level to a color hex string.
    Level should be one of: Good, Moderate, Unhealthy, Very Unhealthy, Hazardous.
    """
    if not level:
        return "#9ca3af"  # neutral gray

    level = str(level).strip().lower()
    mapping = {
        "good": "#16a34a",           # green
        "moderate": "#f59e0b",       # amber/yellow
        "unhealthy": "#ef4444",      # red
        "very unhealthy": "#8b5cf6", # purple
        "very_unhealthy": "#8b5cf6", # alternative key
        "hazardous": "#7f1d1d",      # maroon/dark red
        "unknown": "#9ca3af"
    }
    return mapping.get(level, "#9ca3af")

def get_aqi_color_from_value(aqi_value) -> str:
    """Convenience: numeric AQI -> category -> hex color"""
    level = get_aqi_level(aqi_value)
    return get_aqi_color(level)


def get_latest_sensor_data():
    return {
        "aqi": random.randint(50, 200),
        "pm25": random.randint(10, 150),
        "pm10": random.randint(20, 250),
        "voc": random.randint(50, 400),
        "temp": random.randint(20, 35),
        "humidity": random.randint(20, 90),
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": "Unhealthy"  # temporary value
    }


def get_forecast():
    return {
        "aqi": 95,
        "level": "Moderate"
    }

def choose_precaution(level):
    level = level.lower()

    if level == "good":
        return "It’s a great day to go outside!"
    if level == "moderate":
        return "Air quality is acceptable; sensitive individuals should take care."
    if level == "unhealthy":
        return "Wear an N95 mask outdoors and limit outdoor exposure."
    if level == "very unhealthy":
        return "Avoid going outside and keep doors/windows closed."
    if level == "hazardous":
        return "Stay indoors. Outdoor exposure is extremely dangerous."

    return "Air quality data unavailable."

def get_history_data():
    now = datetime.now()
    history = []

    for i in range(24):
        history.append({
            "timestamp": now - timedelta(hours=24 - i),
            "pm25": random.randint(10, 180),
            "pm10": random.randint(20, 250)
        })

    return history

def get_device_status():
    return {
        "status": "online",
        "lastSeen": datetime.now().strftime("%H:%M:%S"),
        "signalStrength": -65,
        "battery": 78,
        "sensorStatus": {
            "pm": True,
            "voc": True,
            "dht": True
        }
    }

def get_forecast_6h():
    now = datetime.now()
    forecast = []

    base_aqi = random.randint(50, 150)

    for i in range(6):
        forecast.append({
            "timestamp": now + timedelta(hours=i),
            "aqi": base_aqi + random.randint(-20, 20)
        })

    return forecast



@app.route("/")
def home():
    dashboard = get_latest_sensor_data()
    device = get_device_status()
    history = get_history_data()
    forecast = get_forecast_6h()

    # Format history timestamps
    for h in history:
        h["time"] = h["timestamp"].strftime("%H:%M")

    trend = "Rising" if forecast[-1]["aqi"] > forecast[0]["aqi"] else "Falling"

    
    city = "Bhopal"  
    params = {
        "key": API_KEY,
        "q": city,
        "aqi": "yes"
    }

    weather_res = requests.get("https://api.weatherapi.com/v1/current.json", params=params).json()

    weather = {
        "city": weather_res["location"]["name"],
        "country": weather_res["location"]["country"],
        "temp_c": weather_res["current"]["temp_c"],
        "condition": weather_res["current"]["condition"]["text"],
        "icon": weather_res["current"]["condition"]["icon"]
    }

    return render_template(
        "home.html",
        data=dashboard,
        status=device,
        data_history=history,
        forecast=forecast,
        next_hour_aqi=forecast[0]["aqi"],
        trend=trend,

        # 🔥 REQUIRED (your missing piece)
        weather=weather
    )


@app.route("/api/live")
def live():
    return {
        "aqi": 87,
        "pm25": 34,
        "pm10": 78,
        "voc": 102,
        "time": "2025-11-20 14:20"
    }

@app.route("/api/predict")
def predict():
    return {
        "predicted_aqi": 120,
        "summary": "AQI expected to rise. Avoid going out."
    }

@app.route("/Awareness")
def awareness():
    return render_template("Awareness.html")

@app.route("/Dashboard")

def dashboard():
    data = get_latest_sensor_data()  # your function
    next_hour = get_forecast()

    # If data already contains textual level, use it; otherwise derive from numeric aqi
    data_level = data.get("level") if data.get("level") else get_aqi_level(data.get("aqi"))
    precaution = choose_precaution(data_level)  # implement or use a static mapping

    aqi_color = get_aqi_color(data_level)
    forecast_color = get_aqi_color_from_value(next_hour.get("aqi")) if next_hour and next_hour.get("aqi") is not None else "#9ca3af"

    return render_template(
        "Dashboard.html",
        data=data,
        next_hour=next_hour,
        aqi_color=aqi_color,
        forecast_color=forecast_color,
        precaution=precaution
        

    )
@app.route("/settings")
def settings_page():
    return render_template("settings.html")

# @app.route("/dashboard")
# def dashboard():

#     city = request.args.get("city", "Bhopal")  # default for testing

#     params = {
#         "key": API_KEY,
#         "q": city,
#         "aqi": "yes"
#     }

#     response = requests.get(BASE_URL, params=params)
#     data = response.json()

#     # ---- Extract AQI ----
#     aqi = int(data["current"]["air_quality"]["pm2_5"])   # Using PM2.5 as AQI approximation

#     # ---- Determine AQI Level ----
#     if aqi <= 50:
#         level = "Good"
#         aqi_color = "#4CAF50"
#         precaution = "No precautions needed."
#     elif aqi <= 100:
#         level = "Moderate"
#         aqi_color = "#FFEB3B"
#         precaution = "Sensitive individuals should reduce outdoor activity."
#     elif aqi <= 150:
#         level = "Unhealthy for sensitive groups"
#         aqi_color = "#FF9800"
#         precaution = "Limit prolonged outdoor exertion."
#     else:
#         level = "Unhealthy"
#         aqi_color = "#F44336"
#         precaution = "Avoid outdoor activities."

#     # ---- Forecast dummy (WeatherAPI free tier has limited AQI forecast) ----
#     next_hour = {
#         "aqi": aqi + 5,
#         "level": level
#     }
#     forecast_color = aqi_color

#     # ---- Build final dictionary that matches your HTML ----
#     final_data = {
#         "timestamp": data["location"]["localtime"],
#         "aqi": aqi,
#         "level": level,
#         "pm25": data["current"]["air_quality"]["pm2_5"],
#         "pm10": data["current"]["air_quality"]["pm10"],
#         "voc": data["current"]["air_quality"].get("co", 0),
#         "temp": data["current"]["temp_c"],
#         "humidity": data["current"]["humidity"],
#     }

#     return render_template(
#         "dashboard.html",
#         data=final_data,
#         precaution=precaution,
#         next_hour=next_hour,
#         aqi_color=aqi_color,
#         forecast_color=forecast_color
#     )
latest_esp32_data = {}

@app.route("/update", methods=["POST"])
def update_from_esp32():
    global latest_esp32_data

    print("----- NEW REQUEST -----")
    print("Raw data:", request.data)
    print("JSON:", request.get_json())
    print("------------------------")

    latest_esp32_data = request.get_json()
    return {"status": "ok"}



@app.route("/api/esp32")
def api_esp32():
    return latest_esp32_data


@app.route("/esp32")
def esp32_page():
    return render_template("esp32.html")


@app.route("/DeviceStatus")
def device_status():
    status = {
        "status": "online",
        "lastSeen": "12:45 PM",
        "signalStrength": -55,
        "battery": 78,
        "sensorStatus": {
            "pm": True,
            "voc": False,
            "dht": True
        }
    }
    return render_template("DeviceStatus.html", status=device_status)

@app.route("/Trends")
def trends_page():
    history = get_history_data()

    formatted = []
    for d in history:
        formatted.append({
            "time": d["timestamp"].strftime("%H:%M"),
            "pm25": d["pm25"],
            "pm10": d["pm10"]
        })

    return render_template("Trends.html", data=formatted)

@app.route("/forecast")
def forecast_page():

    forecast_points = get_forecast_6h()   # your function → returns list of dicts

    formatted = []
    for p in forecast_points:
        formatted.append({
            "time": p["timestamp"].strftime("%H:%M"),
            "aqi": p["aqi"]
        })

    # Trend comparison
    trend = "Rising" if formatted[-1]["aqi"] > formatted[0]["aqi"] else "Falling"

    return render_template(
        "forecast.html",
        forecast=formatted,
        next_hour_aqi=formatted[0]["aqi"],
        trend=trend
    )



# Serve the settings page
@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/weather")
def get_weather():
    city = request.args.get("city")

    if not city:
        return "City parameter is required"

    params = {"key": API_KEY, "q": city, "aqi": "no"}
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return "API request failed"

    data = response.json()

    weather = {
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temp_c": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"],
        "icon": data["current"]["condition"]["icon"]
    }

    return render_template("Dashboard.html", weather=weather)


if __name__=="__main__":

    test_vals = [10, 55, 120, 250, 420, None, "abc"]
    for t in test_vals:
        print(t, get_aqi_level(t), get_aqi_color_from_value(t))

    app.run(host="0.0.0.0",port=5000,debug=True)