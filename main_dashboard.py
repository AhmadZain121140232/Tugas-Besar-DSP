import tkinter as tk  # Mengimpor modul Tkinter untuk membuat GUI
from tkinter import ttk, font as tkFont  # Mengimpor submodule ttk untuk widget yang lebih modern dan font untuk kustomisasi font
from PIL import Image, ImageTk  # Mengimpor Image dan ImageTk dari Pillow untuk menangani gambar
import cv2  # Mengimpor OpenCV untuk pemrosesan video dan gambar
import numpy as np  # Mengimpor NumPy untuk operasi numerik, terutama array
# Matplotlib dan FigureCanvasTkAgg digunakan di dalam kelas Visualization, tidak perlu diimpor langsung di sini jika sudah di-handle di sana.

# Mengimpor kelas-kelas dan fungsi yang dibutuhkan dari file lain dalam proyek
from respirasi_processor import RespirationProcessor # Untuk memproses sinyal pernapasan
from rppg_processor import RPPGProcessor # Untuk memproses sinyal rPPG
from visualization import Visualization # Untuk visualisasi sinyal menggunakan Matplotlib
from vital_cam_gui import start_video_capture # Fungsi untuk menginisialisasi penangkapan video dari kamera

class VitalDashboard:
    """
    Kelas utama untuk aplikasi VitalDashboard.
    Mengelola antarmuka pengguna (GUI), penangkapan video, pemrosesan sinyal (pernapasan dan rPPG),
    dan visualisasi data vital secara real-time. Kelas ini mengintegrasikan semua komponen
    aplikasi menjadi satu kesatuan fungsional.
    """
    def __init__(self, root):
        """
        Konstruktor untuk kelas VitalDashboard.

        Menginisialisasi jendela utama, mengatur gaya (style) untuk widget Tkinter,
        menata letak (layout) elemen-elemen GUI, membuat dan menempatkan widget
        (seperti tombol, label, dan frame). Juga menginisialisasi objek untuk
        pemrosesan sinyal (RespirationProcessor, RPPGProcessor) dan visualisasi data (Visualization).

        Args:
            root (tk.Tk): Instance root window dari Tkinter yang menjadi dasar aplikasi.
        """
        self.root = root  # Menyimpan referensi ke root window Tkinter
        self.root.title("Monitor Sinyal Vital Real-time") # Mengatur judul jendela aplikasi
        self.root.geometry("1200x750") # Mengatur ukuran awal jendela aplikasi (lebar x tinggi)
        self.root.configure(bg="#2E2E2E") # Mengatur warna latar belakang utama jendela menjadi abu-abu sangat gelap

        # --- Konfigurasi Gaya (Style Configuration) ---
        self.style = ttk.Style()  # Membuat instance Style untuk kustomisasi tampilan widget ttk
        self.style.theme_use('clam') # Menggunakan tema 'clam' sebagai dasar, yang lebih mudah dikustomisasi daripada tema default

        # Mendefinisikan font kustom yang akan digunakan di berbagai widget
        self.title_font = tkFont.Font(family="Helvetica", size=20, weight="bold") # Font untuk judul utama aplikasi
        self.label_font = tkFont.Font(family="Helvetica", size=12) # Font standar untuk label pada frame
        self.button_font = tkFont.Font(family="Helvetica", size=12, weight="bold") # Font untuk teks pada tombol

        # Gaya untuk ttk.LabelFrame (bingkai dengan label)
        # Mengatur tampilan visual dari LabelFrame, digunakan untuk mengelompokkan widget
        self.style.configure("Dark.TLabelframe",
                             background="#3C3C3C",       # Warna latar belakang bingkai (abu-abu gelap)
                             bordercolor="#555555",      # Warna garis tepi (border) bingkai
                             relief="raised",            # Efek timbul pada garis tepi untuk memberikan kesan 3D
                             borderwidth=1)              # Lebar garis tepi
        # Gaya untuk label di dalam ttk.LabelFrame
        self.style.configure("Dark.TLabelframe.Label",
                             foreground="white",         # Warna teks judul bingkai
                             background="#3C3C3C",       # Warna latar belakang teks judul bingkai, sama dengan bingkainya
                             font=self.label_font,       # Menggunakan font label yang sudah didefinisikan
                             padding=(10, 5))            # Padding di sekitar teks judul (horizontal, vertikal)

        # Gaya untuk ttk.Button (tombol)
        # Mengatur tampilan visual dan interaksi tombol
        self.style.configure("Dark.TButton",
                             background="#0078D4",       # Warna latar tombol (biru modern)
                             foreground="white",         # Warna teks tombol
                             font=self.button_font,      # Menggunakan font tombol yang sudah didefinisikan
                             borderwidth=1,              # Lebar garis tepi tombol
                             relief="raised",            # Efek timbul pada tombol
                             padding=(10, 5))            # Padding internal tombol (horizontal, vertikal)
        # Mendefinisikan perubahan tampilan tombol berdasarkan state (misalnya, saat mouse hover atau ditekan)
        self.style.map("Dark.TButton",
                       background=[('active', '#005A9E'),  # Warna latar saat mouse hover (biru lebih gelap)
                                   ('pressed', '#003963')],# Warna latar saat tombol ditekan (biru sangat gelap)
                       relief=[('pressed', 'sunken'),      # Efek relief menjadi cekung saat tombol ditekan
                               ('!pressed', 'raised')])   # Efek relief timbul saat tombol tidak ditekan

        # Gaya untuk ttk.Frame (bingkai biasa tanpa label)
        self.style.configure("Dark.TFrame", background="#2E2E2E") # Latar belakang untuk frame biasa, sama dengan root window

        # --- Konfigurasi Tata Letak Grid Utama ---
        # Mengatur bagaimana kolom dan baris dalam grid utama (root window) akan menyesuaikan ukuran
        # 'weight' menentukan seberapa besar porsi ruang ekstra yang akan dialokasikan ke kolom/baris tersebut saat jendela di-resize
        self.root.columnconfigure(0, weight=2) # Kolom 0 (untuk video) mengambil 2 bagian dari ruang ekstra
        self.root.columnconfigure(1, weight=3) # Kolom 1 (untuk sinyal) mengambil 3 bagian dari ruang ekstra (lebih besar)
        self.root.rowconfigure(0, weight=0)  # Baris 0 (untuk judul) tidak akan berekspansi secara vertikal
        self.root.rowconfigure(1, weight=0)  # Baris 1 (untuk tombol) tidak akan berekspansi secara vertikal
        self.root.rowconfigure(2, weight=1)  # Baris 2 (untuk frame video dan sinyal) akan mengisi sisa ruang vertikal

        # --- Label Judul Aplikasi ---
        # Membuat label untuk menampilkan judul utama aplikasi
        self.title_label = tk.Label(self.root, text="Monitor Sinyal Real-time",
                                    font=self.title_font, fg="white", bg="#2E2E2E") # Menggunakan font, warna teks, dan warna latar yang ditentukan
        # Menempatkan label judul dalam grid utama, membentang 2 kolom, dengan padding vertikal
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 15))

        # --- Bingkai untuk Tombol ---
        # Membuat frame untuk mengelompokkan tombol "Mulai" dan "Hentikan"
        self.button_frame = ttk.Frame(self.root, style="Dark.TFrame", padding="10") # Menggunakan gaya Dark.TFrame
        # Menempatkan frame tombol dalam grid utama, membentang 2 kolom, dengan padding bawah
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Membuat tombol "Mulai Monitoring"
        self.start_button = ttk.Button(self.button_frame, text="Mulai Monitoring",
                                       command=self.start_video, style="Dark.TButton", width=22) # Menghubungkan dengan metode start_video
        self.start_button.grid(row=0, column=0, padx=15) # Menempatkan tombol di frame tombol dengan padding horizontal

        # Membuat tombol "Hentikan Monitoring"
        self.stop_button = ttk.Button(self.button_frame, text="Hentikan Monitoring",
                                      command=self.stop_video, style="Dark.TButton", width=22) # Menghubungkan dengan metode stop_video
        self.stop_button.grid(row=0, column=1, padx=15) # Menempatkan tombol di frame tombol dengan padding horizontal
        self.stop_button.config(state=tk.DISABLED) # Tombol stop awalnya dinonaktifkan karena monitoring belum dimulai

        # --- Bingkai Video ---
        # Membuat LabelFrame (bingkai dengan judul) untuk menampilkan video dari kamera
        self.video_frame = ttk.LabelFrame(self.root, text="Video Kamera Langsung",
                                          style="Dark.TLabelframe", padding=10) # Menggunakan gaya Dark.TLabelframe
        # Menempatkan frame video dalam grid utama, mengisi ruang yang tersedia (sticky="nsew")
        self.video_frame.grid(row=2, column=0, sticky="nsew", padx=(20,10), pady=(0,20)) # Padding eksternal
        self.video_frame.columnconfigure(0, weight=1) # Mengatur agar konten di dalam frame video (label video) dapat mengisi ruang horizontal
        self.video_frame.rowconfigure(0, weight=1)  # Mengatur agar konten di dalam frame video (label video) dapat mengisi ruang vertikal

        # Label untuk menampilkan frame video dari kamera
        self.video_label = ttk.Label(self.video_frame, background="#1E1E1E") # Warna latar belakang area video (hitam keabuan)
        self.video_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) # Menempatkan label video di dalam frame video, mengisi ruang


        # --- Bingkai Sinyal ---
        # Membuat LabelFrame untuk menampilkan visualisasi sinyal (plot Matplotlib)
        self.signal_frame = ttk.LabelFrame(self.root, text="Visualisasi Sinyal",
                                           style="Dark.TLabelframe", padding=10) # Menggunakan gaya Dark.TLabelframe
        # Menempatkan frame sinyal dalam grid utama, mengisi ruang yang tersedia
        self.signal_frame.grid(row=2, column=1, sticky="nsew", padx=(10,20), pady=(0,20)) # Padding eksternal
        self.signal_frame.columnconfigure(0, weight=1) # Mengatur agar konten di dalam frame sinyal (canvas plot) dapat mengisi ruang horizontal
        self.signal_frame.rowconfigure(0, weight=1)  # Mengatur agar konten di dalam frame sinyal (canvas plot) dapat mengisi ruang vertikal

        # --- Inisialisasi Visualisasi (Matplotlib) ---
        # Membuat instance dari kelas Visualization, meneruskan frame sinyal sebagai master widget
        # dan parameter warna untuk kustomisasi tampilan plot agar sesuai dengan tema gelap aplikasi
        self.visualization = Visualization(self.signal_frame,
                                           fig_bg_color="#3C3C3C",      # Warna latar belakang Figure Matplotlib
                                           axes_bg_color="#252525",     # Warna latar belakang area plot (Axes)
                                           text_color="white",          # Warna teks pada plot (judul, label, tick)
                                           grid_color="#555555",        # Warna garis grid pada plot
                                           line1_color="#00FF00",       # Warna garis untuk sinyal pernapasan (hijau terang)
                                           line2_color="#00FFFF")       # Warna garis untuk sinyal rPPG (cyan terang)

        # --- Inisialisasi Prosesor Sinyal ---
        self.respiration_processor = RespirationProcessor() # Membuat instance dari RespirationProcessor
        self.rppg_processor = RPPGProcessor() # Membuat instance dari RPPGProcessor

        # --- Variabel Status Aplikasi ---
        self.cap = None # Variabel untuk menyimpan objek VideoCapture OpenCV, awalnya None (tidak ada kamera aktif)
        self.running = False # Flag boolean untuk menandakan apakah proses penangkapan video dan monitoring sedang berjalan

        # --- Menangani Penutupan Jendela dan Pintasan Keyboard ---
        # Menetapkan fungsi on_closing untuk dipanggil saat pengguna menekan tombol 'X' (close) pada jendela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Mengikat event penekanan tombol keyboard ('<Key>') ke fungsi key_press_handler
        self.root.bind('<Key>', self.key_press_handler)

    def key_press_handler(self, event):
        """
        Menangani event penekanan tombol keyboard untuk menyediakan pintasan (shortcuts).

        Pintasan yang didukung:
        - 'q': Keluar dari aplikasi (sama seperti menutup jendela).
        - 's': Memulai monitoring (jika belum berjalan).
        - 'x': Menghentikan monitoring (jika sedang berjalan).

        Args:
            event (tk.Event): Objek event Tkinter yang berisi informasi tentang tombol yang ditekan,
                              seperti karakter tombol (`event.char`).
        """
        char = event.char.lower() # Mendapatkan karakter tombol yang ditekan dan mengubahnya ke huruf kecil
        if char == 'q': # Jika tombol 'q' ditekan
            self.on_closing() # Panggil fungsi untuk menutup aplikasi
        elif char == 's' and not self.running: # Jika tombol 's' ditekan DAN monitoring tidak sedang berjalan
            self.start_video() # Panggil fungsi untuk memulai video/monitoring
        elif char == 'x' and self.running: # Jika tombol 'x' ditekan DAN monitoring sedang berjalan
            self.stop_video() # Panggil fungsi untuk menghentikan video/monitoring


    def on_closing(self):
        """
        Menangani proses penutupan aplikasi dengan aman.

        Fungsi ini dipanggil ketika pengguna mencoba menutup jendela aplikasi (misalnya,
        dengan menekan tombol 'X'). Ini memastikan bahwa video dihentikan dengan benar
        (melepaskan resource kamera) sebelum aplikasi keluar dan jendela dihancurkan.
        """
        self.stop_video() # Memastikan proses penangkapan video dihentikan dan kamera dilepaskan
        self.root.quit()    # Keluar dari mainloop Tkinter, menghentikan pemrosesan event
        self.root.destroy() # Menghancurkan semua widget dan jendela utama, membersihkan resource

    def start_video(self):
        """
        Memulai proses penangkapan video dari kamera, mereset prosesor sinyal,
        membersihkan plot sebelumnya, dan memulai loop utama untuk menangkap dan memproses frame.

        Metode ini akan:
        1. Mencoba menginisialisasi kamera menggunakan fungsi `start_video_capture`.
        2. Jika kamera berhasil dibuka, set flag `self.running` menjadi True.
        3. Mereset state pada `RespirationProcessor` dan `RPPGProcessor`.
        4. Membersihkan plot yang ada di `Visualization`.
        5. Memanggil `capture_video()` untuk memulai loop pemrosesan frame.
        6. Mengatur ulang state tombol "Mulai" (menjadi nonaktif) dan "Hentikan" (menjadi aktif).
        """
        if not self.running: # Hanya jalankan jika monitoring belum/tidak sedang berjalan
            try:
                # Menggunakan fungsi dari vital_cam_gui.py untuk menginisialisasi kamera
                # Angka 0 biasanya merujuk pada kamera default/internal
                self.cap = start_video_capture(0) # Panggil fungsi eksternal untuk setup kamera
                
                # Memeriksa apakah objek kamera berhasil dibuat dan dibuka
                if self.cap is None or not self.cap.isOpened():
                    print("Error: Tidak dapat membuka kamera.") # Pesan error jika kamera gagal diakses
                    self.cap = None # Pastikan self.cap adalah None jika gagal
                    return # Keluar dari fungsi jika kamera tidak bisa dibuka
            except Exception as e:
                # Menangani potensi error lain yang mungkin terjadi saat membuka kamera
                print(f"Error saat membuka kamera: {e}")
                self.cap = None # Pastikan self.cap adalah None jika terjadi error
                return # Keluar dari fungsi

            self.running = True # Set flag bahwa monitoring sedang berjalan
            self.respiration_processor.reset() # Mereset buffer dan state di RespirationProcessor
            self.rppg_processor.reset() # Mereset buffer dan state di RPPGProcessor
            self.visualization.clear_plots() # Membersihkan data dari plot sebelumnya di visualizer
            
            self.capture_video() # Memulai fungsi rekursif untuk menangkap dan memproses frame video
            
            # Mengatur ulang state tombol GUI
            self.start_button.config(state=tk.DISABLED) # Tombol "Mulai Monitoring" dinonaktifkan
            self.stop_button.config(state=tk.NORMAL)   # Tombol "Hentikan Monitoring" diaktifkan

    def stop_video(self):
        """
        Menghentikan proses penangkapan video dan monitoring.

        Metode ini akan:
        1. Set flag `self.running` menjadi False untuk menghentikan loop di `capture_video`.
        2. Melepaskan objek kamera (`self.cap.release()`) untuk membebaskan resource.
        3. Mengatur `self.cap` kembali ke `None`.
        4. Mengatur ulang state tombol "Mulai" (menjadi aktif) dan "Hentikan" (menjadi nonaktif).
        """
        if self.running: # Hanya jalankan jika monitoring sedang berjalan
            self.running = False # Set flag bahwa monitoring dihentikan
            if self.cap is not None: # Jika objek VideoCapture ada (kamera sedang digunakan)
                self.cap.release() # Melepaskan resource kamera
                self.cap = None # Set objek kamera kembali ke None
            
            # Mengatur ulang state tombol GUI
            self.start_button.config(state=tk.NORMAL)   # Tombol "Mulai Monitoring" diaktifkan kembali
            self.stop_button.config(state=tk.DISABLED) # Tombol "Hentikan Monitoring" dinonaktifkan

    def capture_video(self):
        """
        Menangkap satu frame dari kamera, memprosesnya untuk mendapatkan sinyal pernapasan dan rPPG,
        menampilkan frame yang telah diproses di GUI, dan memperbarui plot sinyal.

        Fungsi ini bersifat rekursif melalui `self.root.after()`: ia menjadwalkan dirinya sendiri
        untuk dipanggil kembali setelah interval waktu tertentu, menciptakan loop video real-time
        selama flag `self.running` adalah True dan kamera (`self.cap`) tersedia.

        Proses per frame:
        1. Baca frame dari kamera.
        2. Jika gagal, hentikan video.
        3. Proses frame menggunakan `RespirationProcessor`.
        4. Proses frame (hasil dari `RespirationProcessor`) menggunakan `RPPGProcessor`.
        5. Konversi frame yang sudah diproses untuk ditampilkan di label video Tkinter.
        6. Perbarui visualisasi sinyal dengan data baru.
        7. Jadwalkan pemanggilan berikutnya untuk `capture_video`.
        """
        # Pemeriksaan kondisi untuk melanjutkan loop: monitoring harus berjalan DAN objek kamera harus ada
        if not self.running or self.cap is None:
            self.stop_video() # Jika kondisi tidak terpenuhi, pastikan video dihentikan dengan benar
            return # Keluar dari fungsi (menghentikan loop)

        ret, frame = self.cap.read() # Membaca satu frame dari kamera; `ret` adalah boolean (berhasil/gagal), `frame` adalah data gambar
        if not ret: # Jika frame tidak berhasil ditangkap (misalnya, kamera terputus)
            print("Error: Gagal menangkap frame.") # Cetak pesan error ke konsol
            self.stop_video() # Hentikan proses monitoring
            return # Keluar dari fungsi

        # --- Pemrosesan Frame ---
        # frame.copy() digunakan untuk mengirim salinan frame ke prosesor, sehingga modifikasi
        # di satu prosesor tidak mempengaruhi input ke prosesor lain jika frame asli masih dibutuhkan.
        # 1. Proses frame untuk sinyal pernapasan
        processed_frame_resp, respiration_signal = self.respiration_processor.process(frame.copy())
        
        # 2. Proses frame (yang mungkin sudah ada ROI pernapasan dari prosesor sebelumnya) untuk sinyal rPPG
        final_processed_frame, rppg_signal = self.rppg_processor.process(processed_frame_resp)

        # --- Memperbarui Tampilan Video di GUI ---
        try:
            # Konversi frame dari format OpenCV (BGR) ke format RGB yang umum digunakan oleh Pillow/PIL
            cv2_frame_rgb = cv2.cvtColor(final_processed_frame, cv2.COLOR_BGR2RGB)
            # Membuat objek Image dari Pillow dari array NumPy (frame RGB)
            pil_image = Image.fromarray(cv2_frame_rgb)

            # Mendapatkan dimensi aktual dari widget label video untuk penyesuaian ukuran gambar (resize)
            video_label_width = self.video_label.winfo_width()  # Lebar widget label video saat ini
            video_label_height = self.video_label.winfo_height() # Tinggi widget label video saat ini

            # Pastikan dimensi label valid (lebih besar dari 1x1 piksel) sebelum mengubah ukuran.
            # Ini untuk menghindari error jika widget belum sepenuhnya digambar.
            if video_label_width > 1 and video_label_height > 1:
                img_aspect_ratio = pil_image.width / pil_image.height # Rasio aspek gambar asli
                label_aspect_ratio = video_label_width / video_label_height # Rasio aspek label video

                # Menentukan apakah penyesuaian ukuran didasarkan pada lebar atau tinggi label,
                # agar gambar pas di dalam label tanpa distorsi, mempertahankan rasio aspek aslinya.
                if img_aspect_ratio > label_aspect_ratio:
                    # Jika gambar lebih lebar relatif terhadap label, sesuaikan lebar gambar dengan lebar label
                    new_width = video_label_width
                    new_height = int(new_width / img_aspect_ratio) # Hitung tinggi baru berdasarkan rasio aspek
                else:
                    # Jika gambar lebih tinggi relatif terhadap label (atau rasio aspeknya sama), sesuaikan tinggi gambar dengan tinggi label
                    new_height = video_label_height
                    new_width = int(new_height * img_aspect_ratio) # Hitung lebar baru berdasarkan rasio aspek
                
                # Mengubah ukuran gambar menggunakan metode resampling LANCZOS untuk kualitas terbaik
                resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                # Mengkonversi gambar PIL yang sudah di-resize ke PhotoImage Tkinter agar bisa ditampilkan di label
                photo = ImageTk.PhotoImage(image=resized_image)
            else:
                # Jika dimensi label belum siap (misalnya saat inisialisasi awal atau jika tersembunyi),
                # tampilkan gambar dengan ukuran aslinya atau ukuran default tanpa resize.
                photo = ImageTk.PhotoImage(image=pil_image)


            self.video_label.config(image=photo) # Menetapkan gambar yang sudah diproses ke label video
            # Menyimpan referensi ke objek PhotoImage (self.video_label.image = photo).
            # Ini PENTING di Tkinter agar gambar tidak di-garbage collect oleh Python,
            # yang akan menyebabkan gambar tidak tampil atau hilang.
            self.video_label.image = photo
        except Exception as e:
            # Menangani potensi error saat konversi atau update gambar (misalnya, jika frame rusak)
            print(f"Error saat memperbarui frame video: {e}")


        # --- Memperbarui Grafik Sinyal ---
        # Mengirimkan data sinyal pernapasan dan rPPG yang baru didapatkan ke objek visualisasi untuk di-plot
        self.visualization.update([respiration_signal, rppg_signal])

        # --- Loop untuk Frame Berikutnya ---
        if self.running: # Jika monitoring masih harus berjalan
            # Jadwalkan pemanggilan fungsi capture_video lagi setelah 20 milidetik.
            # Ini menciptakan loop yang berjalan dengan target sekitar 50 FPS (1000ms / 20ms = 50 FPS).
            # Nilai interval (20ms) bisa disesuaikan untuk trade-off antara kelancaran video dan beban CPU.
            self.root.after(20, self.capture_video)