import machine
import time
import pycom
import keys
import urequests as requests
from machine import ADC, I2C, Pin, PWM
from onewire import OneWire, DS18X20
from network import WLAN
import ssd1327

import ufirebase as firebase
firebase.setURL("https://smart-house-ae2d9-default-rtdb.europe-west1.firebasedatabase.app/")


#  =================== DECLARATION ================
pycom.heartbeat(False)

# Temperature sensor Declaration
ow = OneWire(Pin('P22'))                    # DS18B20 data line connected to pin P22
temp = DS18X20(ow)


pycom.pybytes_on_boot(True)

# OLED display Declaration
i2c = I2C(0)                                 # create on bus 0
#i2c = I2C(0, pins=('P9','P10'))             # PIN assignments (P9=SDA, P10=SCL)
#display = ssd1327.WS_OLED_128X128(i2c)      # Grove OLED Display
display = ssd1327.SH1107_I2C(128, 128, i2c)  # Width and height of the display
display.fill(0)                              # '0' for BLACK & '1' for WHITE
#display.invert(1)


# Buzzer Declaration

A6 = 1760                                  # define frequency for each tone
AS6 = 1865
B6 = 1976
E6 = 1319
G6 = 1568
A7 = 3520
C7 = 2093
D7 = 2349
E7 = 2637
F7 = 2794
G7 = 3136

buzzer_pin = Pin("P8")                       # set up pin PWM timer for output to buzzer
pwm = PWM(0, frequency=300)
pwm_channel = pwm.channel(2, duty_cycle = 0, pin=buzzer_pin)

TOKEN = keys.token                           # Put your ubidots TOKEN here
DELAY = 1                                    # Delay in seconds

# pH sensor Declaration
adc = machine.ADC(bits=10)                   # ADC (Analogue to Digital Conversion)
apin = adc.channel(pin='P16')                # create an analog pin on P16 for pH sensor
bpin = adc.channel(pin='P18')                # create an analog pin on P16 for temp sensor


# WiFi Declaration
wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.INT_ANT)
#print(wlan.scan())

# Assign your own Wi-Fi credentials (SSID and Password) here
wlan.connect(keys.wifi_ssid, auth=(WLAN.WPA2, keys.wifi_password))

while not wlan.isconnected():
    machine.idle()
print("Connected to Wifi\n")



#  ===================IMPLEMENTATION================
# Plays the Super Mario melody
def play_tune():
    super_mario_tone = [E7, E7, 0, E7, 0, C7, E7, 0, G7, 0, 0, 0, G6, 0, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0,
                        AS6, A6, 0, G6, E7, 0, G7, A7,0, F7, G7, 0, E7, 0, C7, D7, B6, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0,
                        A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0, C7, D7, B6, 0, 0]
    for i in super_mario_tone:
        if i == 0:
            pwm_channel.duty_cycle(0)
        else:
            pwm = PWM(0, frequency = i)        # changes frequency to change tone
            pwm_channel.duty_cycle(0.50)
        time.sleep(0.150)



# Sends data to PyBytes
def send_data_to_pybytes(pH, temperature, celsius):
    pybytes.send_signal(1, pH)
    pybytes.send_signal(2, temperature)
    pybytes.send_signal(3, celsius)
    time.sleep(DELAY)


# Builds the JSON-object to send the POST HTTP request
def build_json(variable1, value1, variable2, value2, variable3, value3):
    try:
        lat = 56.029394
        lng = 14.156678
        data = {variable1: {"value": value1},
                variable2: {"value": value2, "context": {"lat": lat, "lng": lng}},
                variable3: {"value": value3}}
        return data
    except:
        return None


# Sends the POST HTTP request. Please refer the REST API reference https://ubidots.com/docs/api/
def sending_data_to_ubidots(device, value1, value2, value3):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json("temperature", value1, "position", value2, "pH", value3)
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass

# =================== MAIN ===================

while True:

    millivolts = apin.voltage()             # Reads the voltage in mV
    mvolt = bpin.voltage()
    celsius = (mvolt - 500.0) / 10.0
    print(millivolts)
    print(mvolt)
    print(celsius)

    print("Room Temperature reading: {}".format(celsius))
    time.sleep(1)
    # Data values
    pH = millivolts / 1024 * 5 * 1.45       # Calculates the pH
    #pH = -2.5440366428206*10**(-12)*mvolt**4+1.0717620652870*10**(-8)*mvolt**3-0.0000163809*mvolt**2+0.0136789*mvolt-0.332595   #Newton's interpolation
    print(pH)
    print("pH probe reading: {}".format(pH))
    time.sleep(5)
    temp.start_conversion()                 # Start the temp conversion on one DS18x20 device
    time.sleep(DELAY)
    temperature = temp.read_temp_async()    # Read the temperature of one DS18x20 device if the conversion is complete, otherwise return None.
    while temperature is None:
        temperature = temp.read_temp_async()
    print("Temperature probe reading: {}".format(temperature))

    display.text('pH: ' + str(pH), 0, 10, 255)
    display.show()                          # Displays pH value to the OLED Screen
    display.text('Aqua temp: ' + str(temperature) + ' C', 0, 30, 255)
    display.show()                          # Displays temp value to the OLED Screen
    display.text('Room temp: ' + str(celsius) + ' C', 0, 50, 255)
    display.show()

    # This will signal whether the aquarium is within the ideal range or not
    if (pH < 8 and pH > 6) and (temperature < 29 and temperature > 23):
        print("The aquarium is in ideal condition!")
        display.text("The aquarium ", 10, 80, 255)
        display.show()
        display.text("is in optimal ", 10, 90, 255)
        display.show()
        display.text("condition!!", 20, 100, 255)
        display.show()
        #display.invert(true)
        pycom.rgbled(0x00FF00)               # pycom's built-in LED device will emit GREEN light

    else:
        print("The aquarium is not within the optimal range!")
        display.text("The aquarium is ", 0, 80, 255)
        display.show()
        display.text("not within the ", 5, 90, 255)
        display.show()
        display.text("optimal range!", 5, 100, 255)
        display.show()
        pycom.rgbled(0xFF0000)               # pycom's built-in LED device will emit RED light
        play_tune()                          # plays the super mario melody to alert the user

    send_data_to_pybytes(pH, temperature, celsius)    # sends data to pybytes
    print("send_data_to_pybytes")

    sending_data_to_ubidots("pycom", temperature, 1, pH)   # sends data to ubidots
    print("sending_data_to_ubidots")

    firebase.put("Sensors", {"pH": pH, "aquarium temperature": temperature, "room temperature":celsius})  # sends data to firebase
    #firebase.addto("testsensor", {"pH": pH, "aquarium temperature": temperature, "room temperature":celsius})
    print("sending data to firebase")

    time.sleep(60)
