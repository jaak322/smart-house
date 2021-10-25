# boot.py -- run on boot-up
import machine
import os
import keys
from network import WLAN

uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('main.py')

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
   if net.ssid ==  keys.wifi_ssid:
       print('Network found!')
       wlan.connect(net.ssid, auth=(net.sec, keys.wifi_password), timeout=5000)
       while not wlan.isconnected():
           machine.idle() # save power while waiting
       print('WLAN connection succeeded!')
       print(wlan.ifconfig())
       break
