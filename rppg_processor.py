import cv2 # Mengimpor OpenCV untuk pemrosesan gambar dan video
import mediapipe as mp # Mengimpor MediaPipe untuk deteksi wajah
import numpy as np # Mengimpor NumPy untuk operasi numerik, terutama array dan mean
from collections import deque # Mengimpor deque untuk buffer sinyal dengan ukuran tetap

class RPPGProcessor:
    """
    Kelas untuk memproses frame video guna mengekstraksi sinyal photoplethysmography jarak jauh (rPPG).
    Menggunakan MediaPipe Face Detection untuk mendeteksi wajah dan menentukan Region of Interest (ROI).
    Sinyal rPPG diestimasi dari perubahan rata-rata intensitas piksel pada kanal hijau di dalam ROI wajah,
    yang berkorelasi dengan perubahan volume darah.
    """
    def __init__(self):
        """
        Konstruktor untuk kelas RPPGProcessor.
        Menginisialisasi model MediaPipe Face Detection dan buffer untuk menyimpan sinyal.
        """
        self.mp_face = mp.solutions.face_detection # Mengakses solusi deteksi wajah dari MediaPipe
        # Inisialisasi objek FaceDetection dengan parameter kepercayaan deteksi minimum
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.5) #
        # Buffer untuk menyimpan nilai sinyal rPPG (rata-rata intensitas kanal hijau ROI)
        # maxlen=300 berarti buffer akan menyimpan 300 sampel terakhir
        self.signal_buffer = deque(maxlen=300) #
        self.roi_coords = None # Menyimpan koordinat ROI wajah (x1, y1, x2, y2), awalnya None

    def reset(self):
        """
        Mereset buffer sinyal dan koordinat ROI.
        Biasanya dipanggil sebelum memulai sesi monitoring baru.
        """
        self.signal_buffer.clear() # Mengosongkan buffer sinyal
        self.roi_coords = None # Mereset koordinat ROI

    def process(self, frame):
        """
        Memproses satu frame video untuk mengekstraksi sinyal rPPG.

        Args:
            frame (numpy.ndarray): Frame video input dalam format BGR OpenCV.

        Returns:
            tuple:
                - numpy.ndarray: Frame video yang telah diproses (mungkin dengan ROI wajah digambar).
                - list: Daftar (list) dari sinyal rPPG yang ada di buffer.
        """
        # Membalik frame secara horizontal (efek cermin) agar lebih intuitif bagi pengguna
        # Catatan: Jika frame sudah di-flip di RespirationProcessor dan outputnya digunakan di sini,
        # flip ini mungkin perlu dipertimbangkan ulang atau dihilangkan untuk menghindari double flip.
        # Namun, jika kedua prosesor menerima frame asli yang sama (setelah satu flip awal), ini OK.
        # Berdasarkan main_dashboard.py, rppg_processor menerima output dari respiration_processor,
        # yang sudah di-flip. Jadi, flip ini akan menjadi flip kedua. Idealnya, flip dilakukan sekali saja.
        # Untuk saat ini, saya biarkan sesuai kode asli, namun ini adalah area potensial untuk perbaikan.
        frame = cv2.flip(frame, 1) #
        # Konversi frame dari BGR (format OpenCV) ke RGB (format yang dibutuhkan MediaPipe)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #
        # Memproses frame RGB dengan model MediaPipe Face Detection
        results = self.face_detector.process(rgb_frame) #

        h, w, _ = frame.shape # Mendapatkan tinggi (h) dan lebar (w) frame

        # Jika ada wajah yang terdeteksi
        if results.detections:
            detection = results.detections[0] # Ambil deteksi pertama (asumsi hanya satu wajah utama)
            # Dapatkan bounding box relatif dari wajah yang terdeteksi
            bboxC = detection.location_data.relative_bounding_box #
            
            # Konversi koordinat bounding box relatif (0-1) ke koordinat piksel absolut
            x1 = int(bboxC.xmin * w) #
            y1 = int(bboxC.ymin * h) #
            box_w = int(bboxC.width * w) #
            box_h = int(bboxC.height * h) #

            # Hitung koordinat x2 dan y2 untuk bounding box
            x2 = x1 + box_w #
            y2 = y1 + box_h #

            # Simpan koordinat ROI wajah yang baru dihitung
            self.roi_coords = (x1, y1, x2, y2) #

        # Jika koordinat ROI wajah sudah ditentukan
        if self.roi_coords is not None:
            x1, y1, x2, y2 = self.roi_coords # Ambil koordinat ROI
            # Ekstraksi Region of Interest (ROI) dari frame (area wajah)
            roi = frame[y1:y2, x1:x2] #
            
            # Pastikan ROI tidak kosong (memiliki ukuran)
            if roi.size != 0:
                # Ekstrak kanal hijau (Green channel) dari ROI. Kanal hijau seringkali
                # memberikan sinyal rPPG yang lebih baik karena penyerapan hemoglobin.
                green_channel = roi[:, :, 1] # Indeks 1 untuk kanal Hijau dalam BGR
                # Hitung rata-rata intensitas piksel pada kanal hijau
                mean_green = np.mean(green_channel) #
                # Tambahkan nilai rata-rata ini ke buffer sinyal rPPG
                self.signal_buffer.append(mean_green) #

            # Gambar persegi panjang biru di sekitar ROI wajah pada frame untuk visualisasi
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Kotak biru untuk rPPG

        # Kembalikan frame yang telah diproses (dengan ROI wajah digambar) dan list dari buffer sinyal rPPG
        return frame, list(self.signal_buffer) #