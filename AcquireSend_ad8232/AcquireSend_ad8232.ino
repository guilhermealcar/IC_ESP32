#include <BluetoothSerial.h>

// Define the pins for the AD8232
const int LO_NEG = 18;
const int LO_POS = 19;
const int ECG_OUT = 4;

BluetoothSerial SerialBT;

// Define the sampling rate
const int SAMPLE_RATE = 1000; // samples per second

void setup() {
  // Initialize the serial port for debugging
  Serial.begin(115200);

  // Initialize the AD8232 pins
  pinMode(LO_NEG, OUTPUT);
  pinMode(LO_POS, OUTPUT);
  pinMode(ECG_OUT, INPUT);

  // Initialize Bluetooth
  SerialBT.begin("ESP32_BT"); // Set the Bluetooth name to "ESP32_BT"
}

void loop() {
  // Turn on the LO_NEG and LO_POS pins
  digitalWrite(LO_NEG, HIGH);
  digitalWrite(LO_POS, HIGH);

  // Wait for a settling time
  delayMicroseconds(1000); // EMG pattern

  // Read the value of the ECG_OUT pin and convert to voltage
  float ecg_voltage = (analogRead(ECG_OUT) / 1023.0) * 3.3 - 1.65;

  // Turn off the LO_NEG and LO_POS pins
  digitalWrite(LO_NEG, LOW);
  digitalWrite(LO_POS, LOW);

  // Wait for the next sample
  delayMicroseconds(1000000 / SAMPLE_RATE);

  // Send the ECG voltage over Bluetooth
  SerialBT.println(ecg_voltage);
  Serial.println(ecg_voltage);
}
