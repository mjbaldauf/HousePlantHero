from soil_monitor import read_soil_moisture
from climate_monitor import take_temp_humidity_reading
import motion_sensor
from time import sleep, time, ctime
import threading
import json
from mqtt_client import MQTTPublisher
import toy_data
import traffic_light
import send_notification

### main.py

##InfluxDB API Key and URL
# INFLUXDB_URL = "http://localhost:8086"
#  INFLUXDB_TOKEN = 
# y3Fl5CO-A3ikiLlu2SolFlW-t0IEyqq5rUmy4laLRjVZOVYkf4bx2-orNTjCsq8X94rOFCqSsrSYXeJfWf8_qw==


# Initialize the MQTT publisher
publisher = MQTTPublisher()
## MQTT Topics

# File Paths
MOTION_LOG = "/home/mb/FinalProject/motion_log.json" 
CLIMATE_LOG = "/home/mb/FinalProject/climate_log.json"

MOTION_TOY = "/home/mb/FinalProject/motion_toy.json"  # Path to the motion toy log file
CLIMATE_TOY = "/home/mb/FinalProject/climate_toy.json"  # Path to the climate toy log file
SOIL_MOISTURE_THRESHOLD = 30  # Threshold for soil moisture alert
SOIL_MOISTURE_WARNING = 40  # Warning level for soil moisture

# Variables to track the last time the sensors were read
last_sensor_read = 0  # Initialize to 0 to ensure the first reading occurs immediately
last_motion_publish = 0  # Initialize to 0 to ensure the first motion event is published immediately
sensor_interval = 3600  # 1 hour in seconds

climate_info = {} # empty dictionary to store plant info

# Start up motion detector and run it in a separate thread
motion_thread = threading.Thread(
    target=motion_sensor.start_motion_monitoring,
    daemon=True)    
motion_thread.start()

def write_plant_info_to_json(plant_info, file=CLIMATE_LOG):
    with open(file, "a") as f:
        f.write(json.dumps(plant_info)+"\n")
    print(f"Plant info logged to {file}")

## check if the motion sensor has detected motion, log it to a file, and publish it to the MQTT topic 
def check_motion():
    global last_motion_publish
    
    if motion_sensor.motion_event.is_set():
        print("Motion detected! Logging to file and publishing to MQTT topic.")
        motion_sensor.log_motion_event(MOTION_LOG)
        motion_sensor.motion_event.clear()
        publisher.publish("soil_monitor/motion", 1)



def check_climate(climate_info=climate_info):

    # if time() - last_sensor_read >= sensor_interval:
    print("Reading soil moisture, temperature, and humidity...\n")
    soil_moisture = read_soil_moisture()

        ## Notification if soil moisture is below threshold
    if  soil_moisture < SOIL_MOISTURE_THRESHOLD:
        send_notification.send_email(
            "m.baldauf@live.com",
            "Low Soil Moisture Alert",
            f"Soil moisture is low: {soil_moisture}")
        send_notification.send_sms(
            "575-405-6141",
            "verizon",
            f"Soil moisture is low: {soil_moisture}")
        traffic_light.red_light()  # Turn on red light for low soil moisture
        led_status = 0
    elif soil_moisture < SOIL_MOISTURE_WARNING:
        traffic_light.yellow_light()  # Turn on yellow light for warning level soil moisture
        led_status = 1
    else:
        traffic_light.green_light()  # Turn on green light for healthy soil moisture
        led_status = 2

    #publish led status to MQTT topic
    publisher.publish("soil_monitor/led_status", led_status)
    ## Read temperature and humidity from the DHT11 sensor
    temp, humidity = take_temp_humidity_reading()
    timestamp = time()

    # Update the climate_info dictionary with the latest readings
    climate_info.update({
        "soil": soil_moisture,
        "temperature": temp,
        "humidity": humidity,
        "timestamp": str(timestamp),
        "Reading taken at: ": str(ctime(timestamp))
    })

    # Publish the plant info to the MQTT topic
    publisher.publish("soil_monitor/soil", climate_info["soil"])
    print(f"Published soil info to MQTT topic 'soil_monitor/soil': {climate_info['soil']}")

    publisher.publish("soil_monitor/temperature", climate_info["temperature"])
    print(f"Published temperature info to MQTT topic 'soil_monitor/temperature': {climate_info['temperature']}")
    
    publisher.publish("soil_monitor/humidity", climate_info["humidity"])
    print(f"Published humidity info to MQTT topic 'soil_monitor/humidity': {climate_info['humidity']}")
    
    return time() # Update the last sensor read time
  

# toy_data.publish_toy_soil_values()  # Publish toy soil moisture values to MQTT topic     

## Main Loop
while True:

    # Check if motion was detected
    check_motion()

    # Check if it's time to read the sensors (Once every hour)
    # Call the function to check climate and publish data if needed
    # check_climate() returns None if it's not time to read the sensors, 
    # last_sensor_read value remains unchanged in that case.
    last_sensor_read = check_climate() or last_sensor_read
     ## write the data to a json file
    write_plant_info_to_json(climate_info, CLIMATE_LOG)


    sleep(10)  # Delay between readings

 




