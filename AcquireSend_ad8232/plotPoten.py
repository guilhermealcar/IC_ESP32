import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

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

    # Matplotlib
    #plt.plot(x, y)
    #plt.show()

    # Plotly
    df = pd.DataFrame(x,y)
    fig = px.line(df, x, y, title = "Img do plotly")
    fig.update_layout(title='sEMG graph <br><sup>Biceps</sup>',
                      title_x=0.5,
                      xaxis_title='Time',
                      yaxis_title='Voltage')
    fig.show()