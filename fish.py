import time
import threading
import random  # 用於生成隨機數
import pydirectinput
from pynput import keyboard
import pygetwindow as gw

# 狀態標誌
auto_press_running = False  # 是否正在自動按 A
stop_thread = False  # 是否停止按鍵循環
exit_script = False  # 是否退出腳本
toggle_direction = True  # 用於切換方向鍵的標誌
a_press_count = 0  # 記錄按下 A 的次數

def detect_active_window():
    """檢測當前窗口並提示用戶切換至遊戲窗口"""
    active_window = gw.getActiveWindow()
    if active_window:
        print(f"當前焦點窗口：{active_window.title}")
    else:
        print("無法檢測到當前窗口，請確認遊戲已啟動並切換至焦點。")
    print("請切換到遊戲窗口並開始操作。")

def auto_press_a():
    """持續按壓 A，並在偵測其他鍵時暫停"""
    global stop_thread, other_key_pressed
    while not stop_thread:
        if not other_key_pressed:  # 只有在沒有其他鍵時才按壓 A
            pydirectinput.keyDown('a')
        time.sleep(0.05)  # 這裡可以調整持續按壓的頻率
    pydirectinput.keyUp('a')  # 停止時釋放 A 鍵

def auto_press_j():
    """每 3 分鐘按下 J 一次"""
    while not exit_script:
        time.sleep(180)  # 等待 3 分鐘
        if not stop_thread:  # 若自動按鍵未停止，執行按 J
            print("每 3 分鐘自動按下 J")
            pydirectinput.press('j')

def on_press(key):
    global auto_press_running, stop_thread, exit_script, other_key_pressed, a_thread

    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:  # 按下 Ctrl 開始自動按鍵
            if not auto_press_running:
                auto_press_running = True
                stop_thread = False
                print("開始持續按壓 A...")
                pydirectinput.press('z')
                a_thread = threading.Thread(target=auto_press_a, daemon=True)
                a_thread.start()
            else:
                print("自動按鍵已經在運行中。")

        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:  # 按下 Alt 停止自動按鍵
            if auto_press_running:
                auto_press_running = False
                stop_thread = True
                print("自動按 A 停止。")

        elif isinstance(key, keyboard.KeyCode) and key.char == 't':  # 按 T 退出腳本
            print("退出腳本中...")
            stop_thread = True
            exit_script = True
            return False  # 停止鍵盤監聽

        else:
            other_key_pressed = True  # 其他鍵被按下，停止 A 按壓

    except AttributeError:
        pass  # 忽略無效鍵

def on_release(key):
    global other_key_pressed

    # 當其他鍵被鬆開時，稍等 0.05 秒後恢復 A 持續按壓
    if other_key_pressed:
        time.sleep(0.05)
        other_key_pressed = False  # 恢復 A 按壓


def main():
    print("啟動腳本...")
    detect_active_window()  # 提示當前焦點窗口
    print("- 按 ctrl 開始/恢復自動按 A 並模擬方向鍵")
    print("- 按 alt 停止自動按 A")
    print("- 按 T 完全退出腳本")
    print("- 按 Ctrl + C 強制終止腳本")
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("腳本已退出。再見！")

if __name__ == "__main__":
    main()
