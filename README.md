Python Libraries
  tkinter (usually comes pre-installed with Python)
  matplotlib
  pillow
  numpy
  pandas
  scikit-learn
  tensorflow
  requests

  Ensure you have a valid Mapbox API key. Replace the placeholder 
 Required Files
background.png: Background image for the GUI.
satellite_image.png: This file will be created when the script runs and downloads the satellite image.
my_model.h5: The pre-trained model file. Make sure this file is in the same directory as your script.
model.py: This should contain the scaler object used for normalizing the input features.

Hardware Requirements
  ESP32 or ESP8266 Board
  DHT22 Temperature and Humidity Sensor
  Soil Moisture Sensor
  Connecting Wires
Software Requirements
  MicroPython on the ESP32/ESP8266
  Adafruit_DHT library for the DHT22 sensor
  ADC for the soil moisture sensor
Connecting the Hardware
DHT22 Sensor:

VCC to 3.3V
GND to GND
Data to a digital pin (e.g., GPIO 4)
Soil Moisture Sensor:

VCC to 3.3V
GND to GND
Analog output to an analog pin (e.g., GPIO 34)
