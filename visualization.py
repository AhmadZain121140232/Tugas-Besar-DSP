# visualization.py
# File ini digunakan untuk visualisasi sinyal yang telah diproses, seperti sinyal respirasi
# dan rPPG, dengan menggunakan pustaka matplotlib.

import matplotlib.pyplot as plt

# Fungsi untuk memvisualisasikan sinyal respirasi dan rPPG
def visualize_signals(respiration_signal, rppg_signal):
    # Visualisasi sinyal respirasi
    plt.figure(figsize=(10, 5))

    plt.subplot(2, 1, 1)
    plt.plot(respiration_signal)
    plt.title("Respiratory Signal")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")

    # Visualisasi sinyal rPPG
    plt.subplot(2, 1, 2)
    plt.plot(rppg_signal)
    plt.title("rPPG Signal")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()
