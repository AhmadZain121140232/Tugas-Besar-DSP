# signal_utils.py
# File ini berisi fungsi pendukung untuk pemrosesan sinyal, seperti filter dan normalisasi
# sinyal, yang digunakan dalam proses ekstraksi sinyal respirasi dan rPPG.

from scipy.signal import butter, filtfilt

# Fungsi untuk membuat filter bandpass
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# Fungsi untuk normalisasi sinyal
def normalize_signal(signal):
    # Normalisasi sinyal agar berada dalam rentang [0, 1]
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
