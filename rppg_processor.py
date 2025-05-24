import cv2
import mediapipe as mp
import numpy as np
from collections import deque

class RPPGProcessor:
    def __init__(self):
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.5)
        self.signal_buffer = deque(maxlen=300)
        self.roi_coords = None

    def reset(self):
        self.signal_buffer.clear()
        self.roi_coords = None

    def process(self, frame):
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detector.process(rgb_frame)

        h, w, _ = frame.shape
        if results.detections:
            detection = results.detections[0]
            bboxC = detection.location_data.relative_bounding_box
            x1 = int(bboxC.xmin * w)
            y1 = int(bboxC.ymin * h)
            box_w = int(bboxC.width * w)
            box_h = int(bboxC.height * h)

            x2 = x1 + box_w
            y2 = y1 + box_h

            self.roi_coords = (x1, y1, x2, y2)

        if self.roi_coords is not None:
            x1, y1, x2, y2 = self.roi_coords
            roi = frame[y1:y2, x1:x2]
            if roi.size != 0:
                green_channel = roi[:, :, 1]
                mean_green = np.mean(green_channel)
                self.signal_buffer.append(mean_green)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # kotak biru untuk rPPG

        return frame, list(self.signal_buffer)
