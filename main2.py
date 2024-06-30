import tkinter as tk
import tkinter
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import customtkinter as ct
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model
from model import scaler
import requests

model = load_model('my_model.h5')
API_KEY = 'pk.eyJ1Ijoic2FjaGluMjAwNSIsImEiOiJjbHcxNWl3ZHcwOHhuMnFtcXZ2dXdoaGJ4In0.sb3rXrdi9oKRjQsL94xCdw'
zoom_level = 18


def input_dialog1():
    global Soil_moisture
    dialog = ct.CTkInputDialog(text="Enter Soil Moisture (%):", title="Soil Moisture")
    Soil_moisture = dialog.get_input()


def input_dialog2():
    global Temperature
    dialog = ct.CTkInputDialog(text="Enter Temperature (C):", title="Temperature")
    Temperature = dialog.get_input()


def input_dialog3():
    global Humidity
    dialog = ct.CTkInputDialog(text="Enter Soil Humidity (%):", title="Soil Humidity")
    Humidity = dialog.get_input()


def recommendations():
    def get_recommendations(soil_moisture, temperature, humidity):
        x = [[soil_moisture, temperature, humidity]]
        X = np.array(x)
        X_norm = scaler.transform(X)
        y_hat = model.predict(X_norm)
        prediction = (y_hat >= 0.5).astype(int)
        if prediction == 1:
            irrigation = "Increase irrigation"
            fertilization = "Use nitrogen-rich fertilizer"
            pest_control = "Check for fungal infections"
        else:
            irrigation = "Irrigation is sufficient"
            fertilization = "Use phosphorus-rich fertilizer"
            pest_control = "No immediate pest control needed"

        return irrigation, fertilization, pest_control

    def on_submit():
        try:
            soil_moisture = float(Soil_moisture)
            temperature = float(Temperature)
            humidity = float(Humidity)

            irrigation, fertilization, pest_control = get_recommendations(soil_moisture, temperature, humidity)

            result_text.set(
                f"Irrigation Status: {irrigation}\nFertilization: {fertilization}\nPest Control: {pest_control}")
            update_plot(soil_moisture, temperature, humidity)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numerical values")
        except NameError as ne:
            messagebox.showerror("NameError", f"NameError occurred: {ne}")
        except TypeError as te:
            messagebox.showerror("TypeError", f"TypeError occurred: {te}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def update_plot(soil_moisture, temperature, humidity):
        try:
            ax.clear()
            ax.bar(['Soil Moisture', 'Temperature', 'Humidity'], [soil_moisture, temperature, humidity],
                   color=['blue', 'red', 'green'], width=0.2)
            ax.set_ylim(0, 100)
            ax.set_ylabel('Value')
            ax.set_title('Sensor Data Overview')
            canvas.draw()
        except Exception as e:
            print(f"Error in update_plot: {e}")
    def quit():
        recommendation_window.destroy()

    recommendation_window = ct.CTkToplevel(root)
    recommendation_window.configure(highlightbackground="#81A263")
    recommendation_window.title("Recommendations")
    recommendation_window.geometry("1000x800")

    frame_input = ct.CTkFrame(recommendation_window, height=300, width=500, corner_radius=5)
    frame_input.grid(row=0, column=2, rowspan=3, padx=(220, 0), pady=10, sticky="nsew")
    frame_input.grid_rowconfigure(3, weight=0)

    label_1 = ct.CTkLabel(frame_input, text="Enter Features",
                          font=ct.CTkFont(family="Helvetica", size=15, weight="bold"))
    label_1.grid(row=0, column=2, padx=10, pady=10)

    input_button1 = ct.CTkButton(frame_input, text="Soil Moisture", font=("Georgia", 18), command=input_dialog1)
    input_button1.grid(row=2, column=1, padx=20, pady=(10, 10))

    input_button2 = ct.CTkButton(frame_input, text="Temperature", font=("Georgia", 18), command=input_dialog2)
    input_button2.grid(row=2, column=2, padx=20, pady=(10, 10))

    input_button3 = ct.CTkButton(frame_input, text="Soil Humidity", font=("Georgia", 18), command=input_dialog3)
    input_button3.grid(row=2, column=3,  padx=20, pady=(10, 10))

    sub = ct.CTkButton(frame_input, text="Submit", font=("Georgia", 18), command=on_submit)
    sub.grid(row=3, column=2, padx=20, pady=20)

    progressbar_1 = ct.CTkProgressBar(recommendation_window, width=10)
    progressbar_1.grid(row=3, column=2, padx=(220, 10), pady=(10, 10), sticky="ew")
    progressbar_1.configure(mode="indeterminate")
    progressbar_1.start()

    frame_graph = ct.CTkFrame(recommendation_window, height=400, width=200, corner_radius=5)
    frame_graph.grid(row=4, column=2, rowspan=5, padx=(220, 0), pady=10, sticky="nsew")
    frame_graph.grid_rowconfigure(5, weight=0)

    fig, ax = plt.subplots(figsize=(5, 3))
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    update_plot(0, 0, 0)

    result_frame = ct.CTkFrame(recommendation_window, height=100, width=500, corner_radius=5)
    result_frame.grid(row=10, column=2, padx=(220, 0), pady=10, sticky="nsew")
    result_text = ct.StringVar()

    result_label = ct.CTkLabel(result_frame, textvariable=result_text, font=("Impact", 16))
    result_label.pack(padx=10, pady=10)

    quit_button = ct.CTkButton(recommendation_window, text="Quit", width=10, font=("Georgia", 18),
                               command=quit)
    quit_button.grid(row=11, column=2, padx=(220,10), pady=20, sticky="n")


def change_appearance(new_appearance: str):
    ct.set_appearance_mode(new_appearance)


def open_image_page():
    def view_map():
        location = location_entry.get()
        latitude = latitude_entry.get()
        longitude = longitude_entry.get()

        if not location or not latitude or not longitude:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            url = f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{longitude},{latitude},{zoom_level},0,0/800x600?access_token={API_KEY}'

            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                with open('satellite_image.png', 'wb') as f:
                    f.write(response.content)

            img = Image.open("satellite_image.png")
            img = img.resize((800, 600), Image.LANCZOS)
            img_photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(image_window, image=img_photo)
            img_label.image = img_photo
            img_label.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load map: {str(e)}")

    image_window = ct.CTkToplevel(root)
    image_window.title("View Map")

    image_window.geometry("600x500")

    ct.CTkLabel(image_window, text="City :",font=("Helvetica", 18)).place(x=150, y=10)
    location_entry = ct.CTkEntry(image_window, width=200)
    location_entry.place(x=200, y=12)

    ct.CTkLabel(image_window,font=("Helvetica", 18), text="Latitude:").place(x=10, y=50)
    latitude_entry = ct.CTkEntry(image_window, width=200)
    latitude_entry.place(x=80, y=52)

    ct.CTkLabel(image_window,font=("Helvetica", 18), text="Longitude:").place(x=300, y=50)
    longitude_entry = ct.CTkEntry(image_window, width=200)
    longitude_entry.place(x=390, y=52)

    map_canvas = ct.CTkLabel(image_window, width=400, height=300,text=" ")
    map_canvas.place(x=50, y=100)

    view_map_button = ct.CTkButton(image_window, text="View Map", font=("Georgia", 18), command=view_map)
    view_map_button.place(x=220, y=300)

    image_window.mainloop()


def suggest_crops():
    month = str(combobox_1.get())
    crops = ["Wheat, Barley, Mustard, Peas",
             "Rice, Groundnut, Jute",
             "Rice, Soybean, Corn, Cotton, Sugarcane, Pulses",
             "Wheat, Barley, Mustard, Potato, Onion"]
    if month in ["January", "February", "March"]:
        messagebox.showinfo(title="Suggested Crops", message=f"{crops[0]} are peak growing crops of {month}")
    elif month in ["April", "May", "June"]:
        messagebox.showinfo(title="Suggested Crops", message=f"{crops[1]} are peak growing crops of {month}")
    elif month in ["July", "August", "September"]:
        messagebox.showinfo(title="Suggested Crops", message=f"{crops[2]} are peak growing crops of {month}")
    elif month in ["October", "November", "December"]:
        messagebox.showinfo(title="Suggested Crops", message=f"{crops[3]} are peak growing crops of {month}")

def exit_all():
    root.quit()


root = ct.CTk()
root.title("Smart Agriculture Monitoring System")
root.geometry("1000x700")

root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

sidebar_frame = ct.CTkFrame(root, width=170, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
sidebar_frame.grid_rowconfigure(10, weight=0)

logo_label = ct.CTkLabel(sidebar_frame, text="AGRISYNC",
                         font=ct.CTkFont(family="Times New Roman", size=20, weight="bold"))
logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

sidebar_button1 = ct.CTkButton(sidebar_frame, font=("Georgia", 18), text="Home")
sidebar_button1.grid(row=1, column=0, padx=20, pady=10)

sidebar_button2 = ct.CTkButton(sidebar_frame, text="Recommendations", font=("Georgia", 18), command=recommendations)
sidebar_button2.grid(row=2, column=0, padx=20, pady=10)

sidebar_button3 = ct.CTkButton(sidebar_frame, font=("Georgia", 18), text="Weather Data")
sidebar_button3.grid(row=3, column=0, padx=20, pady=10)

sidebar_button4 = ct.CTkButton(sidebar_frame, text="Satellite Image", font=("Georgia", 18), command=open_image_page)
sidebar_button4.grid(row=4, column=0, padx=20, pady=10)

emty_label = ct.CTkLabel(sidebar_frame, text=" ")
emty_label.grid(row=5, column=0, padx=20, pady=120)

label = ct.CTkLabel(sidebar_frame, text="Appearance Mode:", font=ct.CTkFont(size=20))
label.grid(row=6, column=0, padx=20, pady=10)

appearance_mode = ct.CTkOptionMenu(sidebar_frame, font=("Georgia", 18), values=["Light", "Dark", "System"],
                                   command=change_appearance)
appearance_mode.grid(row=7, column=0, padx=20, pady=10)

exit_button = ct.CTkButton(sidebar_frame, text="Exit", font=("Georgia", 18), command=exit_all)
exit_button.grid(row=8, column=0, padx=20, pady=10)

textbox = ct.CTkTextbox(root, height=300, font=("Georgia", 18))
textbox.grid(row=0, column=1, padx=(10, 10), pady=(10, 0), sticky="nsew")
textbox.insert(tkinter.END, """
\t\tAGRISYNC: Smart Agriculture Management System

AGRISYNC is an advanced agricultural management application designed to optimize crop and
irrigation cycles by leveraging real-time data and cutting-edge technology.

Soil Moisture: Continuous monitoring of soil moisture levels to ensure optimal irrigation.

Soil Humidity: Detailed analysis of soil humidity to maintain the ideal growing environment for crops.

Temperature: Real-time temperature tracking to adapt farming practices to current conditions.

Satellite Imagery:
Provides up-to-date satellite images of the farmland, helping farmers monitor crop health and growth
patterns over time.

Weather Conditions:
Offers current weather data, including temperature, precipitation, and wind speed, to assist
farmers in making informed decisions about planting, watering, and harvesting.

Recommendations:
Fertilizers: Tailored suggestions for fertilizer application based on soil and crop needs to enhance
growth and yield.

Pesticides: Expert recommendations on pesticide usage to protect crops from pests while
minimizing environmental impact.

With AGRISYNC, farmers can make data-driven decisions to improve productivity, conserve
resources, and achieve sustainable farming practices. Whether you're managing a small farm or a large agricultural operation, AGRISYNC provides the tools
and insights needed to maximize efficiency and crop yield.
""")

month_label = ct.CTkLabel(root, text="\n    Suggestions ✨\n\nSelect Month",
                          font=ct.CTkFont(family="Helvetica", size=18))
month_label.grid(row=1, column=1, padx=(0, 650), pady=(0, 0))
combobox_1 = ct.CTkComboBox(root, values=["January", "February", "March", "April", "May", "June", "July", "August",
                                          "September", "October", "November", "December"])
combobox_1.grid(row=2, column=1, padx=(0, 620), pady=(0, 250))

submit_button = ct.CTkButton(root, text="Suggest Crops", font=("Georgia", 18), command=suggest_crops)
submit_button.grid(row=2, column=1, padx=(0, 620), pady=(0, 150))

api_key = 'a3615c455f40843cb4cc82194e368cd8'
lat = 11.319813
lon = 77.000166
response = requests.get(
    url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
)

data = response.json()
temp = round(data["main"]["temp"] - 273)
feel_like = round(data["main"]["feels_like"] - 273)
weather_label = ct.CTkLabel(root, text=f"Current Temperature: {temp}°C\nFeels like {feel_like}°C",
                            font=ct.CTkFont(size=16))
weather_label.grid(row=2, column=1, padx=(400, 0), pady=(0, 150))

root.mainloop()
