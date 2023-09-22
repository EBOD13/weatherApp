import random
import re
import tkinter
from tkinter import *
import tkinter as tk
import customtkinter as ctk
import geocoder
import requests
import pandas as pd
from PIL import Image, ImageTk
from datetime import datetime

# ----------- Get the current location based on IP address --------------------
class WeatherApp:
    def __init__(self):
        # IMPORTANT APP GUI PROPERTIES
        self.ninja_API = "YOUR NINJA API KEY"
        self.wind_speed = None
        self.API_KEY = "YOUR WEATHER API KEY"
        self.BASE_URL = "http://api.weatherapi.com/v1/"
        self.app = ctk.CTk()
        self.app.geometry("350x653")
        self.app.title("Weather")  # Window title
        self.app.iconbitmap('cloudy.ico')  # Window main icon
        self.width, self.height = self.app.winfo_screenwidth(), self.app.winfo_screenheight()
        self.main_fg_color = "#011f4b"
        self.secondary_color = "#142c5e"
        self.tertiary_color = "#b3cde0"
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(self.app, height=self.height, width=self.width, fg_color=self.main_fg_color)
        self.main_frame.pack()

        geocode = geocoder.ip('me')
        if geocode.ok:
            global location_lat, location_long
            location_lat, location_long = geocode.latlng
        else:
            print("Unable to retrieve current location.")

        self.request_url = self.BASE_URL + "current.json?" + "key=" + self.API_KEY + "&q=" + str(
            location_lat) + "," + str(location_long)
        self.response = requests.get(self.request_url).json()
        self.location_name = self.response['location']['name']
        # --------------------------- API FOR DAILY WEATHER INFORMATION ------------------------
        self.daily_response = requests.get(
            f'http://api.weatherapi.com/v1/forecast.json?key={self.API_KEY}&q={self.location_name}&days=7').json()
        self.data = self.daily_response['forecast']['forecastday']

        # -------------------------- ALL IMPORTANT VARIABLES -------------------
        self.feelslike_c = self.response["current"]['feelslike_c']
        self.uv = self.response['current']['uv']
        self.humidity = self.response['current']['humidity'] # Get humidity
        self.wind_speed = self.response['current']['wind_kph'] / 3.6  # Get wind speed
        self.current_temp_c = self.response['current']['temp_c']
        self.current_condition = self.response['current']['condition']['text']
        self.maxTempCel = self.daily_response['forecast']['forecastday'][0]['day']['maxtemp_c']
        self.minTempCel = self.daily_response['forecast']['forecastday'][0]['day']['mintemp_c']
        self.location = ctk.CTkLabel(self.main_frame, text=self.location_name, font=("Times", 35), text_color="#b3cde0")
        self.location.place(relx=0.5, rely=0.02, anchor=tk.N)
        self.wind_dir = self.response["current"]['wind_dir']

        self.quote_label = Label(self.app, text="", font=("Times", 15, "bold italic"),
                                        background=self.main_fg_color, foreground=self.tertiary_color, wraplength=420)
        self.quote_label.place(relx=0.5, rely=0.46, anchor='center')

        # Schedule the function to update the quote label
        self.update_quote_label()

        # NINJA API
        self.levelConcern = ""
        api_url = 'https://api.api-ninjas.com/v1/airquality?city={}'.format(self.location_name)
        response = requests.get(api_url, headers={'X-Api-Key': self.ninja_API})
        if response.status_code == requests.codes.ok:
            self.aqi = response.json()['overall_aqi']
            if self.aqi < 50:
                self.levelConcern = "Good"
            elif self.aqi < 101:
                self.levelConcern = "Moderate"
            elif self.aqi < 151:
                self.levelConcern = "USG"
            elif self.aqi < 201:
                self.levelConcern = "Unhealthy"
            elif self.aqi < 301:
                self.levelConcern = "Very Unhealthy"
            elif self.aqi >= 301:
                self.levelConcern = "Hazardous"
        else:
            print("Error:", response.status_code, response.text)

        # ---------------------------- ALL THE FRAMES --------------------------------------

        self.temp_frame = ctk.CTkFrame(self.main_frame, height=190, width=190, corner_radius=150, border_width=8,
                                       border_color='#03396c',
                                       fg_color=self.main_fg_color)
        self.temp_frame.place(relx=0.5, rely=0.1, anchor="n")

        self.description_label = ctk.CTkLabel(self.temp_frame, text=str(self.current_condition).title(),
                                              font=("Times", 18),
                                              text_color="#b3cde0")
        self.description_label.place(relx=0.5, rely=0.2, anchor='center')
        # -------------------------------- DAILY TEMPERATURE WITH MAX & MIN --------------------------------------

        self.temperature = ctk.CTkLabel(self.temp_frame, text=str(int(self.current_temp_c)) + "°", font=("Times", 70),
                                        text_color=self.tertiary_color)
        self.temperature.place(relx=0.55, rely=0.48, anchor="center")
        self.max_and_min_temp = ctk.CTkLabel(self.temp_frame,
                                             text=f"H: {round(self.maxTempCel)}°  L: {round(self.minTempCel)}°",
                                             font=("Times", 17),
                                             text_color=self.tertiary_color)
        self.max_and_min_temp.place(relx=0.52, rely=0.77, anchor='center')

        # CANVAS FOR

        self.canvas = ctk.CTkCanvas(self.app, background='red', scrollregion=(0, 0, 100, 500), width=self.width,
                                    height=150, bg=self.main_fg_color, highlightbackground=self.main_fg_color)
        self.smallRoundedFrames()
        self.addSquares()

    def update_quote_label(self):
        # Fetch a new quote
        category = ['age', 'alone', 'amazing', 'anger', 'architecture', 'art', 'attitude', 'beauty', 'best', 'birthday',
                    'business', 'car', 'change', 'communications', 'computers', 'cool', 'courage',
                    'dad', 'dating', 'death', 'design', 'dreams', 'education', 'environmental', 'equality', 'experience',
                    'failure', 'faith', 'family', 'famous', 'fear', 'fitness', 'food', 'forgiveness', 'freedom',
                    'friendship', 'funny', 'future', 'god', 'good', 'government', 'graduation', 'great', 'happiness',
                    'health', 'history', 'home', 'hope', 'humor', 'imagination', 'inspirational', 'intelligence',
                    'jealousy', 'knowledge', 'leadership', 'learning', 'legal', 'life', 'love', 'marriage', 'medical',
                    'men', 'mom', 'money', 'morning', 'movies', 'success']

        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(random.choice(category))
        response = requests.get(api_url, headers={'X-Api-Key': self.ninja_API})

        if response.status_code == requests.codes.ok:
            quote = response.json()[0]['quote']
            quote_author = response.json()[0]['author']
            new_quote = quote + " - " + quote_author

            # Update the quote label text
            self.quote_label.config(text=new_quote)
        else:
            print("Error:", response.status_code, response.text)

        # Schedule the next update after 30 seconds
        self.app.after(30000, self.update_quote_label)

    def smallRoundedFrames(self):
        j = 0
        dist_x = 500
        while j < 4:

            round_frame = ctk.CTkFrame(self.canvas, height=120, width=90, fg_color='#03396c', corner_radius=60)
            round_frame.pack(side='right', padx=8)
            self.canvas.create_window((dist_x, 50), window=round_frame, anchor='nw')
            self.canvas.place(relx=0.5, rely=0.92, anchor='s', relwidth=0.95)
            dist_x += 125
            round_frame.bind("<MouseWheel>", self.on_mousewheel)
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

            # ------------------------------ DAY OF THE WEEK FORECAST -------------------------------
            if datetime.today().weekday() == pd.Timestamp(self.data[j]['date']).day_of_week:
                day_of_week = "NOW"
            else:
                day_of_week = pd.Timestamp(self.data[j]['date']).day_name()[:3].upper()

            forecast_day = ctk.CTkLabel(round_frame, text=day_of_week, font=("Times", 14), text_color="#b3cde0", )
            forecast_day.place(relx=.5, rely=0.2, anchor='center')

            # -------------------------------------FORECAST TEMPERATURE -----------------------------
            avgtemp_c = round(self.data[j]['day']['avgtemp_c'])
            forecast_avgtemp_c = ctk.CTkLabel(round_frame, text=str(avgtemp_c) + "°", font=("Times", 16),
                                              text_color="#b3cde0", )
            forecast_avgtemp_c.place(relx=.5, rely=0.8, anchor='center')

            # ----------------------- ICON INFORMATION & IMAGE ----------------------
            icon_data = self.data[j]['day']['condition']['icon']
            icon_number = re.findall("/+[day|night]+/+[0-9]+.png$", icon_data)
            icon_number = icon_number[0]
            icon_location = 'images/weather/64x64' + icon_number
            my_image = ctk.CTkImage(Image.open(icon_location), size=(45, 45))
            image_label = ctk.CTkLabel(round_frame, image=my_image, fg_color="transparent",
                                       text="")  # display image with a CTkLabel
            image_label.place(relx=0.5, rely=0.5, anchor='center')
            j += 1

    def addSquares(self):
        dist_x = 0.17
        for i in range(3):
            mini_frame = ctk.CTkFrame(self.main_frame, height=109, width=109, fg_color=self.secondary_color)
            mini_frame.place(relx=dist_x, rely=0.7, anchor='s')
            dist_x = dist_x + 0.33
            if i == 0:
                image = Image.open('images/aqit.png')
                image = image.resize((23, 23))
                wind_speed_image = ImageTk.PhotoImage(image)

                # Create a Label with both image and text
                square_label = Label(mini_frame, text=' WIND SPEED', background=self.secondary_color,
                                     font=("Times", 12), foreground=self.tertiary_color,
                                     image=wind_speed_image, compound='left')
                wind_speed_label = Label(mini_frame, text=str(round(self.wind_speed)) + " mps",
                                         background=self.secondary_color,
                                         font=("Times", 20, "bold italic"), foreground=self.tertiary_color)
                wind_dir = Label(mini_frame, text=self.wind_dir, background=self.secondary_color,
                                       font=("Times", 15, "bold italic"), foreground=self.tertiary_color)

                # Keep a reference to the PhotoImage object
                square_label.image = wind_speed_image

                square_label.place(relx=0.96, rely=0.16, anchor='e')
                wind_speed_label.place(relx=0.5, rely=0.5, anchor='center')
                wind_dir.place(relx=0.5, rely=0.75, anchor='center')

            elif i == 1:
                image = Image.open('images/feelslike.png')
                image = image.resize((25, 25))
                feelslike_image = ImageTk.PhotoImage(image)

                # Create a Label with both image and text
                square_label = Label(mini_frame, text=' FEELS LIKE', background=self.secondary_color,
                                     font=("Times", 12), foreground=self.tertiary_color,
                                     image=feelslike_image, compound='left')
                feelslike = Label(mini_frame, text=str(round(self.feelslike_c)) + "°", background=self.secondary_color,
                                  font=("Times", 20, "bold italic"), foreground=self.tertiary_color)
                celcius = Label(mini_frame, text="Celcius", background=self.secondary_color,
                                 font=("Times", 15, "bold italic"), foreground=self.tertiary_color)

                # Keep a reference to the PhotoImage object
                square_label.image = feelslike_image

                square_label.place(relx=0.85, rely=0.16, anchor='e')
                feelslike.place(relx=0.5, rely=0.5, anchor='center')
                celcius.place(relx=0.5, rely=0.75, anchor='center')
            elif i == 2:
                image = Image.open('images/haqi.png')
                image = image.resize((25, 25))
                aqi_image = ImageTk.PhotoImage(image)

                # Create a Label with both image and text
                square_label = Label(mini_frame, text=' AIR QUALITY', background=self.secondary_color,
                                     font=("Times", 12), foreground=self.tertiary_color,
                                     image=aqi_image, compound='left')
                aqi = Label(mini_frame, text=self.aqi, background=self.secondary_color,
                                  font=("Times", 20, "bold italic"), foreground=self.tertiary_color)

                levelOfConcern = Label(mini_frame, text=self.levelConcern, background=self.secondary_color,
                            font=("Times", 15, "bold italic"), foreground=self.tertiary_color)

                # Keep a reference to the PhotoImage object
                square_label.image = aqi_image

                square_label.place(relx=0.96, rely=0.16, anchor='e')
                aqi.place(relx=0.5, rely=0.5, anchor='center')
                levelOfConcern.place(relx=0.5, rely=0.75, anchor='center')

    def on_mousewheel(self, event):
        menu_photo = ctk.CTkImage(Image.open('images/more.png'), size=(28, 28))
        map_photo = ctk.CTkImage(Image.open('images/map.png'), size=(35, 35))
        button = ctk.CTkButton(self.main_frame, text=None, image=menu_photo, width=45, height=45,
                               fg_color='transparent',
                               hover_color=self.main_fg_color)
        button.place(relx=0.97, rely=0.95, anchor='e')
        self.canvas.xview_scroll(int(-1 * (event.delta / 100)), "units")

        map_button = ctk.CTkButton(self.main_frame, text=None, image=map_photo, width=45, height=45,
                                   fg_color='transparent',
                                   hover_color=self.main_fg_color)
        map_button.bind('<Button-1>', )  # add the bigger method
        map_button.place(relx=0.18, rely=0.955, anchor='e')

    def update(self):
        self.main_frame.after(5000, self.update)

    def run(self):

        self.update()
        self.canvas.config(scrollregion=[x for x in self.canvas.bbox('all')])
        self.app.mainloop()


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
