#include <IRremote.h>

// Define sensor pin
const int RECV_PIN = 4;

// Define switch pin
const int switchPin = 7;
 
// Define a variable for the button state
int buttonState = 0;
 
// Create IR Send Object
IRsend irsend;
 
 
// Define IR Receiver and Results Objects
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup() {
 
  Serial.begin(9600);
  // Enable the IR Receiver
  irrecv.enableIRIn(); // start the reciever

   // Set Switch pin as Input
  pinMode(switchPin, INPUT);
}

void loop() {
  getRemoteHexCode();
  //displayManufacturerCode();
  //emulateRemote();
}

void getRemoteHexCode() {
 if (irrecv.decode(&results)){
    // Print Code in HEX
        Serial.println(results.value, HEX);
        irrecv.resume();
  }
}

void displayManufacturerCode() {
 if (irrecv.decode(&results)){ // verify that we have indeed received a valid bit of data.
        Serial.println(results.value, HEX);
        switch (results.decode_type){ // decode_type --> related to the manufacturer code (protocol) received
            case NEC: 
              Serial.println("NEC"); 
              break;
            case SONY: 
              Serial.println("SONY"); 
              break;
            case RC5: 
              Serial.println("RC5"); 
              break;
            case RC6: 
              Serial.println("RC6"); 
              break;
            case DISH: 
              Serial.println("DISH"); 
              break;
            case SHARP: 
              Serial.println("SHARP"); 
              break;
            case JVC: 
              Serial.println("JVC"); 
              break;
            // case SANYO: 
            //   Serial.println("SANYO"); 
            //   break;
            // case MITSUBISHI: 
            //   Serial.println("MITSUBISHI"); 
            //   break;
            case SAMSUNG: 
              Serial.println("SAMSUNG"); 
              break;
            case LG: 
              Serial.println("LG"); 
              break;
            case WHYNTER: 
              Serial.println("WHYNTER"); 
              break;
            // case AIWA_RC_T501: 
            //   Serial.println("AIWA_RC_T501"); 
            //   break;
            case PANASONIC: 
              Serial.println("PANASONIC"); 
              break;
            case DENON: 
              Serial.println("DENON"); 
              break;
          default:
            case UNKNOWN: 
              Serial.println("UNKNOWN"); 
              break;
          }
        irrecv.resume();
   }
}

void emulateRemote() {
  // Set button state depending upon switch position
  buttonState = digitalRead(switchPin);
  
  //If button is pressed send power code command
   if (buttonState == HIGH) {
    irsend.sendNEC(0x33FAC573, 32); // LG TV power code in hex   
  }
    
    // Add a small delay before repeating
    delay(300);
}

