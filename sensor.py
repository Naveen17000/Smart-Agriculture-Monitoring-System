import time
import board
import adafruit_dht

adc_pin = ADC(Pin(34))
adc_pin.atten(ADC.ATTN_11DB)
dht_device = adafruit_dht.DHT22(board.D4)

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        soil_moisture_value = adc_pin.read()

        moisture_percent = (soil_moisture_value / 4095) * 100

        print('Temperature: {:.1f} C'.format(temperature))
        print('Humidity: {:.1f} %'.format(humidity))
        print("Soil Moisture Level: {:.2f}%".format(moisture_percent))

    except RuntimeError as e:
        print('Failed to read sensor:', e)
    sleep_duration = 12 * 3600
    time.sleep(sleep_duration)