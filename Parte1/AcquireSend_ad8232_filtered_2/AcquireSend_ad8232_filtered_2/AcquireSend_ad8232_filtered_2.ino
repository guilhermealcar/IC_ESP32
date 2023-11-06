#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

const int LO_NEG = 18;
const int LO_POS = 19;
const int ECG_OUT = 4;

const int SAMPLE_RATE = 8000; // samples per second
const unsigned long SAMPLE_INTERVAL = 1000000 / SAMPLE_RATE;

const int AD8232_OUT_PIN = 4;
unsigned long lastSampleTime = 0;
float sampleFrequency = 0.0;

void IRAM_ATTR onTimer() {
  // This function is called from an ISR, so keep it as short as possible

  // Check if leads off detection is triggered
  bool leadsOff = (digitalRead(LO_NEG) == 1 || digitalRead(LO_POS) == 1);
  if (leadsOff) {
    Serial.println('!');
    // Handle leads off condition (e.g., set a flag, ignore the sample, etc.)
  } else {
    // Read the value of the ECG_OUT pin and convert to voltage
    int ecg_value = analogRead(ECG_OUT);
    float ecg_voltage = (ecg_value / 1023.0) * 3.3 - 1.65;

    // Send the ECG voltage over Bluetooth
    SerialBT.println(ecg_voltage);
    Serial.println(ecg_voltage);
  }

  // Calculate the sample frequency
  unsigned long currentTime = micros();
  sampleFrequency = 1000000.0 / (currentTime - lastSampleTime);

  Serial.print("Sample Frequency: ");
  Serial.print(sampleFrequency);
  Serial.println(" Hz");

  lastSampleTime = currentTime;
}

hw_timer_t * timer = NULL;

void setup() {
  // Initialize the serial port for debugging
  Serial.begin(115200);

  // Initialize the AD8232 pins
  pinMode(AD8232_OUT_PIN, INPUT);
  pinMode(LO_NEG, INPUT);
  pinMode(LO_POS, INPUT);

  // Initialize Bluetooth
  SerialBT.begin("ESP32_BT");

  // Set up the timer and attach the ISR
  timer = timerBegin(0, 5, true); // Timer 0, prescaler 80
  timerAttachInterrupt(timer, &onTimer, true); // Attach the ISR function
  timerAlarmWrite(timer, SAMPLE_INTERVAL, true); // Set the alarm to trigger at SAMPLE_INTERVAL
  timerAlarmEnable(timer); // Enable the timer alarm
}

void loop() {
  // Your main loop can remain empty, as the sampling is handled by the ISR
}
