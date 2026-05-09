import os
import matplotlib.pyplot as plt
from datetime import datetime


def generate_weather_chart(city, temp, humidity):

    os.makedirs("images", exist_ok=True)

    labels = ["Temperature", "Humidity"]
    values = [temp, humidity]

    plt.figure(figsize=(6, 4))

    plt.bar(labels, values)

    plt.title(f"Weather Data - {city}")
    plt.ylabel("Values")

    filename = f"images/weather_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    plt.savefig(filename)

    print(f"📊 Chart saved: {filename}")

    plt.close()