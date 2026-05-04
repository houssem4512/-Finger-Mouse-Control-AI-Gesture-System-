import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:
    def __init__(self):
        # Load model
        base_options = python.BaseOptions(
            model_asset_path="models/hand_landmarker.task"
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

    def find_hand(self, frame):
        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # ✅ Correct MediaPipe input (FIXED)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Run detection
        result = self.detector.detect(mp_image)

        landmarks = []

        # If hand detected
        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            h, w, _ = frame.shape

            for i, lm in enumerate(hand):
                x = int(lm.x * w)
                y = int(lm.y * h)
                landmarks.append((i, x, y))

        return frame, landmarks