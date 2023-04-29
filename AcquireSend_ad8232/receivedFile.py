# Não é possível rodar enquanto o Serial Monitor está ativado
# Deve-se fechar o SM para rodar esse código
import serial

ser = serial.Serial('COM3', 115200)
filename = 'pot_data.txt'

with open(filename, 'w') as file:
    while True:
        line = ser.readline().decode().rstrip() # Read a line of a text from the Serial port
        file.write(line + '\n') # Write the line to the text file
        print(line) # Print the line to the console