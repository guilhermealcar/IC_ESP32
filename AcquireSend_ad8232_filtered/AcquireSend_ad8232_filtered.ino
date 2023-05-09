#include <BluetoothSerial.h>

// Define the pins for the AD8232
const int LO_NEG = 18;
const int LO_POS = 19;
const int ECG_OUT = 4;

BluetoothSerial SerialBT;

// Define the sampling rate
const int SAMPLE_RATE = 1000; // samples per second

// Define the filter coefficients
// Filters defined on coefficients.py
float b[] = {0.8484753, -3.39390118, 5.09085177, -3.39390118, 0.8484753};
float a[] = {1.0000000, -3.67172909, 5.06799839, -3.11596693, 0.71991033};

// Define arrays to hold the previous input and output values of the filter
float inputHistory[5] = {0};
float outputHistory[5] = {0};

void setup() {
  // Initialize the serial port for debugging
  Serial.begin(115200);

  // Initialize the AD8232 pins
  pinMode(LO_NEG, OUTPUT);
  pinMode(LO_POS, OUTPUT);
  pinMode(ECG_OUT, INPUT);

  // Initialize Bluetooth
  SerialBT.begin("ESP32_BT"); // Set the Bluetooth name to "ESP32_BT"

  // Initialize filter history arrays to zero
  memset(inputHistory, 0, sizeof(inputHistory));
  memset(outputHistory, 0, sizeof(outputHistory));
}

void loop() {
  // Turn on the LO_NEG and LO_POS pins
  digitalWrite(LO_NEG, HIGH);
  digitalWrite(LO_POS, HIGH);

  // Wait for a settling time
  delayMicroseconds(1000); // EMG pattern

  // Read the value of the ECG_OUT pin and convert to voltage
  float ecg_voltage = (analogRead(ECG_OUT) / 1023.0) * 3.3 - 1.65;

  // Apply highpass filter
  float filtered_voltage = filter(ecg_voltage, b, a, inputHistory, outputHistory);

  // Turn off the LO_NEG and LO_POS pins
  digitalWrite(LO_NEG, LOW);
  digitalWrite(LO_POS, LOW);

  // Wait for the next sample
  delayMicroseconds(1000000 / SAMPLE_RATE);

  // Send the filtered ECG voltage over Bluetooth
  SerialBT.println(filtered_voltage);
  Serial.println(filtered_voltage);
}

// Define the filter function
float filter(float input, float b[], float a[], float inputHistory[], float outputHistory[]) {
  // Update input history
  inputHistory[4] = inputHistory[3];
  inputHistory[3] = inputHistory[2];
  inputHistory[2] = inputHistory[1];
  inputHistory[1] = inputHistory[0];
  inputHistory[0] = input;

  // Update output history
  outputHistory[4] = outputHistory[3];
  outputHistory[3] = outputHistory[2];
  outputHistory[2] = outputHistory[1];
  outputHistory[1] = outputHistory[0];

  // Calculate filtered output
  float output = (b[0] * inputHistory[0] + b[1] * inputHistory[1] + b[2] * inputHistory[2] + b[3] * inputHistory[3] + b[4] * inputHistory[4])
               - (a[1] * outputHistory[1] + a[2] * outputHistory[2] + a[3] * outputHistory[3] + a[4] * outputHistory[4]);

  outputHistory[0] = output;

  return output;
}
