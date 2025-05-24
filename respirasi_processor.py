import cv2
import mediapipe as mp
import numpy as np
from collections import deque

class RespirationProcessor:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.signal_buffer = deque(maxlen=300)
        self.roi_coords = None

    def reset(self):
        self.signal_buffer.clear()
        self.roi_coords = None

    def process(self, frame):
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        h, w, _ = frame.shape
        if results.pose_landmarks:
            left_shoulder = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]

            left_x, left_y = int(left_shoulder.x * w), int(left_shoulder.y * h)
            right_x, right_y = int(right_shoulder.x * w), int(right_shoulder.y * h)

            x1 = max(min(left_x, right_x), 0)
            x2 = min(max(left_x, right_x), w)
            y_shoulder = int((left_y + right_y) / 2)

            y1 = max(y_shoulder - 80, 0)
            box_height = 60
            y2 = min(y1 + box_height, h)

            self.roi_coords = (x1, y1, x2, y2)

        if self.roi_coords is not None:
            x1, y1, x2, y2 = self.roi_coords
            roi = frame[y1:y2, x1:x2]
            if roi.size != 0:
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                mean_intensity = np.mean(gray_roi)
                self.signal_buffer.append(mean_intensity)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return frame, list(self.signal_buffer)
