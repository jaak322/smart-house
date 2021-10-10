from firebase import firebase
import serial
import time
import re


FBConn = firebase.FirebaseApplication('https://smart-house-ae2d9-default-rtdb.europe-west1.firebasedatabase.app/', None)

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    

    if (ser.in_waiting > 0) :
         line = ser.readline()
         
         line1 = line.decode('ASCII')
         line2 = line.decode('ASCII')
         
         
         
         regex = '\d+[T]'
         match1 = re.findall(regex, line1)
         
         regex = '\d+[H]'
         match2 = re.findall(regex, line2)
         
         
         x = "".join(map(str, match1))
         y = "".join(map(str, match2))
         
         
         x1 =int(re.search(r'\d+', x).group(0))
         y1 =int(re.search(r'\d+', y).group(0))
        
        
         
         print(x1)
         print(y1)
         
         
         line22 = FBConn.put("/Sensors","temperature",x1)
         line34 = FBConn.put("/Sensors","humidity",y1)
       
         
         


       
    
        
         
        
        
         
 


