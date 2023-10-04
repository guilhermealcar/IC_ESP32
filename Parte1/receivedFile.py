# Not possible to run when Serial Monitor/ Arduino IDE is being used
import serial

ser = serial.Serial('COM3', 115200)
filename = 'pot_data.txt'

y = []

# Read and discard the first line
ser.readline()

counter = 0  # Initialize the counter variable

with open(filename, 'w') as file:
    while True:
        line = ser.readline().decode().rstrip()  # Read a line of text from the Serial port
        if line:  # Check if the line is not empty
            counter += 1  # Increment the counter
            
            if counter >= 10:  # Check if the counter is greater than or equal to 10
                try:
                    value = float(line.split(',')[0])  # Extract the value from the line
                    y.append(value)  # Append the value to the array for plotting
                    file.write(line + '\n')  # Write the line to the text file
                    print(line)  # Print the line to the console
                except ValueError:
                    pass  # Skip the line if it cannot be converted to a float
