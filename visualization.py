import numpy as np #
import matplotlib.pyplot as plt #
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #

class Visualization:
    def __init__(self, master, fig_bg_color='#3C3C3C', axes_bg_color='#252525',
                 text_color='white', grid_color='#555555',
                 line1_color='lime', line2_color='cyan'):
        self.fig, self.ax = plt.subplots(figsize=(8, 5), facecolor=fig_bg_color) #
        
        self.ax.set_facecolor(axes_bg_color) # Atur warna latar belakang area plot

        # Mengatur warna untuk teks dan tick pada sumbu
        self.ax.set_title("Visualisasi Sinyal", color=text_color, fontsize=14) #
        self.ax.set_xlabel("Frame", color=text_color, fontsize=12) #
        self.ax.set_ylabel("Intensitas", color=text_color, fontsize=12) #

        self.ax.tick_params(axis='x', colors=text_color)
        self.ax.tick_params(axis='y', colors=text_color)

        # Mengatur warna untuk garis batas (spines) plot
        self.ax.spines['bottom'].set_color(text_color)
        self.ax.spines['top'].set_color(text_color) 
        self.ax.spines['left'].set_color(text_color)
        self.ax.spines['right'].set_color(text_color)

        # Menambahkan grid dengan warna yang sesuai
        self.ax.grid(True, linestyle='--', linewidth=0.5, color=grid_color)

        self.buffer_size = 300 # Ukuran buffer default untuk sumbu x
        self.ax.set_xlim(0, self.buffer_size) #
        self.ax.set_ylim(0, 255) # Batas y awal, bisa diatur dinamis nanti

        # Membuat dua garis plot dengan warna yang ditentukan
        self.respiration_line, = self.ax.plot([], [], label="Sinyal Pernapasan", color=line1_color, linewidth=1.5) #
        self.rppg_line, = self.ax.plot([], [], label="Sinyal rPPG", color=line2_color, linewidth=1.5) #
        
        # Mengatur gaya legenda
        legend = self.ax.legend(facecolor=axes_bg_color, edgecolor=grid_color, labelcolor=text_color, fontsize=10) #
        for text in legend.get_texts():
            text.set_color(text_color)

        self.canvas = FigureCanvasTkAgg(self.fig, master=master) #
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill='both', expand=True, padx=5, pady=5) # Menambahkan padding di sekitar canvas

        # Menyesuaikan layout agar judul dan label tidak terpotong
        self.fig.tight_layout(pad=1.5)


    def update(self, signals): #
        """Memperbarui data pada plot."""
        if len(signals) < 2: #
            return

        resp_signal = signals[0] #
        rppg_signal = signals[1] #

        # Menyesuaikan data sumbu X agar tetap dalam buffer_size
        if resp_signal: #
            x_resp = np.arange(len(resp_signal))
            self.respiration_line.set_xdata(x_resp) #
            self.respiration_line.set_ydata(resp_signal) #

        if rppg_signal: #
            x_rppg = np.arange(len(rppg_signal))
            self.rppg_line.set_xdata(x_rppg) #
            self.rppg_line.set_ydata(rppg_signal) #
        
        # Menyesuaikan batas sumbu Y secara dinamis
        all_y_data = []
        if resp_signal: all_y_data.extend(resp_signal)
        if rppg_signal: all_y_data.extend(rppg_signal)

        if all_y_data:
            min_y = min(all_y_data)
            max_y = max(all_y_data)
            padding_y = (max_y - min_y) * 0.1  # 10% padding
            if padding_y == 0 : padding_y = 5 # Padding minimal jika data flat
            
            self.ax.set_ylim(min_y - padding_y, max_y + padding_y)
        else:
            self.ax.set_ylim(0, 255) # Kembali ke default jika tidak ada data

        # Mengatur batas sumbu X agar tidak melebihi buffer_size, namun bisa kurang jika data sedikit
        max_len_signal = 0
        if resp_signal: max_len_signal = max(max_len_signal, len(resp_signal))
        if rppg_signal: max_len_signal = max(max_len_signal, len(rppg_signal))
        
        # Sumbu x akan mengikuti panjang sinyal terpanjang, hingga self.buffer_size
        # Jika sinyal lebih pendek dari buffer_size, xlim akan sesuai panjang sinyal.
        # Jika sinyal lebih panjang dari buffer_size, data yang ditampilkan akan menjadi yang terbaru sejumlah buffer_size
        # Namun, kode prosesor sinyal Anda menggunakan deque dengan maxlen=300, jadi ini sudah tertangani di sana.
        # Kita hanya perlu memastikan xlim sesuai dengan panjang data yang ada di buffer.
        current_xlim_max = max(self.buffer_size, max_len_signal)
        if current_xlim_max != self.ax.get_xlim()[1]: # Hanya update jika perlu
            self.ax.set_xlim(0, current_xlim_max) #

        self.canvas.draw_idle() #

    def clear_plots(self):
        """Membersihkan data dari plot."""
        self.respiration_line.set_xdata([])
        self.respiration_line.set_ydata([])
        self.rppg_line.set_xdata([])
        self.rppg_line.set_ydata([])
        self.ax.set_ylim(0, 255) # Reset batas y
        self.ax.set_xlim(0, self.buffer_size) # Reset batas x
        self.canvas.draw_idle()