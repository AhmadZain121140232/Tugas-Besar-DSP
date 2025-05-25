import cv2 # Mengimpor OpenCV untuk fungsionalitas terkait kamera

def start_video_capture(camera_index=0):
    """
    Menginisialisasi dan mengembalikan objek VideoCapture dari OpenCV.

    Fungsi ini mencoba untuk membuka koneksi ke kamera yang ditentukan oleh `camera_index`,
    dan mengatur properti lebar dan tinggi frame kamera.

    Args:
        camera_index (int, optional): Indeks kamera yang akan digunakan.
                                      Defaultnya adalah 0 (biasanya kamera internal/default).

    Returns:
        cv2.VideoCapture or None: Objek VideoCapture jika kamera berhasil dibuka,
                                  None jika gagal.
    """
    # Membuat objek VideoCapture untuk kamera dengan indeks yang diberikan
    cap = cv2.VideoCapture(camera_index) #
    
    # Mengatur lebar frame yang diinginkan dari kamera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #
    # Mengatur tinggi frame yang diinginkan dari kamera
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #
    
    # Periksa apakah kamera berhasil dibuka
    if not cap.isOpened():
        print(f"Error: Tidak dapat membuka kamera dengan indeks {camera_index}.")
        return None # Kembalikan None jika gagal membuka kamera
        
    return cap # Kembalikan objek VideoCapture yang berhasil diinisialisasi