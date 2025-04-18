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
    """模擬按下 A，並在每 25 次後模擬按下方向鍵"""
    global stop_thread, toggle_direction, a_press_count
    while not stop_thread:
        # 模擬按下 A
        pydirectinput.keyDown('a')
        time.sleep(random.uniform(0.2, 1.2))
        pydirectinput.keyUp('a')
        a_press_count += 1

        # 每 25 次 A 按鍵後模擬方向鍵
        if a_press_count % 2 == 0:
            press_time = random.uniform(0.2,0.3)  # 隨機方向鍵按壓時間
            if toggle_direction:
                print(f"按住 左方向鍵 {press_time:.2f} 秒")
                pydirectinput.keyDown('left')
                time.sleep(press_time)
                pydirectinput.keyUp('left')
            else:
                print(f"按住 右方向鍵 {press_time:.2f} 秒")
                pydirectinput.keyDown('right')
                time.sleep(press_time)
                pydirectinput.keyUp('right')

            # 切換方向
            toggle_direction = not toggle_direction

        # 每次按 A 間隔 1 秒
        time.sleep(random.uniform(0.1, 0.3))

def auto_press_j():
    """每 3 分鐘按下 J 一次"""
    while not exit_script:
        time.sleep(180)  # 等待 3 分鐘
        if not stop_thread:  # 若自動按鍵未停止，執行按 J
            print("每 3 分鐘自動按下 J")
            pydirectinput.press('j')

def on_press(key):
    global auto_press_running, stop_thread, exit_script

    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:  # 按下 Y 開始/恢復自動按鍵
            if not auto_press_running:
                auto_press_running = True
                stop_thread = False
                print("開始每秒按 A...")
                threading.Thread(target=auto_press_a, daemon=True).start()
            else:
                print("自動按鍵已經在運行中。")
        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            if auto_press_running:
                auto_press_running = False
                stop_thread = True
                print("自動按 A 停止。")
            else:
                pass
        elif key.char == 't':  # 按下 T 完全退出腳本
            print("退出腳本中...")
            stop_thread = True
            exit_script = True
            return False  # 停止鍵盤監聽
    except AttributeError:
        pass  # 忽略非字母鍵

def main():
    print("啟動腳本...")
    detect_active_window()  # 提示當前焦點窗口
    print("- 按 ctrl 開始/恢復自動按 A 並模擬方向鍵")
    print("- 按 alt 停止自動按 A")
    print("- 按 T 完全退出腳本")
    print("- 按 Ctrl + C 強制終止腳本")

    # 啟動每 3 分鐘按 J 的功能
    threading.Thread(target=auto_press_j, daemon=True).start()

    # 監聽鍵盤輸入
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    print("腳本已退出。再見！")

if __name__ == "__main__":
    main()
