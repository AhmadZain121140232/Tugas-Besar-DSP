import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from respirasi_processor import RespirationProcessor
from rppg_processor import RPPGProcessor
from visualization import Visualization

class VitalDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Respiration Real-time")
        self.root.geometry("1000x600")
        self.root.config(bg="black")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(2, weight=1)

        self.title_label = tk.Label(self.root, text="Welcome To Signal Respiration Real-time",
                                    font=("Helvetica", 16), fg="white", bg="black")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.button_frame = ttk.Frame(self.root, padding="10")
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=20)

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start_video)
        self.start_button.grid(row=0, column=0, padx=20)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_video)
        self.stop_button.grid(row=0, column=1, padx=20)

        # Video frame di kolom 0
        self.video_frame = ttk.LabelFrame(self.root, text="Video", padding=10)
        self.video_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # Signal frame di kolom 1
        self.signal_frame = ttk.LabelFrame(self.root, text="Signal Visualizations", padding=10)
        self.signal_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.visualization = Visualization(self.signal_frame)

        self.respiration_processor = RespirationProcessor()
        self.rppg_processor = RPPGProcessor()

        self.cap = None
        self.running = False

        # Bind keyboard event untuk shortcut keluar program dengan 'q'
        self.root.bind('<Key>', self.key_press)

    def key_press(self, event):
        if event.char.lower() == 'q':
            self.stop_video()
            self.root.quit()  # Keluar dari mainloop Tkinter

    def start_video(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.respiration_processor.reset()
            self.rppg_processor.reset()
            self.capture_video()

    def stop_video(self):
        if self.running:
            self.running = False
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            cv2.destroyAllWindows()

    def capture_video(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.stop_video()
            return

        processed_frame, respiration_signal = self.respiration_processor.process(frame)
        processed_frame, rppg_signal = self.rppg_processor.process(processed_frame)

        # Update video frame
        cv2_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(cv2_frame)
        photo = ImageTk.PhotoImage(image=image)
        self.video_label.config(image=photo)
        self.video_label.image = photo

        # Update grafik sinyal
        self.visualization.update([respiration_signal, rppg_signal])

        self.root.after(30, self.capture_video)