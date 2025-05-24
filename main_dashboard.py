import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def capture_respirasi_with_mediapipe():
    cap = cv2.VideoCapture(0)
    fs = 30
    duration = 10
    buffer_size = fs * duration
    signal_buffer = deque(maxlen=buffer_size)

    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    ax.set_ylim(0, 255)
    ax.set_xlim(0, buffer_size)
    ax.set_title("Sinyal Respirasi dari Bahu (Intensity)")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Mean Grayscale Intensity")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame supaya mirror image (optional)
        frame = cv2.flip(frame, 1)

        # Convert BGR ke RGB untuk MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Proses pose
        results = pose.process(rgb_frame)

        h, w, _ = frame.shape

        if results.pose_landmarks:
            # Ambil koordinat bahu kiri dan kanan
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

            # Konversi ke pixel
            left_x, left_y = int(left_shoulder.x * w), int(left_shoulder.y * h)
            right_x, right_y = int(right_shoulder.x * w), int(right_shoulder.y * h)

            # Tentukan kotak ROI di antara bahu kiri dan kanan, agak turun sedikit dari bahu
            x1 = min(left_x, right_x)
            x2 = max(left_x, right_x)
            y1 = min(left_y, right_y)
            y2 = y1 + int((y1 * 0.5))  # ambil area sedikit di bawah bahu, bisa disesuaikan

            # Pastikan batas dalam frame
            x1 = max(x1, 0)
            x2 = min(x2, w)
            y1 = max(y1, 0)
            y2 = min(y2, h)

            roi = frame[y1:y2, x1:x2]

            if roi.size != 0:
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                mean_intensity = np.mean(gray_roi)
                signal_buffer.append(mean_intensity)

                # Gambar kotak di frame asli
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

        # Tampilkan webcam feed
        cv2.imshow("Webcam Feed", frame)

        # Update plot sinyal
        if len(signal_buffer) > 10:
            line.set_xdata(np.arange(len(signal_buffer)))
            line.set_ydata(signal_buffer)
            ax.set_xlim(0, len(signal_buffer))
            fig.canvas.draw()
            fig.canvas.flush_events()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_respirasi_with_mediapipe()
