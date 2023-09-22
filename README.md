# weatherApp
This GitHub repository hosts the source code for a Python-based weather application. The application skillfully merges Weather API and Google API to provide real-time weather updates and location-based data. It showcases advanced programming capabilities and effective API integration.
Certainly! Here's a simple README.md file for your Git repository:
# Weather App

## Overview

The Weather App is a Python application that provides current weather information and forecasts for a given location. It fetches weather data from the [WeatherAPI](http://api.weatherapi.com/) and provides various weather-related details.

## Features
![Weather 9_22_2023 5_49_29 PM](https://github.com/EBOD13/weatherApp/assets/74140112/549abea6-d734-4e1e-bb14-ae88987031b6)

- Display of current temperature, condition, and location.
- Daily weather forecast for the next seven days.
- Additional weather information, such as wind speed, feels like temperature, and air quality.
- Inspirational quotes updated at regular intervals.
- Dynamic user interface with rounded frames and icons.

## Requirements

To run the Weather App, you need the following:

- Python 3.x
- Required Python libraries (tkinter, customtkinter, geocoder, requests, pandas, PIL)
- WeatherAPI API key
- Ninja API key (for inspirational quotes)

## Installation

1. Clone this repository to your local machine:

shell
git clone https://github.com/EBOD13/weather-app.git


2. Install the required Python libraries if you haven't already:

shell
pip install tkinter customtkinter geocoder requests pandas pillow

3. Replace the API keys in the code:
   - Replace `YOUR NINJA API KEY"` with your Ninja API key.
   - Replace `"YOUY WEATHER API KEY"` with your WeatherAPI API key.

4. Run the Weather App:

shell
python weather_app.py

## Usage

- Upon launching the app, it will fetch the current weather for your location based on your IP address.
- You can view the current temperature, condition, and location at the top.
- The daily weather forecast for the next seven days is displayed in the rounded frames below.
- Additional weather information is available in the squares at the bottom.
- Inspirational quotes are updated at regular intervals in the center of the app.
- You can scroll through the weather forecast using your mouse wheel.
- Clicking the map icon will provide additional functionality (you can add details here).

## Credits

This Weather App was created by Daniel Esambu.

## License
