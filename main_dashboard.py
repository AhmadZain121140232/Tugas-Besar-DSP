import cv2
import numpy as np
import matplotlib.pyplot as plt

# Fungsi utama untuk capture video webcam
def capture_video():
    cap = cv2.VideoCapture(0)  # buka webcam default

    if not cap.isOpened():
        print("Error: Webcam tidak dapat dibuka")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Webcam Feed", frame)  # tampilkan frame asli

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
