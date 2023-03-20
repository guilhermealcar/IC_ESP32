//This example creates a bridge between Serial and Classical Bluetooth (SPP)
//and also demonstrate analog values of a potentiometer

#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
uint8_t byteArray[2];
//int byteArray[2];

const int potPin = 34; //GPIO 34 (D34 on ESP32)

int analogValue = 0; // variable for storing potentiometer value
char analogWord;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
}

void loop() {
  analogValue = analogRead(potPin); //Reading value received from the potentiometer medium pin 

  //byteArray[0] = highByte(analogValue);
  //byteArray[1] = lowByte(analogValue);

  //analogWord = word(byteArray[0], byteArray[1]);

  if (Serial.available()) {
    SerialBT.write(Serial.read());
    //SerialBT.write(analogValue);
    //SerialBT.write(analogWord);
    //SerialBT.print(analogValue);
  }
  if (SerialBT.available()) {
    Serial.write(SerialBT.read());
    //Serial.write(analogValue);
    //Serial.print(analogValue);
  }
  //Serial.write(analogWord);
  
  SerialBT.println(analogValue);  //Show value on cellphone
  Serial.println(analogValue);  //Show value on PC
  delay(1000);
}