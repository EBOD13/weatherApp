import requests
import customtkinter as ctk
from tkinter import ttk
from CTkListbox import *
from tkinter import *

app = ctk.CTk()
app.geometry("350x653")
# ------------------ COLOR VARIABLES --------------
main_fg_color = "#011f4b"
secondary_color = "#142c5e"
tertiary_color = "#b3cde0"

search_frame = ctk.CTkFrame(app, fg_color="#011f4b", width=app.winfo_screenwidth(), height=app.winfo_screenheight())
search_frame.pack()
search_label = ctk.CTkLabel(search_frame, text='Weather', font=('Times', 35, 'normal'))
search_label.place(anchor='nw', relx=0.05, rely=0.01)
search_box = ctk.CTkEntry(search_frame, width=320, height=28, placeholder_text="Search for a city or airport",
                          font=('Times', 15, 'normal'), fg_color='#142c5e')
search_box.place(anchor='nw', relx=0.05, rely=0.1)

result_frame = ctk.CTkFrame(search_frame, corner_radius=0, width=320, fg_color=secondary_color)


def getSelectedPlace(event):
    if searching_label.curselection() == ():
        pass
    else:
        print(searching_label.get((searching_label.curselection())))



def update():
    global searching_label
    y = -0.38
    search_box.after(500, update)

    API = "AIzaSyCu7nYsBLUrqwYMTohOJFdJD0bCdcCUrlM"
    CITY = search_box.get()
    MAIN_URL = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={CITY}&types=geocode&language=en&key={API}'
    cityResults = []
    responce = requests.get(MAIN_URL).json()

    searching_label = Listbox(result_frame, font=("Times", 16), width=search_box.winfo_width(),
                                      activestyle=NONE, bd=0, fg=tertiary_color, bg=secondary_color, borderwidth=0,
                                      relief=FLAT, highlightthickness=0)

    for i in range(len(responce['predictions'])):
        cityResults.append(responce['predictions'][i]['description'])

        searching_label.insert(i, cityResults[i])

        searching_label.place(relx=0.005, rely=0, anchor='nw',)
        searching_label.bind('<<ListboxSelect>>', getSelectedPlace)

    if len(search_box.get()) > 0:
        result_frame.place(relx=0.06, rely=0.15, anchor='nw', )
        near_city.lower()
    elif len(search_box.get()) == 0:
        search_box.delete(0, END)
        searching_label.after(10, searching_label.destroy())
        result_frame.place_forget()


near_city = ctk.CTkFrame(search_frame, width=320, height=90, corner_radius=25)
near_city.place(anchor='nw', relx=0.05, rely=0.16)

update()
app.mainloop()