import cv2
import time
import pyautogui

from hand_tracker import HandTracker
from mouse_controller import move_mouse, left_click, right_click
from utils import distance, SmoothCursor

# Camera
cap = cv2.VideoCapture(0)

tracker = HandTracker()

cam_w, cam_h = 640, 480

# Smooth cursor
smooth = SmoothCursor(alpha=0.25)

# States
left_state = False
right_state = False
fist_start = 0

prev_y = 0

while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (cam_w, cam_h))

    frame, lm = tracker.find_hand(frame)

    if lm:
        index = lm[8][1:]
        middle = lm[12][1:]
        thumb = lm[4][1:]

        # =========================
        # 🖱️ MOVE CURSOR (INDEX)
        # =========================
        sx, sy = smooth.update(index[0], index[1])
        move_mouse(sx, sy, cam_w, cam_h)

        # =========================
        # 👆 LEFT CLICK (PINCH)
        # thumb + index
        # =========================
        if distance(thumb, index) < 30:
            if not left_state:
                left_click()
                left_state = True
        else:
            left_state = False

        # =========================
        # ✊ RIGHT CLICK (FIST HOLD)
        # all fingers folded
        # =========================
        if (lm[8][2] > lm[6][2] and
            lm[12][2] > lm[10][2] and
            lm[16][2] > lm[14][2]):

            if right_state is False:
                fist_start = time.time()
                right_state = True
            elif time.time() - fist_start > 0.4:
                right_click()
                right_state = "done"
        else:
            right_state = False

        # =========================
        # 📜 SCROLL (2 FINGERS MODE)
        # index + middle movement
        # =========================
        scroll_y = index[1]

        if distance(index, middle) > 40:
            pyautogui.scroll(int((prev_y - scroll_y) * 2))

        prev_y = scroll_y

    # Show camera
    cv2.imshow("Finger Mouse PRO", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()