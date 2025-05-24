import cv2
from vital_cam_gui import start_video_capture
from respirasi_processor import process_respiration_signal
from rppg_processor import process_rppg_signal
from visualization import visualize_signals

# Fungsi utama untuk menjalankan aplikasi
def main():
    """
    Fungsi utama yang mengatur alur aplikasi, mulai dari pengambilan video, 
    pemrosesan sinyal respirasi dan rPPG, hingga visualisasi hasil.
    """

    # Memulai pengambilan video dari webcam
    cap = start_video_capture()

    while True:
        # Membaca frame dari video
        ret, frame = cap.read()
        if not ret:
            break

        # Proses sinyal respirasi dan rPPG dari frame yang diambil
        respiration_signal = process_respiration_signal(frame)
        rppg_signal = process_rppg_signal(frame)

        # Visualisasi hasil sinyal respirasi dan rPPG
        visualize_signals(respiration_signal, rppg_signal)

        # Tampilkan frame yang telah diproses
        cv2.imshow("Processed Video", frame)

        # Tekan 'q' untuk keluar dari webcam
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Melepaskan akses ke webcam dan menutup semua jendela
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Jalankan fungsi utama untuk memulai aplikasi
    main()
