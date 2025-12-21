import requests
import pyttsx3
import tkinter as tk
from tkinter import messagebox

# -------------------- CONFIG --------------------
API_KEY = "15ec3d046c86417e8b2135427252012"   # <-- put your WeatherAPI key here

# -------------------- TEXT TO SPEECH --------------------
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -------------------- AQI INTERPRETATION --------------------
def interpret_aqi(index):
    if index == 1:
        return "Good"
    elif index == 2:
        return "Moderate"
    elif index == 3:
        return "Unhealthy for Sensitive Groups"
    elif index == 4:
        return "Unhealthy"
    elif index == 5:
        return "Very Unhealthy"
    else:
        return "Hazardous"

# -------------------- WEATHER FUNCTION --------------------
def get_weather():
    city = city_entry.get().strip()

    if city == "":
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    city = city.title()
    result_label.config(text="Fetching weather...")
    get_weather_btn.config(state="disabled")
    root.update()

    url = (
        f"https://api.weatherapi.com/v1/current.json"
        f"?key={API_KEY}&q={city}&aqi=yes"
    )

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        air = current["air_quality"]

        temp = current["temp_c"]
        condition = current["condition"]["text"]
        humidity = current["humidity"]
        wind = current["wind_kph"]

        pm25 = air["pm2_5"]
        pm10 = air["pm10"]
        aqi_index = air["us-epa-index"]
        aqi_status = interpret_aqi(aqi_index)

        result_text = (
            f"City: {city}\n"
            f"Temperature: {temp} °C\n"
            f"Condition: {condition}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} km/h\n\n"
            f"Air Quality Index:\n"
            f"Status: {aqi_status}\n"
            f"PM2.5: {pm25}\n"
            f"PM10: {pm10}"
        )

        result_label.config(text=result_text)

        speak(
            f"Weather in {city}. Temperature {temp} degrees Celsius. "
            f"Condition {condition}. Air quality is {aqi_status}."
        )

        if aqi_index >= 4:
            speak("Warning. Air quality is unhealthy. Avoid outdoor activities.")

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Unable to fetch weather data")

    finally:
        get_weather_btn.config(state="normal")

# -------------------- GUI SETUP --------------------
root = tk.Tk()
root.title("Smart Weather App")
root.geometry("420x420")
root.resizable(False, False)

TITLE_FONT = ("Arial", 16, "bold")
LABEL_FONT = ("Arial", 12)
RESULT_FONT = ("Arial", 11)

tk.Label(root, text="Weather Information System", font=TITLE_FONT).pack(pady=10)

tk.Label(root, text="Enter City Name:", font=LABEL_FONT).pack()
city_entry = tk.Entry(root, font=LABEL_FONT, width=25)
city_entry.pack(pady=5)
city_entry.focus()

city_entry.bind("<Return>", lambda event: get_weather())

get_weather_btn = tk.Button(
    root,
    text="Get Weather",
    font=LABEL_FONT,
    bg="blue",
    fg="white",
    command=get_weather
)
get_weather_btn.pack(pady=10)

result_label = tk.Label(root, text="", font=RESULT_FONT, justify="left")
result_label.pack(pady=10)

# Keyboard shortcut to exit
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
