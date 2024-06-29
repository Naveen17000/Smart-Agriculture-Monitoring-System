import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow.keras.models import load_model
from model import scaler
import requests

API_KEY = 'Your API key'

longitude = 77.000166 #Replace with your land
latitude = 11.319813 #Replace with your land
zoom_level = 18 #Replace zoom level if needed

url = f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{longitude},{latitude},{zoom_level},0,0/800x600?access_token={API_KEY}'

response = requests.get(url)

if response.status_code == 200:
    with open('satellite_image.png', 'wb') as f:
        f.write(response.content)
        print('Satellite image saved successfully.')
else:
    print('Failed')


model = load_model('my_model.h5')


def get_recommendations(soil_moisture, temperature, humidity):
    x = [[soil_moisture, temperature, humidity]]
    X = np.array(x)
    X_norm = scaler.transform(X)
    y_hat = model.predict(X_norm)
    prediction = (y_hat > 0.5).astype(int)
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
        soil_moisture = float(entry_soil_moisture.get())
        temperature = float(entry_temperature.get())
        humidity = float(entry_humidity.get())

        irrigation, fertilization, pest_control = get_recommendations(soil_moisture, temperature, humidity)

        result_text.set(f"Irrigation: {irrigation}\nFertilization: {fertilization}\nPest Control: {pest_control}")
        update_plot(soil_moisture, temperature, humidity)
        update_history(soil_moisture, temperature, humidity)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numerical values")

def update_plot(soil_moisture, temperature, humidity):
    try:
        ax.clear()
        ax.bar(['Soil Moisture', 'Temperature', 'Humidity'], [soil_moisture, temperature, humidity],
               color=['blue', 'red', 'green'])
        ax.set_ylim(0, 100)
        ax.set_ylabel('Value')
        ax.set_title('Sensor Data Overview')
        canvas.draw()
    except Exception as e:
        print(f"Error in update_plot: {e}")


def update_history(soil_moisture, temperature, humidity):
    tree.insert('', 'end', values=(soil_moisture, temperature, humidity))

def open_image_page():
    image_window = tk.Toplevel(root)
    image_window.title("Image Page")
    image_window.geometry("800x600")

    img = Image.open("satellite_image.png")  # Replace with your image file
    img = img.resize((800, 600), Image.LANCZOS)
    img_photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(image_window, image=img_photo)
    img_label.image = img_photo
    img_label.pack()


def out():
    exit()


root = tk.Tk()
root.title("Smart Agriculture Monitoring System")
root.geometry("1000x800")

# Load and set background image
bg_image = Image.open("background.png")
bg_image = bg_image.resize((1950, 1400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

frame_inputs = tk.Frame(root, bg='lightblue', bd=5)
frame_inputs.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.2, anchor='n')

tk.Label(frame_inputs, text="Soil Moisture (%)", bg='lightblue',
         font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_soil_moisture = tk.Entry(frame_inputs, font=("Arial", 12))
entry_soil_moisture.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_inputs, text="Temperature (°C)", bg='lightblue',
         font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_temperature = tk.Entry(frame_inputs, font=("Arial", 12))
entry_temperature.grid(row=1, column=1, padx=5, pady=5)
tk.Label(frame_inputs, text="Humidity (%)", bg='lightblue',
         font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
entry_humidity = tk.Entry(frame_inputs, font=("Arial", 12))
entry_humidity.grid(row=2, column=1, padx=5, pady=5)
submit_button = tk.Button(frame_inputs, text="Get Recommendations",
                          command=on_submit, bg='lightgreen', font=("Arial", 12))
submit_button.grid(row=3, columnspan=2, pady=10)
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, bg='lightyellow', font=("Arial", 12), bd=5)
result_label.place(relx=0.5, rely=0.35, relwidth=0.8, anchor='n')

fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(relx=0.5, rely=0.45, relwidth=0.8, relheight=0.3, anchor='n')
update_plot(0, 0, 0)

frame_history = tk.Frame(root, bg='lightgrey', bd=5)
frame_history.place(relx=0.5, rely=0.8, relwidth=0.8, relheight=0.15, anchor='n')

tree = ttk.Treeview(frame_history, columns=('Soil Moisture', 'Temperature', 'Humidity'), show='headings')
tree.heading('Soil Moisture', text='Soil Moisture (%)')
tree.heading('Temperature', text='Temperature (°C)')
tree.heading('Humidity', text='Humidity (%)')
tree.pack(fill='both', expand=True)

image_button = tk.Button(root, text="Satellite Image", command=open_image_page, bg='lightblue', font=("Arial", 12))
image_button.pack(side='bottom', pady=5)

exit_button = tk.Button(root, text="Exit", command=root.quit, bg='lightcoral', font=("Arial", 12))
exit_button.pack(side='bottom', pady=10)

root.mainloop()
