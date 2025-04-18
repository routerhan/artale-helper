import time
import threading
import random  # 用於生成隨機數
import pydirectinput
from pynput import keyboard
import pygetwindow as gw
import pyautogui

# 確保遊戲視窗是活動的
time.sleep(3)  # 給使用者3秒準備時間切換到遊戲

# 模擬滑鼠移動到 (x, y) 位置，這裡是測試座標
x, y = 968, 703
pyautogui.moveTo(x, y, duration=0.5)  # 平滑移動到指定位置
pyautogui.click()  # 按一下
time.sleep(random.uniform(0.3, 0.5))
# 模擬按鍵（例如 "space"）
pydirectinput.press('a')

print("測試完成")