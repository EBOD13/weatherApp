import json
import math
import random
from tkinter import ttk
import webview
import webbrowser
import re
import tkinter as tk
import customtkinter as ctk
import datetime as dt
import tkintermapview
import geocoder
from PIL import Image, ImageTk
import requests
import pprint
from tkinter.ttk import *
import pandas as pd
from PIL import Image
from datetime import datetime

# ---------------------------- POSITIVE AFFIRMATIONS ----------------------------------

# ----------- Get the current location based on IP address --------------------
geocode = geocoder.ip('me')
if geocode.ok:
    global location_lat, location_long
    location_lat, location_long = geocode.latlng

else:
    print("Unable to retrieve current location.")

# -------------------MAIN URL -------------------------
BASE_URL = "http://api.weatherapi.com/v1/"
API_KEY = "9091497be56f450e942141923232506"

request_url = BASE_URL + "current.json?" + "key=" + API_KEY + "&q=" + str(location_lat) + "," + str(location_long)
response = requests.get(request_url).json()

# --------------------------- API FOR DAILY WEATHER INFORMATION ------------------------
daily_response = requests.get(
    f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q=Norman&days=7').json()
data = daily_response['forecast']['forecastday']

# -------------------------- ALL IMPORTANT VARIABLES -------------------
location_name = response['location']['name']
current_temp_c = response['current']['temp_c']
current_condition = response['current']['condition']['text']
maxtemp_c = daily_response['forecast']['forecastday'][0]['day']['maxtemp_c']
mintemp_c = daily_response['forecast']['forecastday'][0]['day']['mintemp_c']

# -------------------------- Weather information --------------------------

# System Settings
ctk.CTkImage(Image.open("Reg-Screen.png"))
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ----------------------------- The App Frame -------------------------------

app = ctk.CTk()
width, height = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry("350x653")
# app.geometry('%dx%d-9-1' % (width, height))  # Window geometry
app.title("Weather")  # Window title
app.iconbitmap('cloudy.ico')  # Window main icon
# -------------------- Adding UI elements ------------------------
main_fg_color = "#011f4b"
secondary_color = "#142c5e"
tertiary_color = "#b3cde0"
# -------------------- Frame for temperature -------------
main_frame = ctk.CTkFrame(app, height=height, width=width, fg_color=main_fg_color)
main_frame.pack()

location = ctk.CTkLabel(main_frame, text=location_name, font=("Times", 35), text_color="#b3cde0")
location.place(relx=0.5, rely=0.02, anchor=tk.N)

# ---------------------------- ALL THE FRAMES --------------------------------------

temp_frame = ctk.CTkFrame(main_frame, height=190, width=190, corner_radius=150, border_width=8, border_color='#03396c',
                          fg_color=main_fg_color)
temp_frame.place(relx=0.5, rely=0.1, anchor="n")

description_label = ctk.CTkLabel(temp_frame, text=str(current_condition).title(), font=("Times", 18),
                                 text_color="#b3cde0")
description_label.place(relx=0.5, rely=0.2, anchor='center')
# -------------------------------- DAILY TEMPERATURE WITH MAX & MIN --------------------------------------

temperature = ctk.CTkLabel(temp_frame, text=str(int(current_temp_c)) + "°", font=("Times", 70), text_color=tertiary_color)
temperature.place(relx=0.55, rely=0.48, anchor="center")
max_and_min_temp = ctk.CTkLabel(temp_frame, text=f"H: {round(maxtemp_c)}°  L: {round(mintemp_c)}°", font=("Times", 17),
                                text_color=tertiary_color)
max_and_min_temp.place(relx=0.52, rely=0.77, anchor='center')

# --------------------------- EVENT BINDERS FUNCTIONS ---------------------
def bigger(event):
    global done_button
    global gmap

    gmap = tkintermapview.TkinterMapView(main_frame, width=width, height=height)

    gmap.set_position(location_lat, location_long)
    gmap.set_marker(35.1933660, -97.4471577)
    gmap.set_zoom(20)
    # gmap.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
    gmap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    gmap.pack(fill='both', expand=True)
    canvas.place_forget()
    button.place_forget()
    main_frame.configure(fg_color="#0D0D0D")
    done_button = ctk.CTkButton(main_frame, height=30, width=30, text="DONE", fg_color='#0D0D0D', hover_color="#0D0D0D")
    done_button.bind('<Button-1>', smaller)
    done_button.place(relx=0.83, rely=0.01, relwidth=0.15, relheight=0.05, )


def smaller(event):
    main_frame.configure(fg_color=main_fg_color)
    button.place(relx=0.97, rely=0.95, anchor='e')
    done_button.place_forget()
    canvas.place(relx=0.5, rely=0.92, anchor='s', relwidth=0.95)
    gmap.destroy()


dist_x = 0.2
for i in range(3):
    mini_frame = ctk.CTkFrame(main_frame, height=90, width=90, fg_color=secondary_color)
    mini_frame.place(relx=dist_x, rely=0.65, anchor='s')
    dist_x = dist_x + 0.3

    if i == 0:
        add_photo = ctk.CTkImage(Image.open('addbutton.png'), size=(50, 50))

        add_button = ctk.CTkButton(mini_frame, text=None, image=add_photo, width=50, height=50, fg_color='transparent',
                                   hover_color=secondary_color)
        add_button.place(relx=0.5, rely=0.5, anchor='center')


# ------------------------- CREATING MANY FRAMES ------------------------
def on_mousewheel(event):
    canvas.xview_scroll(int(-1 * (event.delta / 100)), "units")


canvas = ctk.CTkCanvas(app, background='red', scrollregion=(0, 0, 100, 500), width=width, height=150, bg=main_fg_color,
                       highlightbackground=main_fg_color)

j = 0

dist_x = 500
while j < 4:

    round_frame = ctk.CTkFrame(canvas, height=120, width=90, fg_color='#03396c', corner_radius=60)
    round_frame.pack(side='right', padx=8)
    canvas.create_window((dist_x, 50), window=round_frame, anchor='nw')
    canvas.place(relx=0.5, rely=0.92, anchor='s', relwidth=0.95)
    dist_x += 125
    round_frame.bind("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ------------------------------ DAY OF THE WEEK FORECAST -------------------------------
    if datetime.today().weekday() == pd.Timestamp(data[j]['date']).day_of_week:
        day_of_week = "NOW"
    else:
        day_of_week = pd.Timestamp(data[j]['date']).day_name()[:3].upper()

    forecast_day = ctk.CTkLabel(round_frame, text=day_of_week, font=("Times", 14), text_color="#b3cde0", )
    forecast_day.place(relx=.5, rely=0.2, anchor='center')

    # -------------------------------------FORECAST TEMPERATURE -----------------------------
    avgtemp_c = round(data[j]['day']['avgtemp_c'])
    forecast_avgtemp_c = ctk.CTkLabel(round_frame, text=str(avgtemp_c), font=("Times", 16), text_color="#b3cde0", )
    forecast_avgtemp_c.place(relx=.5, rely=0.8, anchor='center')

    # ----------------------- ICON INFORMATION & IMAGE ----------------------
    icon_data = data[j]['day']['condition']['icon']
    icon_number = re.findall("/+[day|night]+/+[0-9]+.png$", icon_data)
    icon_number = icon_number[0]
    icon_location = 'weather/64x64' + icon_number
    my_image = ctk.CTkImage(Image.open(icon_location), size=(45, 45))
    image_label = ctk.CTkLabel(round_frame, image=my_image, fg_color="transparent",
                               text="")  # display image with a CTkLabel
    image_label.place(relx=0.5, rely=0.5, anchor='center')
    j += 1



menu_photo = ctk.CTkImage(Image.open('more.png'), size=(28, 28))
map_photo = ctk.CTkImage(Image.open('map.png'), size=(35, 35))

button = ctk.CTkButton(main_frame, text=None, image=menu_photo, width=45, height=45, fg_color='transparent',
                       hover_color=main_fg_color)
button.place(relx=0.97, rely=0.95, anchor='e')

map_button = ctk.CTkButton(main_frame, text=None, image=map_photo, width=45, height=45, fg_color='transparent',
                           hover_color=main_fg_color)
map_button.bind('<Button-1>', bigger)
map_button.place(relx=0.18, rely=0.955, anchor='e')

# ------------------- Main App Loop -----------------

def update():
    main_frame.after(5000, update)


update()
canvas.config(scrollregion=[x for x in canvas.bbox('all')])
app.mainloop()

# ------------------------ WORKING ON GETTING SPECIFIC TEMPERATURE ------------------
