#include <BluetoothSerial.h>

// Define the pins for the AD8232
const int LO_NEG = 18;
const int LO_POS = 19;
const int ECG_OUT = 4;

BluetoothSerial SerialBT;

// Define the sampling rate
const int SAMPLE_RATE = 8000; // samples per second

// Define the sample interval
const unsigned long SAMPLE_INTERVAL = 1000000 / SAMPLE_RATE;

// Define variables to check sample rate
const int AD8232_OUT_PIN = 4;
unsigned long lastSampleTime = 0;
float sampleFrequency = 0.0;

void setup() {
  // Initialize the serial port for debugging
  Serial.begin(115200);

  // Initialize the AD8232 pins
  pinMode(AD8232_OUT_PIN, INPUT);
  pinMode(LO_NEG, INPUT);
  pinMode(LO_POS, INPUT);

  // Initialize Bluetooth
  SerialBT.begin("ESP32_BT"); // Set the Bluetooth name to "ESP32_BT"
}

void loop() {
  // Check if enough time has passed for the next sample
  if (micros() - lastSampleTime >= SAMPLE_INTERVAL) {
    lastSampleTime = micros();

    // Check if leads off detection is triggered
    bool leadsOff = (digitalRead(LO_NEG) == 1 || digitalRead(LO_POS) == 1);
    if (leadsOff) {
      Serial.println('!');
      // Handle leads off condition (e.g., set a flag, ignore sample, etc.)
    } else {
      // Read the value of the ECG_OUT pin and convert to voltage
      int ecg_value = analogRead(ECG_OUT);
      float ecg_voltage = (ecg_value / 1023.0) * 3.3 - 1.65;

      // Send the ECG voltage over Bluetooth
      SerialBT.println(ecg_voltage);
      Serial.println(ecg_voltage);
    }

    // Calculate the sample frequency
    unsigned long elapsedTime = micros() - lastSampleTime;
    sampleFrequency = 1000000.0 / elapsedTime;

    Serial.print("Sample Frequency: ");
    Serial.print(sampleFrequency);
    Serial.println(" Hz");

    // Update the last sample time
    lastSampleTime = micros();
  }
}
