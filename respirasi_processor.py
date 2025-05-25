import cv2 # Mengimpor OpenCV untuk pemrosesan gambar dan video
import mediapipe as mp # Mengimpor MediaPipe untuk deteksi pose tubuh
import numpy as np # Mengimpor NumPy untuk operasi numerik, terutama array dan mean
from collections import deque # Mengimpor deque untuk buffer sinyal dengan ukuran tetap

class RespirationProcessor:
    """
    Kelas untuk memproses frame video guna mendeteksi sinyal pernapasan.
    Menggunakan MediaPipe Pose untuk mendeteksi landmark bahu,
    menentukan Region of Interest (ROI) di area dada/bahu,
    dan menghitung perubahan intensitas rata-rata piksel di ROI tersebut
    sebagai indikasi pergerakan pernapasan.
    """
    def __init__(self):
        """
        Konstruktor untuk kelas RespirationProcessor.
        Menginisialisasi model MediaPipe Pose dan buffer untuk menyimpan sinyal.
        """
        self.mp_pose = mp.solutions.pose # Mengakses solusi pose dari MediaPipe
        # Inisialisasi objek Pose dengan parameter kepercayaan deteksi dan pelacakan minimum
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        # Buffer untuk menyimpan nilai sinyal pernapasan (intensitas rata-rata ROI)
        # maxlen=300 berarti buffer akan menyimpan 300 sampel terakhir
        self.signal_buffer = deque(maxlen=300) #
        self.roi_coords = None # Menyimpan koordinat ROI (x1, y1, x2, y2), awalnya None

    def reset(self):
        """
        Mereset buffer sinyal dan koordinat ROI.
        Biasanya dipanggil sebelum memulai sesi monitoring baru.
        """
        self.signal_buffer.clear() # Mengosongkan buffer sinyal
        self.roi_coords = None # Mereset koordinat ROI

    def process(self, frame):
        """
        Memproses satu frame video untuk mengekstraksi sinyal pernapasan.

        Args:
            frame (numpy.ndarray): Frame video input dalam format BGR OpenCV.

        Returns:
            tuple:
                - numpy.ndarray: Frame video yang telah diproses (mungkin dengan ROI digambar).
                - list: Daftar (list) dari sinyal pernapasan yang ada di buffer.
        """
        # Membalik frame secara horizontal (efek cermin) agar lebih intuitif bagi pengguna
        frame = cv2.flip(frame, 1) #
        # Konversi frame dari BGR (format OpenCV) ke RGB (format yang dibutuhkan MediaPipe)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #
        # Memproses frame RGB dengan model MediaPipe Pose untuk mendapatkan landmark pose
        results = self.pose.process(rgb_frame) #

        h, w, _ = frame.shape # Mendapatkan tinggi (h) dan lebar (w) frame

        # Jika landmark pose terdeteksi
        if results.pose_landmarks:
            # Mendapatkan landmark untuk bahu kiri dan kanan
            left_shoulder = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER] #
            right_shoulder = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER] #

            # Mengkonversi koordinat landmark (normalisasi 0-1) ke koordinat piksel
            left_x, left_y = int(left_shoulder.x * w), int(left_shoulder.y * h) #
            right_x, right_y = int(right_shoulder.x * w), int(right_shoulder.y * h) #

            # Menentukan koordinat x untuk ROI berdasarkan posisi bahu
            # ROI akan membentang dari bahu terkiri ke bahu terkanan
            x1 = max(min(left_x, right_x), 0) # Pastikan x1 tidak kurang dari 0
            x2 = min(max(left_x, right_x), w) # Pastikan x2 tidak lebih dari lebar frame
            
            # Menghitung posisi y tengah antara kedua bahu
            y_shoulder = int((left_y + right_y) / 2) #

            # Menentukan koordinat y untuk ROI
            # ROI ditempatkan sedikit di bawah garis bahu (area dada atas)
            y1 = max(y_shoulder - 80, 0) # Titik y atas ROI, 80 piksel di atas y_shoulder (atau batas atas frame)
            box_height = 60 # Tinggi kotak ROI
            y2 = min(y1 + box_height, h) # Titik y bawah ROI, pastikan tidak melebihi tinggi frame

            # Menyimpan koordinat ROI yang baru dihitung
            self.roi_coords = (x1, y1, x2, y2) #

        # Jika koordinat ROI sudah ditentukan (baik dari frame ini atau frame sebelumnya)
        if self.roi_coords is not None:
            x1, y1, x2, y2 = self.roi_coords # Ambil koordinat ROI
            # Ekstraksi Region of Interest (ROI) dari frame
            roi = frame[y1:y2, x1:x2] #
            
            # Pastikan ROI tidak kosong (memiliki ukuran)
            if roi.size != 0:
                # Konversi ROI ke grayscale untuk analisis intensitas
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) #
                # Hitung intensitas rata-rata piksel dalam ROI grayscale
                mean_intensity = np.mean(gray_roi) #
                # Tambahkan nilai intensitas rata-rata ini ke buffer sinyal
                self.signal_buffer.append(mean_intensity) #

            # Gambar persegi panjang hijau di sekitar ROI pada frame untuk visualisasi
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) #

        # Kembalikan frame yang telah diproses (dengan ROI digambar) dan list dari buffer sinyal
        return frame, list(self.signal_buffer) #