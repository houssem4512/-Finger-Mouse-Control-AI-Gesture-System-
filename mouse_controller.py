import pyautogui
import time

screen_w, screen_h = pyautogui.size()

last_left_click = 0
last_right_click = 0

CLICK_DELAY = 0.4  # anti spam

def move_mouse(x, y, cam_w, cam_h):
    px = screen_w / cam_w * x
    py = screen_h / cam_h * y
    pyautogui.moveTo(px, py, duration=0.01)


def left_click():
    global last_left_click
    if time.time() - last_left_click > CLICK_DELAY:
        pyautogui.click()
        last_left_click = time.time()


def right_click():
    global last_right_click
    if time.time() - last_right_click > CLICK_DELAY:
        pyautogui.rightClick()
        last_right_click = time.time()