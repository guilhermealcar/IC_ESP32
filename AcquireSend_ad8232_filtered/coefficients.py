from scipy.signal import butter

# Define the sampling frequency
fs = 1000 # Hz

# Define the cutoff frequency
fc = 20 # Hz

# Define the filter order
order = 4

# Calculate the filter coefficients
b, a = butter(order, fc/(fs/2), 'high')

print(b)
print(a)