#%%
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import signal
from scipy.signal import find_peaks, peak_widths
import pywt

#%%

# Open the file and skip the first line
with open(r'C:\Users\guiia\OneDrive\Documentos\IC_4\Parte1\pot_data.txt', 'r') as f:
    f.readline()

    # Counts lines
    count = -1   # -1 to not count the first line

    # Read the remaining lines and plot
    x = []
    y = []
    for line in f:
        count += 1
        values = line.split(',')
        y.append(float(values[0]))  # Values

    # Plotly
    x = np.arange(len(y))
    df = pd.DataFrame({'Samples': x, 'Voltage': y})
    fig = px.line(df, x='Samples', y='Voltage', title='sEMG graph <br><sup>Biceps</sup>')
    fig.update_layout(title_x=0.5, xaxis_title='Samples', yaxis_title='Voltage')
    fig.show()

    # PLOT THE FFT OF THE SIGNAL
    # Perform FFT
    y_fft = np.fft.fft(y)

    # Frequencies corresponding to the FFT coefficients
    sampling_rate = 1000   # Assuming the x-axis is in units of seconds
    frequencies = np.fft.fftfreq(len(y), d=1 / sampling_rate)

    # Plot the FFT magnitude spectrum

    # Plotly
    fft_df = pd.DataFrame({'Frequency': frequencies, 'Magnitude': np.abs(y_fft)})
    fig = px.line(fft_df, x='Frequency', y='Magnitude', title='FFT')
    fig.update_layout(title_x=0.5, xaxis_title='Frequency', yaxis_title='Magnitude')
    fig.show()

    # APPLY NOTCH FILTER TO 50 Hz
    notch_freq = 50  # Frequency to be rejected = 50Hz
    sampling_rate = 1000   # Assuming the x axis is in units of samples

    normalized_notch_freq = notch_freq / (sampling_rate / 2)  # Normalize the notch frequency

    if 0 < normalized_notch_freq < 1:
        Q = 30  # Quality factor

        b, a = signal.iirnotch(normalized_notch_freq, Q)
        y_notch = signal.lfilter(b, a, y)

        # Plotly
        df_notch = pd.DataFrame({'Samples': x, 'Voltage': y_notch})
        fig = px.line(df_notch, x='Samples', y='Voltage', title='Filtered Signal')
        fig.update_layout(title='sEMG graph <br><sup>Notch Filter</sup>', title_x=0.5, xaxis_title='Samples', yaxis_title='Voltage')
        fig.show()
    else:
        print("Normalized notch frequency is out of range.")

    # APPLY NOTCH FILTER TO 50 Hz
    notch_freq = 50  # Frequency to be rejected = 50Hz
    sampling_rate = 2000   # Assuming the x axis is in units of samples

    normalized_notch_freq = notch_freq / (sampling_rate / 2)  # Normalize the notch frequency

    if 0 < normalized_notch_freq < 1:
        Q = 30  # Quality factor

        b, a = signal.iirnotch(normalized_notch_freq, Q)
        y_notch = signal.lfilter(b, a, y)

        # Plotly
        df_notch = pd.DataFrame({'Samples': x, 'Voltage': y_notch})
        fig = px.line(df_notch, x='Samples', y='Voltage', title='Filtered Signal')
        fig.add_annotation(text='2kHz Sample Rate', xref='paper', yref='paper', x=0.5, y=1.05, showarrow=False)
        fig.update_layout(title='sEMG graph <br><sup>Notch Filter</sup>', title_x=0.5, xaxis_title='Samples', yaxis_title='Voltage')
        fig.show()
    else:
        print("Normalized notch frequency is out of range.")

    # APPLY BAND PASS FILTER
    lowcut = 20     # Lower cutoff frequency
    highcut = 450   # Upper cutoff frequency
    nyquist_freq = 0.5 * sampling_rate
    normalized_lowcut = lowcut / nyquist_freq
    normalized_highcut = highcut / nyquist_freq

    if 0 < normalized_lowcut < 1 and 0 < normalized_highcut < 1:
        b, a = signal.butter(2, [normalized_lowcut, normalized_highcut], btype='band')
        y_bandpass = signal.lfilter(b, a, y)

        # Update x after filtering
        x_bandpass = np.arange(len(y_bandpass))

        # Plotly
        df_bandpass = pd.DataFrame({'Samples': x_bandpass, 'Voltage': y_bandpass})
        fig = px.line(df_bandpass, x='Samples', y='Voltage', title='Filtered Signal')
        fig.update_layout(title='sEMG graph <br><sup>Bandpass Filter</sup>', title_x=0.5, xaxis_title='Samples', yaxis_title='Voltage')
        fig.show()
    else:
        print("Normalized cutoff frequencies are out of range.")

    # APPLY SPIKE FILTER
    # Denoise the signal using wavelet denoising
    wavelet = 'db4'  # Choose the wavelet type
    level = 5  # Wavelet decomposition level
    threshold = 0.1  # Threshold for wavelet coefficients
    coeffs = pywt.wavedec(y_bandpass, wavelet, level=level)
    coeffs_thresh = [pywt.threshold(c, threshold * max(c)) for c in coeffs]
    y_denoised = pywt.waverec(coeffs_thresh, wavelet)

    # Apply median filtering to remove remaining spikes
    window_size = 5
    y_median_filtered = signal.medfilt(y_denoised, kernel_size=window_size)

    # Create the subplots
    fig = sp.make_subplots(rows=4, cols=1, subplot_titles=('Original Bandpass Signal', 'Denoised Signal', 'Median Filtered Signal', 'Wavelet Coefficients'))

    # Add the original signal trace
    fig.add_trace(go.Scatter(x=np.arange(len(y_bandpass)), y=y_bandpass, name='Original Bandpass Signal'), row=1, col=1)

    # Add the denoised signal trace
    fig.add_trace(go.Scatter(x=np.arange(len(y_denoised)), y=y_denoised, name='Denoised Signal'), row=2, col=1)

    # Add the median filtered signal trace
    fig.add_trace(go.Scatter(x=np.arange(len(y_median_filtered)), y=y_median_filtered, name='Median Filtered Signal'), row=3, col=1)

    # Add the wavelet coefficients trace
    fig.add_trace(go.Heatmap(z=coeffs_thresh, coloraxis='coloraxis'), row=4, col=1)

    # Update layout
    fig.update_layout(height=1000, width=800, showlegend=False, title='Wavelet Denoising and Coefficients')
    fig.update_yaxes(title_text='Voltage', row=1, col=1)
    fig.update_yaxes(title_text='Voltage', row=2, col=1)
    fig.update_yaxes(title_text='Voltage', row=3, col=1)
    fig.update_xaxes(title_text='Samples', row=3, col=1)
    fig.update_yaxes(title_text='Level', row=4, col=1)
    fig.update_xaxes(title_text='Coefficient Index', row=4, col=1)

    # Show the figure
    fig.show()

    # PLOT THE FFT OF THE SIGNAL MEDIAN FILTERED
    # Perform FFT
    y_median_filtered_fft = np.fft.fft(y_median_filtered)

    # Frequencies corresponding to the FFT coefficients
    sampling_rate = 2000   # Assuming the x-axis is in units of seconds
    frequencies_median_filtered = np.fft.fftfreq(len(y_median_filtered), d=1 / sampling_rate)

    # Plot the FFT magnitude spectrum

    # Plotly
    fft_df = pd.DataFrame({'Frequency': frequencies_median_filtered, 'Magnitude': np.abs(y_median_filtered_fft)})
    fig = px.line(fft_df, x='Frequency', y='Magnitude', title='FFT')
    fig.update_layout(title_x=0.5, xaxis_title='Frequency', yaxis_title='Magnitude')
    fig.show()

    # Extract the RMS from signal
    rms = np.sqrt(np.mean(np.square(y_median_filtered)))
    print("RMS value: ", rms)

    # RMS for a window size of 50 samples 
    window_size = 50 
    num_windows = len(y_median_filtered) // window_size

    rms_values = []

    for i in range(num_windows):
        start_index = i * window_size
        end_index = start_index + window_size
        window = y_median_filtered[start_index:end_index]

        rms = np.sqrt(np.mean(np.square(window)))
        rms_values.append(rms)

    print("RMS values for each 50 samples: ", rms_values)

    # Plot the RMS values
    x_rms = np.arange(0, num_windows) * window_size
    df_rms = pd.DataFrame({'Samples': x_rms, 'RMS': rms_values})
    fig = px.line(df_rms, x='Samples', y='RMS', title='RMS Values')
    fig.update_layout(title='RMS Values <br><sup>Window size = 50 samples</sup></br>', title_x=0.5, xaxis_title='Samples', yaxis_title='RMS')
    fig.show()

    # Create the subplots
    fig = sp.make_subplots(rows=2, cols=1, subplot_titles=('Median Filtered Signal', 'RMS Graph'))

    # Add the median filtered signal trace
    fig.add_trace(go.Scatter(x=np.arange(len(y_median_filtered)), y=y_median_filtered, name='Median Filtered Signal'), row=1, col=1)

    # Add the RMS graph trace
    fig.add_trace(go.Scatter(x=x_rms, y=rms_values, name='RMS'), row=2, col=1)

    # Update layout
    fig.update_layout(height=800, width=800, showlegend=False, title='Median Filtered Signal and RMS Graph<br><sup>Window size = 50 samples</>')
    fig.update_yaxes(title_text='Voltage', row=1, col=1)
    fig.update_yaxes(title_text='RMS', row=2, col=1)
    fig.update_xaxes(title_text='Samples', row=2, col=1)

    # Show the figure
    fig.show()

    # Create a new figure
    fig = go.Figure()

    # Add trace for the median filtered signal
    fig.add_trace(go.Scatter(x=np.arange(len(y_median_filtered)), y=y_median_filtered, name='Median Filtered Signal'))

    # Add trace for the RMS graph
    fig.add_trace(go.Scatter(x=x_rms, y=rms_values, name='RMS'))

    # Update layout
    fig.update_layout(title='Median Filtered Signal and RMS Graph', xaxis_title='Samples', yaxis_title='Voltage')

    # Show the figure
    fig.show()

    ### RMS for a window size of 10 samples 
    window_size = 10 
    num_windows = len(y_median_filtered) // window_size

    rms_values = []

    for i in range(num_windows):
        start_index = i * window_size
        end_index = start_index + window_size
        window = y_median_filtered[start_index:end_index]

        rms = np.sqrt(np.mean(np.square(window)))
        rms_values.append(rms)

    print("RMS values for each 50 samples: ", rms_values)

    # Plot the RMS values
    x_rms = np.arange(0, num_windows) * window_size
    df_rms = pd.DataFrame({'Samples': x_rms, 'RMS': rms_values})
    fig = px.line(df_rms, x='Samples', y='RMS', title='RMS Values')
    fig.update_layout(title='RMS Values <br><sup>Window size = 10 samples</sup></br>', title_x=0.5, xaxis_title='Samples', yaxis_title='RMS')
    fig.show()

    # Create the subplots
    fig = sp.make_subplots(rows=2, cols=1, subplot_titles=('Median Filtered Signal', 'RMS Graph'))

    # Add the median filtered signal trace
    fig.add_trace(go.Scatter(x=np.arange(len(y_median_filtered)), y=y_median_filtered, name='Median Filtered Signal'), row=1, col=1)

    # Add the RMS graph trace
    fig.add_trace(go.Scatter(x=x_rms, y=rms_values, name='RMS'), row=2, col=1)

    # Update layout
    fig.update_layout(height=800, width=800, showlegend=False, title='Median Filtered Signal and RMS Graph<br><sup>Window size = 10 samples</>')
    fig.update_yaxes(title_text='Voltage', row=1, col=1)
    fig.update_yaxes(title_text='RMS', row=2, col=1)
    fig.update_xaxes(title_text='Samples', row=2, col=1)

    # Show the figure
    fig.show()

    # Create a new figure
    fig = go.Figure()

    # Add trace for the median filtered signal
    fig.add_trace(go.Scatter(x=np.arange(len(y_median_filtered)), y=y_median_filtered, name='Median Filtered Signal'))

    # Add trace for the RMS graph
    fig.add_trace(go.Scatter(x=x_rms, y=rms_values, name='RMS'))

    # Update layout
    fig.update_layout(title='Median Filtered Signal and RMS Graph', xaxis_title='Samples', yaxis_title='Voltage')

    # Show the figure
    fig.show()


# %%
    # PLOT THE FFT OF THE SIGNAL MEDIAN FILTERED
    # Perform FFT
    y_median_filtered_fft = np.fft.fft(y_median_filtered)

    # Frequencies corresponding to the FFT coefficients
    sampling_rate = 2000   # Assuming the x-axis is in units of seconds
    frequencies_median_filtered = np.fft.fftfreq(len(y_median_filtered), d=1 / sampling_rate)

    # Plot the FFT magnitude spectrum
    # Plotly
    fft_df = pd.DataFrame({'Frequency': frequencies_median_filtered, 'Magnitude': np.abs(y_median_filtered_fft)})
    fig = px.line(fft_df, x='Frequency', y='Magnitude', title='FFT')
    fig.update_layout(title_x=0.5, xaxis_title='Frequency', yaxis_title='Magnitude')
    fig.show()

    # APPLY BAND PASS FILTER
    lowcut = 10     # Lower cutoff frequency
    highcut = 350   # Upper cutoff frequency
    nyquist_freq = 0.5 * sampling_rate
    normalized_lowcut = lowcut / nyquist_freq
    normalized_highcut = highcut / nyquist_freq

    if 0 < normalized_lowcut < 1 and 0 < normalized_highcut < 1:
        b, a = signal.butter(2, [normalized_lowcut, normalized_highcut], btype='band')
        y_mf_bandpass = signal.lfilter(b, a, y_median_filtered)

        # Update x after filtering
        x_bandpass = np.arange(len(y_mf_bandpass))

        # Plotly
        df_bandpass = pd.DataFrame({'Samples': x_bandpass, 'Voltage': y_mf_bandpass})
        fig = px.line(df_bandpass, x='Samples', y='Voltage', title='Filtered Signal')
        fig.update_layout(title='sEMG graph <br><sup>Bandpass Filter</sup>', title_x=0.5, xaxis_title='Samples', yaxis_title='Voltage')
        fig.show()
    else:
        print("Normalized cutoff frequencies are out of range.")

    # PLOT THE FFT OF THE SIGNAL MEDIAN FILTERED
    # Perform FFT
    y_median_filtered_fft = np.fft.fft(y_mf_bandpass)

    # Frequencies corresponding to the FFT coefficients
    sampling_rate = 2000   # Assuming the x-axis is in units of seconds
    frequencies_median_filtered = np.fft.fftfreq(len(y_mf_bandpass), d=1 / sampling_rate)

    # Plot the FFT magnitude spectrum
    # Plotly
    fft_df = pd.DataFrame({'Frequency': frequencies_median_filtered, 'Magnitude': np.abs(y_median_filtered_fft)})
    fig = px.line(fft_df, x='Frequency', y='Magnitude', title='FFT')
    fig.update_layout(title_x=0.5, xaxis_title='Frequency', yaxis_title='Magnitude')
    fig.show()

#%%
# FAZER DIAGRAMA DE BODE E ROTINA DE INTERRUPÇÃO - https://www.youtube.com/watch?v=373k6-KwOEE
