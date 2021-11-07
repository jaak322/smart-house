from firebase import firebase
import serial
import time
import re
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)


time.sleep(5)

GPIO.cleanup

FBConn = firebase.FirebaseApplication('https://smart-house-ae2d9-default-rtdb.europe-west1.firebasedatabase.app/', None)

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    

    if (ser.in_waiting > 0) :
         line = ser.readline()
         
         line1 = line.decode('ASCII')
         line2 = line.decode('ASCII')
         line3 = line.decode('ASCII')
         
         
         
         regex = '\d+[T]'
         match1 = re.findall(regex, line1)
         
         regex = '\d+[H]'
         match2 = re.findall(regex, line2)
         
         regex = '\d+[L]'
         match3 = re.findall(regex, line3)         
         
         
         x = "".join(map(str, match1))
         y = "".join(map(str, match2))
         z = "".join(map(str, match3))
         
         
         x1 =int(re.search(r'\d+', x).group(0))
         y1 =int(re.search(r'\d+', y).group(0))
         z1 =int(re.search(r'\d+', z).group(0))
        
        
         
        
         
         line22 = FBConn.put("/Sensors","temperature",x1)
         line34 = FBConn.put("/Sensors","humidity",y1)
         line35 = FBConn.put("/Sensors","outdoor light",z1)
         result = FBConn.get("/Lamps","lamp1",)
         
         if (result ==1):
              print(result)
              GPIO.output(18, GPIO.HIGH)
         elif (result ==0):
              print(result)
              GPIO.output(18, GPIO.LOW)
         


       
    
        
         
        
        
         
 



