import time
import board
import adafruit_dht

## This File is for testing the DHT11 sensor. 
## It will print the temperature and humidity readings to the console every 5 seconds.

## DHT11 sensor setup
## Declare the DHT11 sensor object, specifying its GPIO Pin.
##The number after the D always matches the BCM GPIO number, not the physical position
# D4 = GPIO4, D14 = GPIO14, etc
dht = adafruit_dht.DHT11(board.D4)

## Function to take temperature and humidity readings from the DHT11 sensor.
def take_temp_humidity_reading():
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        return temperature, humidity
    except RuntimeError as e:
        print(f"Error reading DHT11 sensor: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected DHT11 error: {e}")
        return None, None

# while True:
#     temperature, humidity = take_temp_humidity_reading()

#     if temperature is not None and humidity is not None:
#         print(f"Temperature: {temperature} C, Humidity: {humidity} %")
#     else:
#         print("No valid sensor reading")

    time.sleep(5)    
#     # Call the function to test the DHT11 sensor and print readings to the console.
#     temperature, humidity = take_temp_humidity_reading()
#     print(f"Temperature: {temperature} C, Humidity: {humidity} %")
# except RuntimeError as e:
#     print(f"Error reading DHT11 sensor: {e}")