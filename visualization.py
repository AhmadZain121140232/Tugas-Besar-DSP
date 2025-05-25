import numpy as np # Mengimpor NumPy untuk operasi array, terutama np.arange
import matplotlib.pyplot as plt # Mengimpor pyplot dari Matplotlib untuk membuat plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Mengimpor FigureCanvasTkAgg untuk menyematkan plot Matplotlib di Tkinter

class Visualization:
    """
    Kelas untuk membuat dan mengelola visualisasi sinyal menggunakan Matplotlib
    yang disematkan dalam antarmuka Tkinter.

    Menampilkan dua sinyal (misalnya, pernapasan dan rPPG) pada satu plot.
    Menyediakan kustomisasi untuk warna latar belakang, teks, grid, dan garis plot.
    """
    def __init__(self, master, fig_bg_color='#3C3C3C', axes_bg_color='#252525',
                 text_color='white', grid_color='#555555',
                 line1_color='lime', line2_color='cyan'):
        """
        Konstruktor untuk kelas Visualization.

        Args:
            master (tk.Widget): Widget master Tkinter tempat canvas plot akan ditempatkan.
            fig_bg_color (str, optional): Warna latar belakang untuk Figure Matplotlib. Default: '#3C3C3C'.
            axes_bg_color (str, optional): Warna latar belakang untuk Axes (area plot). Default: '#252525'.
            text_color (str, optional): Warna untuk teks (judul, label, tick). Default: 'white'.
            grid_color (str, optional): Warna untuk garis grid. Default: '#555555'.
            line1_color (str, optional): Warna untuk garis plot sinyal pertama. Default: 'lime'.
            line2_color (str, optional): Warna untuk garis plot sinyal kedua. Default: 'cyan'.
        """
        # Membuat Figure dan Axes Matplotlib
        # figsize menentukan ukuran gambar dalam inci
        # facecolor mengatur warna latar belakang Figure
        self.fig, self.ax = plt.subplots(figsize=(8, 5), facecolor=fig_bg_color) #
        
        # Mengatur warna latar belakang area plot (Axes)
        self.ax.set_facecolor(axes_bg_color) #

        # Mengatur judul plot beserta warna dan ukuran fontnya
        self.ax.set_title("Visualisasi Sinyal", color=text_color, fontsize=14) #
        # Mengatur label sumbu X beserta warna dan ukuran fontnya
        self.ax.set_xlabel("Frame", color=text_color, fontsize=12) #
        # Mengatur label sumbu Y beserta warna dan ukuran fontnya
        self.ax.set_ylabel("Intensitas", color=text_color, fontsize=12) #

        # Mengatur warna tick (angka penanda) pada sumbu X dan Y
        self.ax.tick_params(axis='x', colors=text_color) #
        self.ax.tick_params(axis='y', colors=text_color) #

        # Mengatur warna garis batas (spines) plot
        self.ax.spines['bottom'].set_color(text_color) #
        self.ax.spines['top'].set_color(text_color)    #
        self.ax.spines['left'].set_color(text_color)   #
        self.ax.spines['right'].set_color(text_color)  #

        # Menambahkan grid ke plot dengan gaya dan warna yang ditentukan
        self.ax.grid(True, linestyle='--', linewidth=0.5, color=grid_color) #

        # Ukuran buffer default untuk sumbu x, menentukan jumlah frame/data point yang ditampilkan
        self.buffer_size = 300 #
        # Mengatur batas awal sumbu X dari 0 hingga buffer_size
        self.ax.set_xlim(0, self.buffer_size) #
        # Mengatur batas awal sumbu Y, nilai ini akan diupdate secara dinamis nanti
        self.ax.set_ylim(0, 255) #

        # Membuat dua objek garis plot (Line2D) untuk dua sinyal
        # Awalnya kosong (data []), akan diupdate nanti
        # label digunakan untuk legenda
        self.respiration_line, = self.ax.plot([], [], label="Sinyal Pernapasan", color=line1_color, linewidth=1.5) #
        self.rppg_line, = self.ax.plot([], [], label="Sinyal rPPG", color=line2_color, linewidth=1.5) #
        
        # Mengatur gaya legenda plot
        legend = self.ax.legend(facecolor=axes_bg_color, edgecolor=grid_color, labelcolor=text_color, fontsize=10) #
        # Mengatur warna teks pada legenda secara eksplisit (jika labelcolor tidak cukup)
        for text in legend.get_texts():
            text.set_color(text_color) #

        # Membuat canvas Tkinter untuk menyematkan figure Matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=master) #
        # Mendapatkan widget Tkinter dari canvas Matplotlib
        self.canvas_widget = self.canvas.get_tk_widget()
        # Menempatkan widget canvas di master widget menggunakan pack manager
        # fill='both' dan expand=True membuat canvas mengisi ruang yang tersedia
        self.canvas_widget.pack(fill='both', expand=True, padx=5, pady=5) #

        # Menyesuaikan layout figure agar judul, label, dan elemen lainnya tidak terpotong
        self.fig.tight_layout(pad=1.5) #


    def update(self, signals): #
        """
        Memperbarui data pada plot dengan sinyal baru.

        Args:
            signals (list of list/numpy.ndarray): Sebuah list yang berisi dua sinyal.
                                                  signals[0] untuk sinyal pernapasan.
                                                  signals[1] untuk sinyal rPPG.
        """
        # Pastikan ada setidaknya dua sinyal yang diberikan
        if len(signals) < 2: #
            return # Keluar jika data sinyal tidak lengkap

        resp_signal = signals[0] # Sinyal pernapasan
        rppg_signal = signals[1] # Sinyal rPPG

        # Memperbarui data untuk garis sinyal pernapasan
        if resp_signal: # Hanya update jika ada data sinyal pernapasan
            x_resp = np.arange(len(resp_signal)) # Membuat array X (indeks frame) untuk sinyal pernapasan
            self.respiration_line.set_xdata(x_resp) # Set data X
            self.respiration_line.set_ydata(resp_signal) # Set data Y

        # Memperbarui data untuk garis sinyal rPPG
        if rppg_signal: # Hanya update jika ada data sinyal rPPG
            x_rppg = np.arange(len(rppg_signal)) # Membuat array X (indeks frame) untuk sinyal rPPG
            self.rppg_line.set_xdata(x_rppg) # Set data X
            self.rppg_line.set_ydata(rppg_signal) # Set data Y
        
        # --- Menyesuaikan batas sumbu Y secara dinamis ---
        all_y_data = [] # Kumpulkan semua data Y untuk menentukan min dan max
        if resp_signal: all_y_data.extend(resp_signal) #
        if rppg_signal: all_y_data.extend(rppg_signal) #

        if all_y_data: # Jika ada data Y
            min_y = min(all_y_data) # Cari nilai minimum
            max_y = max(all_y_data) # Cari nilai maksimum
            padding_y = (max_y - min_y) * 0.1  # Tambahkan padding 10% dari rentang data Y
            if padding_y == 0 : padding_y = 5 # Padding minimal jika data Y flat (semua nilainya sama)
            
            self.ax.set_ylim(min_y - padding_y, max_y + padding_y) # Atur batas Y baru dengan padding
        else:
            self.ax.set_ylim(0, 255) # Jika tidak ada data, kembali ke batas Y default

        # --- Mengatur batas sumbu X ---
        # Sumbu X akan mengikuti panjang sinyal terpanjang, hingga self.buffer_size.
        # Prosesor sinyal menggunakan deque dengan maxlen=300, jadi data yang ditampilkan
        # adalah 300 sampel terakhir jika sinyal lebih panjang dari itu.
        # Xlim di sini disesuaikan dengan panjang data aktual yang ada di buffer sinyal yang dikirim ke update.
        max_len_signal = 0
        if resp_signal: max_len_signal = max(max_len_signal, len(resp_signal)) #
        if rppg_signal: max_len_signal = max(max_len_signal, len(rppg_signal)) #
        
        # Batas atas sumbu X akan menjadi antara buffer_size atau panjang sinyal maksimum saat ini,
        # mana yang lebih besar, untuk mengakomodasi semua data yang ada jika kurang dari buffer_size,
        # atau tetap pada buffer_size jika data lebih banyak (karena data lama sudah dibuang oleh deque).
        # Namun, karena deque sudah membatasi jumlah data, max_len_signal tidak akan melebihi buffer_size (300).
        # Jadi, kita bisa menyederhanakannya:
        current_xlim_max = max(self.buffer_size, max_len_signal) if max_len_signal > 0 else self.buffer_size
        # Hanya update xlim jika batasnya berubah untuk efisiensi
        if current_xlim_max != self.ax.get_xlim()[1] or self.ax.get_xlim()[1] == 0: # Periksa juga jika xlim[1] masih 0 (inisial)
            self.ax.set_xlim(0, current_xlim_max if current_xlim_max > 0 else self.buffer_size) #

        # Menggambar ulang canvas hanya jika ada perubahan (draw_idle lebih efisien)
        self.canvas.draw_idle() #

    def clear_plots(self):
        """
        Membersihkan semua data dari garis plot dan mereset batas sumbu.
        Dipanggil biasanya sebelum memulai sesi monitoring baru.
        """
        # Mengosongkan data pada garis sinyal pernapasan
        self.respiration_line.set_xdata([]) #
        self.respiration_line.set_ydata([]) #
        # Mengosongkan data pada garis sinyal rPPG
        self.rppg_line.set_xdata([]) #
        self.rppg_line.set_ydata([]) #
        
        # Mereset batas sumbu Y ke nilai default
        self.ax.set_ylim(0, 255) #
        # Mereset batas sumbu X ke nilai default (buffer_size)
        self.ax.set_xlim(0, self.buffer_size) #
        
        # Menggambar ulang canvas untuk menampilkan plot yang kosong
        self.canvas.draw_idle() #