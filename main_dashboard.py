import tkinter as tk
from tkinter import ttk, font as tkFont
from PIL import Image, ImageTk
import cv2
import numpy as np
# Matplotlib dan FigureCanvasTkAgg digunakan di dalam kelas Visualization

from respirasi_processor import RespirationProcessor #
from rppg_processor import RPPGProcessor #
from visualization import Visualization #

class VitalDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Sinyal Vital Real-time") # Judul diubah agar lebih deskriptif
        self.root.geometry("1200x750") # Sedikit menambah tinggi untuk spasi yang lebih baik
        self.root.configure(bg="#2E2E2E") # Warna latar belakang utama (abu-abu sangat gelap)

        # --- Konfigurasi Gaya (Style Configuration) ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # Menggunakan tema 'clam' sebagai dasar yang lebih mudah dikustomisasi

        # Mendefinisikan font kustom
        self.title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Gaya untuk ttk.LabelFrame (bingkai berlabel)
        self.style.configure("Dark.TLabelframe",
                             background="#3C3C3C",       # Latar belakang bingkai (abu-abu gelap)
                             bordercolor="#555555",      # Warna border bingkai
                             relief="raised",            # Efek timbul pada border
                             borderwidth=1)
        self.style.configure("Dark.TLabelframe.Label",
                             foreground="white",         # Warna teks judul bingkai
                             background="#3C3C3C",       # Latar belakang teks judul bingkai
                             font=self.label_font,
                             padding=(10, 5))            # Padding di sekitar teks judul

        # Gaya untuk ttk.Button (tombol)
        self.style.configure("Dark.TButton",
                             background="#0078D4",       # Warna latar tombol (biru modern)
                             foreground="white",         # Warna teks tombol
                             font=self.button_font,
                             borderwidth=1,
                             relief="raised",
                             padding=(10, 5))            # Padding internal tombol
        self.style.map("Dark.TButton",
                       background=[('active', '#005A9E'),  # Warna saat mouse hover (biru lebih gelap)
                                   ('pressed', '#003963')],# Warna saat tombol ditekan (biru sangat gelap)
                       relief=[('pressed', 'sunken'),
                               ('!pressed', 'raised')])

        # Gaya untuk ttk.Frame (bingkai biasa)
        self.style.configure("Dark.TFrame", background="#2E2E2E") # Latar belakang untuk frame tombol

        # --- Konfigurasi Tata Letak Grid Utama ---
        self.root.columnconfigure(0, weight=2) # Kolom untuk video, mengambil porsi lebih kecil
        self.root.columnconfigure(1, weight=3) # Kolom untuk sinyal, mengambil porsi lebih besar
        self.root.rowconfigure(0, weight=0)  # Baris untuk judul
        self.root.rowconfigure(1, weight=0)  # Baris untuk tombol
        self.root.rowconfigure(2, weight=1)  # Baris untuk frame video dan sinyal (mengisi sisa ruang)

        # --- Label Judul Aplikasi ---
        self.title_label = tk.Label(self.root, text="Monitor Sinyal Real-time",
                                    font=self.title_font, fg="white", bg="#2E2E2E")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 15)) # Padding atas dan bawah

        # --- Bingkai untuk Tombol ---
        self.button_frame = ttk.Frame(self.root, style="Dark.TFrame", padding="10")
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20)) # Padding bawah

        self.start_button = ttk.Button(self.button_frame, text="Mulai Monitoring",
                                       command=self.start_video, style="Dark.TButton", width=22) # Lebar tombol disesuaikan
        self.start_button.grid(row=0, column=0, padx=15) # Padding horizontal antar tombol

        self.stop_button = ttk.Button(self.button_frame, text="Hentikan Monitoring",
                                      command=self.stop_video, style="Dark.TButton", width=22) # Lebar tombol disesuaikan
        self.stop_button.grid(row=0, column=1, padx=15) # Padding horizontal antar tombol
        self.stop_button.config(state=tk.DISABLED) # Tombol stop awalnya nonaktif

        # --- Bingkai Video ---
        self.video_frame = ttk.LabelFrame(self.root, text="Video Kamera Langsung",
                                          style="Dark.TLabelframe", padding=10)
        self.video_frame.grid(row=2, column=0, sticky="nsew", padx=(20,10), pady=(0,20)) # Padding keliling
        self.video_frame.columnconfigure(0, weight=1) # Agar label video mengisi frame
        self.video_frame.rowconfigure(0, weight=1)  # Agar label video mengisi frame

        self.video_label = ttk.Label(self.video_frame, background="#1E1E1E") # Latar belakang area video (hitam)
        self.video_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) # Padding di dalam bingkai video


        # --- Bingkai Sinyal ---
        self.signal_frame = ttk.LabelFrame(self.root, text="Visualisasi Sinyal",
                                           style="Dark.TLabelframe", padding=10)
        self.signal_frame.grid(row=2, column=1, sticky="nsew", padx=(10,20), pady=(0,20)) # Padding keliling
        self.signal_frame.columnconfigure(0, weight=1) # Agar canvas plot mengisi frame
        self.signal_frame.rowconfigure(0, weight=1)  # Agar canvas plot mengisi frame

        # --- Inisialisasi Visualisasi (Matplotlib) ---
        # Meneruskan warna tema ke kelas Visualization
        self.visualization = Visualization(self.signal_frame,
                                           fig_bg_color="#3C3C3C",      # Latar belakang gambar Matplotlib
                                           axes_bg_color="#252525",     # Latar belakang area plot (lebih gelap dari fig_bg)
                                           text_color="white",          # Warna teks plot
                                           grid_color="#555555",        # Warna grid plot
                                           line1_color="#00FF00",       # Warna garis sinyal pernapasan (hijau terang)
                                           line2_color="#00FFFF")       # Warna garis sinyal rPPG (cyan terang)

        # --- Inisialisasi Prosesor Sinyal ---
        self.respiration_processor = RespirationProcessor() #
        self.rppg_processor = RPPGProcessor() #

        self.cap = None #
        self.running = False #

        # --- Menangani Penutupan Jendela dan Pintasan Keyboard ---
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) # Saat tombol 'X' jendela ditekan
        self.root.bind('<Key>', self.key_press_handler) # Menangani penekanan tombol keyboard

    def key_press_handler(self, event): #
        """Menangani event penekanan tombol."""
        if event.char.lower() == 'q': #
            self.on_closing()
        elif event.char.lower() == 's' and not self.running:
            self.start_video()
        elif event.char.lower() == 'x' and self.running:
            self.stop_video()


    def on_closing(self):
        """Menangani proses penutupan aplikasi."""
        self.stop_video() # Pastikan video berhenti sebelum keluar
        self.root.quit()    # Keluar dari mainloop Tkinter
        self.root.destroy() # Hancurkan jendela utama

    def start_video(self): #
        """Memulai penangkapan video dan pemrosesan sinyal."""
        if not self.running: #
            try:
                self.cap = cv2.VideoCapture(0) # Menggunakan kamera default
                if not self.cap.isOpened():
                    print("Error: Tidak dapat membuka kamera.")
                    self.cap = None
                    # Tampilkan pesan error di GUI jika diinginkan
                    return
            except Exception as e:
                print(f"Error saat membuka kamera: {e}")
                self.cap = None
                return

            self.running = True #
            self.respiration_processor.reset() #
            self.rppg_processor.reset() #
            self.visualization.clear_plots() # Bersihkan plot sebelum memulai
            self.capture_video() #
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_video(self): #
        """Menghentikan penangkapan video."""
        if self.running: #
            self.running = False #
            if self.cap is not None: #
                self.cap.release() #
                self.cap = None #
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            # Opsional: Bersihkan frame video terakhir dari label
            # blank_image = ImageTk.PhotoImage(Image.new('RGB', (640, 480), '#1E1E1E'))
            # self.video_label.config(image=blank_image)
            # self.video_label.image = blank_image

    def capture_video(self): #
        """Menangkap frame dari kamera, memproses, dan menampilkannya."""
        if not self.running or self.cap is None: #
            self.stop_video() # Pastikan berhenti jika tidak seharusnya berjalan
            return

        ret, frame = self.cap.read() #
        if not ret: #
            print("Error: Gagal menangkap frame.")
            self.stop_video() #
            return

        # Pemrosesan frame
        # Sebaiknya frame di-flip sekali saja, mungkin di awal sebelum dikirim ke prosesor
        # atau masing-masing prosesor tidak melakukan flip jika sudah di-flip sebelumnya.
        # Untuk saat ini, asumsikan prosesor menangani flip internalnya.
        processed_frame_resp, respiration_signal = self.respiration_processor.process(frame.copy()) #
        # Frame yang sudah diproses oleh respiration_processor (mungkin sudah ada kotak ROI)
        # kemudian diproses oleh rppg_processor
        final_processed_frame, rppg_signal = self.rppg_processor.process(processed_frame_resp) #

        # --- Memperbarui Tampilan Video ---
        try:
            # Konversi frame OpenCV (BGR) ke format yang bisa digunakan PIL (RGB)
            cv2_frame_rgb = cv2.cvtColor(final_processed_frame, cv2.COLOR_BGR2RGB) #
            pil_image = Image.fromarray(cv2_frame_rgb) #

            # Mengubah ukuran gambar agar sesuai dengan label video, mempertahankan rasio aspek
            video_label_width = self.video_label.winfo_width()
            video_label_height = self.video_label.winfo_height()

            if video_label_width > 1 and video_label_height > 1: # Pastikan dimensi label valid
                img_aspect_ratio = pil_image.width / pil_image.height
                label_aspect_ratio = video_label_width / video_label_height

                if img_aspect_ratio > label_aspect_ratio:
                    # Gambar lebih lebar relatif terhadap label, sesuaikan lebar gambar
                    new_width = video_label_width
                    new_height = int(new_width / img_aspect_ratio)
                else:
                    # Gambar lebih tinggi relatif terhadap label, sesuaikan tinggi gambar
                    new_height = video_label_height
                    new_width = int(new_height * img_aspect_ratio)
                
                # Gunakan Image.Resampling.LANCZOS untuk kualitas terbaik saat resize
                resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image=resized_image) #
            else:
                # Jika dimensi label belum siap, tampilkan gambar asli (mungkin perlu penyesuaian)
                photo = ImageTk.PhotoImage(image=pil_image) #


            self.video_label.config(image=photo) #
            self.video_label.image = photo # Simpan referensi agar gambar tidak di-garbage collect!
        except Exception as e:
            print(f"Error saat memperbarui frame video: {e}")


        # --- Memperbarui Grafik Sinyal ---
        self.visualization.update([respiration_signal, rppg_signal]) #

        # Loop untuk frame berikutnya
        if self.running: #
            self.root.after(20, self.capture_video) # FPS disesuaikan (misal 20ms -> 50 FPS)

# Titik masuk aplikasi tidak berubah, jadi main.py tetap sama.
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VitalDashboard(root)
#     root.mainloop()