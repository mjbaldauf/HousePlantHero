from gpiozero import MotionSensor
from time import sleep
import json
from datetime import datetime
from threading import Event

### motion_sensor.py

# Define the GPIO pin number for the motion sensor
# GPIO21 is pin 40 on the Raspberry Pi header, which corresponds to BCM GPIO 21
PIR_PIN = 21


# Initialize the motion sensor
motion = MotionSensor(PIR_PIN)


motion_event = Event()  # Event to signal motion detection

# Function to log even if motion is detected
def log_motion_event(file):

    # Create a dictionary to store the motion event data
    event = {
        "motion_detected": "1",
        "timestamp": str(datetime.now())
    }

    # Write the motion event data to a JSON file
    with open(file, "a") as f:  
        f.write(json.dumps(event)+"\n")
    print(f"Motion event logged to {file}")
    print("Motion Detected:", event["timestamp"])

# Fuction to Watch for motion
def start_motion_monitoring():
    # When motion is detected, call the log_motion_event function

    while True:
        
        # wait for motion to be detected
        print("Motion Sensor Active.")
        motion.wait_for_motion()

        # motion_detected 
        motion_event.set()  # Set the event to indicate motion detected

        # wait until motion stops to avoid multiple logs for the same event
        motion.wait_for_no_motion()

        sleep(1)  # Add a small delay to avoid rapid logging



