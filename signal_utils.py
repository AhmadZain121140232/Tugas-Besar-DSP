import numpy as np
from scipy.signal import butter, filtfilt

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def normalize_signal(signal):
    signal = np.array(signal)
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal))

def smooth_signal(signal, window_len=5):
    window = np.ones(window_len)/window_len
    return np.convolve(signal, window, mode='same')
