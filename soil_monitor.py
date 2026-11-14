import time
from smbus2 import SMBus

# Soil Moisture Sensor Calibration Values
# Medium    	Moisture Value
# Air	            22.2
# Dry Soil	        22.8
# Damp Soil	        53.5
# Wet Soil	        95.5
# Saturated Soil	
# Water	            90

ADDRESS = 0x48
bus = SMBus(1)


def soil_moisture_percent(adc_value):
    # Calibration points
    DRY = 25
    SATURATED = 100

    # Convert ADC reading to percentage
    moisture = ((adc_value - DRY) / (SATURATED - DRY)) * 100
    if moisture < DRY:
        moisture = 25
    elif moisture > 100:
        moisture = 100

    return round(moisture, 1)

def read_soil_moisture():

    # turn sensor power on here
    bus.write_byte_data(0x48, 0x40, 0x01) 

    # throw away startup readings
    for i in range(3):
        bus.read_byte_data(0x48, 0x40)
        time.sleep(0.05)

    readings = []

    # real measurements
    for i in range(10):
        readings.append(bus.read_byte_data(0x48, 0x40))
        time.sleep(0.1)

    # turn sensor power off here
    bus.write_byte_data(0x48, 0x40, 0x00)

    soil_moisture = sum(readings) / len(readings)
    soil_moisture = soil_moisture_percent(soil_moisture)
    
    return soil_moisture


moisture = read_soil_moisture()