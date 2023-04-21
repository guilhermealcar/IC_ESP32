import matplotlib.pyplot as plt

# Open the file and skip the first line
with open('pot_data.txt', 'r') as f:
    f.readline()

    # Counts lines
    count = -1   # -1 to not count the first line

    # Read the remaining lines and plot
    x = []
    y = []
    for line in f:
        count += 1
        x.append(count) # Samples
        values = line.split(',')
        y.append(float(values[0]))  # Values

    plt.plot(x, y)
    plt.show()