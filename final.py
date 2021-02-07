import time
import grovepi
import json
from grovepi import *
from math import isnan
from grove_rgb_lcd import *



# Connect the Grove Light Sensor to analog port A0 Sound sensor to A1
# SIG,NC,VCC,GND
light_sensor = 0
sound_sensor = 1

# Temp / humidity Sensor is attached to port 4
sensor = 4
blue = 0

# Connect the LED to digital ports
# SIG,NC,VCC,GND
# Blue, Green and Red LED's
BLed = 3
GLed = 6
RLed = 5
time.sleep(.1)

# Turn on LED once sensor exceeds threshold resistance
threshold = 300
#sound sensor threshold
threshold_value = 105
# Sensor setup
grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(sound_sensor, "INPUT")
grovepi.pinMode(BLed, "OUTPUT")
grovepi.pinMode(GLed, "OUTPUT")
grovepi.pinMode(RLed, "OUTPUT")

data1 = []

# sleep to avoid NAN errors
time.sleep(0.5)

while True:
# Turns all LEDs off
    def lights():
        grovepi.digitalWrite(GLed, 0)
        grovepi.digitalWrite(BLed, 0)
        grovepi.digitalWrite(RLed, 0)


    try:
        # sleep to avoid NAN
        time.sleep(0.5)
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
        # Read the sound level
        sensor_value1 = grovepi.analogRead(sound_sensor)
        # Calculate resistance of sensor in K
        if sensor_value > 0: # stops dividing by 0 errors
            if sensor_value1 > threshold_value:
                print("sensor_value = %d" % sensor_value)
            
            resistance = float(1023 - sensor_value) * 10 / sensor_value

        # If resistance is greater than threshold turn LEDs off and do not record data else resistance is below threshold and data records
        if resistance > threshold:

            # Send low to switch off LED
            lights()
        # If light is off, turns off and stop recording
        else:
            [temp, humidity] = grovepi.dht(sensor,blue)
            # celsius to fahrenheit conversion
            fahrenheit = (temp * 9/5) + 32
            print(fahrenheit, humidity)
            t = fahrenheit
            h = humidity
            #LCD Display
            print("temp = %.02f F humidity = %.02f%%"%(fahrenheit, humidity)) #Printing to console
            
            # Send HIGH to switch on LED depending on the Temp and humidity
            if fahrenheit > 95:
                grovepi.digitalWrite(RLed, 1)
            elif (fahrenheit > 60.0 and fahrenheit < 85.0) and (humidity < 80.0):
                grovepi.digitalWrite(GLed, 1)
            elif (85 > fahrenheit and fahrenheit < 95) and (humidity < 80):
                grovepi.digitalWrite(BLed, 1)
            elif humidity > 80:
                grovepi.digitalWrite(GLed, 1)
                grovepi.digitalWrite(BLed, 1)
            else:
                print("No Readings!")
            # Sends data to the global array
            data1.append([t, h])
        #Open JSON 
        with open("data1.json", "a") as tfread:
            
            #dump data to JSON file
            json.dump (data1, tfread)

        # Sleeps for 1800 seconds, or 30 minutes
        time.sleep(1800)
        
        
            
     # catch IO Error
    except IOError:
        print("Error")
    #keyboard interrupt to quit program and shut lights off
    except KeyboardInterrupt:
        print("Program Terminated by User!!!") # Takes keyboard interrupt and ends
        # Turns off lights once program stops
        lights()
        
        # Ends program
        break
    


