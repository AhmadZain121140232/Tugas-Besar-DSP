import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Visualization:
    def __init__(self, master):
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.lines = []
        self.ax.set_ylim(0, 255)
        self.ax.set_xlim(0, 300)
        self.ax.set_title("Signal Visualizations")
        self.ax.set_xlabel("Frame")
        self.ax.set_ylabel("Intensity")

        # Buat dua line: respiration dan rPPG
        self.respiration_line, = self.ax.plot([], [], label="Respiratory Signal", color='green')
        self.rppg_line, = self.ax.plot([], [], label="rPPG Signal", color='blue')
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def update(self, signals):
        # signals adalah list dua array sinyal: [respiration_signal, rppg_signal]
        if len(signals) < 2:
            return

        resp_signal = signals[0]
        rppg_signal = signals[1]

        if resp_signal:
            self.respiration_line.set_xdata(np.arange(len(resp_signal)))
            self.respiration_line.set_ydata(resp_signal)

        if rppg_signal:
            self.rppg_line.set_xdata(np.arange(len(rppg_signal)))
            self.rppg_line.set_ydata(rppg_signal)

        max_len = max(len(resp_signal), len(rppg_signal), 300)
        self.ax.set_xlim(0, max_len)
        self.canvas.draw_idle()
