# vital_cam_gui.py
# File ini bertanggung jawab untuk mengelola pengambilan video dari webcam
# dan menampilkan video tersebut di antarmuka grafis.

import cv2

# Fungsi untuk memulai pengambilan video menggunakan webcam
def start_video_capture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        exit()  # Menghentikan program jika tidak dapat mengakses webcam
    return cap