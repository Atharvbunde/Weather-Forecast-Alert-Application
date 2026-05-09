from weather_chart import generate_weather_chart
import os
import csv
from datetime import datetime

import requests
from dotenv import load_dotenv


# ==============================
# LOAD API KEY
# ==============================
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


# ==============================
# ALERT CHECK FUNCTION
# ==============================
def check_alerts(temp, humidity, weather_condition):
    alerts = []

    if temp >= 35:
        alerts.append("🔥 High Temperature Alert: Very hot weather.")

    if humidity >= 80:
        alerts.append("💧 High Humidity Alert: Humidity is very high.")

    if "rain" in weather_condition.lower():
        alerts.append("🌧 Rain Alert: Carry an umbrella.")

    if "storm" in weather_condition.lower() or "thunder" in weather_condition.lower():
        alerts.append("⛈ Storm Alert: Avoid unnecessary travel.")

    if not alerts:
        alerts.append("✅ No major weather alert.")

    return alerts


# ==============================
# FETCH LIVE WEATHER
# ==============================
# ==============================
# FETCH LIVE WEATHER
# ==============================
def fetch_weather(city):

    if not API_KEY:
        print("❌ API key not found.")
        return None

    url = (
        f"http://api.weatherapi.com/v1/current.json"
        f"?key={API_KEY}&q={city}&aqi=yes"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            print("❌ Error:", data.get("error", {}).get("message", "Unable to fetch data"))
            return None

        return data

    except requests.exceptions.RequestException as e:
        print("❌ Network error:", e)
        return None


# ==============================
# SAVE REPORT
# ==============================
def save_report(city, temp, humidity, condition, alerts):
    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/weather_report_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["City", "Temperature (°C)", "Humidity (%)", "Condition", "Alerts", "Date Time"])
        writer.writerow([
            city,
            temp,
            humidity,
            condition,
            " | ".join(alerts),
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ])

    print(f"\n📁 Report saved successfully: {filename}")


# ==============================
# SIMULATION MODE
# ==============================
def simulation_mode():
    
    print("\n===== SIMULATION MODE =====")

    sample_data = {
        "city": "Pune",
        "temperature": 38,
        "humidity": 85,
        "condition": "Rain"
    }

    city = sample_data["city"]
    temp = sample_data["temperature"]
    humidity = sample_data["humidity"]
    condition = sample_data["condition"]

    alerts = check_alerts(temp, humidity, condition)

    display_output(city, temp, humidity, condition, alerts)
    generate_weather_chart(city, temp, humidity)
    save_report(city, temp, humidity, condition, alerts)


# ==============================
# DISPLAY OUTPUT
# ==============================
def display_output(city, temp, humidity, condition, alerts):
    print("\n========== WEATHER REPORT ==========")
    print(f"📍 City: {city}")
    print(f"🌡 Temperature: {temp} °C")
    print(f"💧 Humidity: {humidity}%")
    print(f"☁ Condition: {condition}")

    print("\n========== ALERTS ==========")
    for alert in alerts:
        print(alert)


# ==============================
# LIVE API MODE
# ==============================
def live_api_mode():
    
    print("\n===== LIVE API MODE =====")
    city = input("Enter city name: ")

    data = fetch_weather(city)

    if data is None:
        return

    temp = data["current"]["temp_c"]
    humidity = data["current"]["humidity"]
    condition = data["current"]["condition"]["text"]

    alerts = check_alerts(temp, humidity, condition)

    display_output(city, temp, humidity, condition, alerts)
    generate_weather_chart(city, temp, humidity)
    save_report(city, temp, humidity, condition, alerts)


# ==============================
# MAIN MENU
# ==============================
def main():
    print("====================================")
    print(" WEATHER FORECAST & ALERT APP")
    print("====================================")
    print("1. Live API Mode")
    print("2. Simulation Mode")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        live_api_mode()
    elif choice == "2":
        simulation_mode()
    elif choice == "3":
        print("Exiting application...")
    else:
        print("❌ Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()