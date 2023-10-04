# IC_ESP32

Undergraduate Research guided by João Ari Gualberto Hill, PhD and Daniel Prado de Campos, PhD:
* Building a sEMG data acquisition system with the microcontroller ESP-32 and the
hardware AD8232.
* sEMG signal monitoring in real time with C++/Arduino.
* Python used for data storage on the time domain for better data analysis and transmission
via Bluetooth Classic.

## Description

### Parte1\AcquireSend_ad8232_filtered_2\AcquireSend_ad8232_filtered_2\AcquireSend_ad8232_filtered_2.ino

* Arduino file which will be executed to configure the ESP-32 hardware together with the AD8232 board in a Protoboard.

### Parte1\receivedFile.py

* Python file that generates "Parte1\pot_data.txt".
* It takes the muscle contraction values and adds it to the file above.

### Parte1\plotData.py

* Python file that generates different plots.
* Applies different filters for better data understanding.
* In the end, Root Mean Square (RMS) values were used to avoid negative values for the muscle contractions.

## Getting Started

### Dependencies

* To use the ESP-32, it's necessary to install another driver.
* You can install the Silicon Labs CP210x USB to UART Bridge (COM3) driver following this tutorial: https://www.driverguide.com/driver/download/Silicon-Labs-CP210x-USB-to-UART-Bridge-(COM3)

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Author

Guilherme de Almeida do Carmo - guiialcar@gmail.com
