@app.route("/dashboard")
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
