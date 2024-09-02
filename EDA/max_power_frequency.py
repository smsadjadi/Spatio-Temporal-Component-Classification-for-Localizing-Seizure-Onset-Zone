import numpy as np
from scipy.signal import periodogram

def max_power_frequency(time_series, tr):
    fs = 1 / tr
    freqs, power_spectrum = periodogram(time_series, fs)
    
    min_freq = 0.01
    max_freq = 0.1
    
    freq_mask = (freqs >= min_freq) & (freqs <= max_freq)
    max_power_frequency = round(freqs[freq_mask][np.argmax(power_spectrum[freq_mask])], 3)
    
    return max_power_frequency