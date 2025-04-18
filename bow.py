import time
import threading
import random
import pydirectinput
from pynput import keyboard
import pygetwindow as gw

# 狀態標誌
running_flags = {
    "a": False,
    "left_combo": False,
    "right_combo": False,
    "space_hold": False,
    "exit": False,
    "paused": False
}

# 執行緒容器
threads = {
    "a": None,
    "j": None,
    "left_combo": None,
    "right_combo": None,
    "space_hold": None
}

def detect_active_window():
    active_window = gw.getActiveWindow()
    if active_window:
        print(f"當前焦點窗口：{active_window.title}")
    else:
        print("無法檢測到當前窗口，請確認遊戲已啟動並切換至焦點。")
    print("請切換到遊戲窗口並開始操作。")

def auto_press_a():
    while running_flags["a"] and not running_flags["exit"]:
        if not running_flags["paused"]:
            pydirectinput.keyDown('a')
        time.sleep(0.01)
    pydirectinput.keyUp('a')

def auto_press_j():
    while not running_flags["exit"]:
        time.sleep(180)
        if not running_flags["paused"]:
            print("每 3 分鐘自動按下 J")
            pydirectinput.press('j')

def combo_press(direction_key, flag_key):
    pydirectinput.keyDown(direction_key)
    print(f"開始長按 {direction_key.upper()} 並連點 SPACE")

    while running_flags[flag_key] and not running_flags["exit"]:
        if not running_flags["paused"]:
            pydirectinput.keyDown('space')
            time.sleep(random.uniform(0.02, 0.04))
            pydirectinput.keyUp('space')

        

    pydirectinput.keyUp(direction_key)
    print(f"停止 {direction_key.upper()} + SPACE")

def hold_space():
    print("開始長按 SPACE")
    pydirectinput.press('z')
    time.sleep(0.01)
    pydirectinput.keyDown('space')
    while running_flags["space_hold"] and not running_flags["exit"]:
        time.sleep(0.01)
    pydirectinput.keyUp('space')
    print("停止長按 SPACE")

def stop_all():
    for key in running_flags:
        if key != "exit":
            running_flags[key] = False
    print("所有自動功能已停止。")

def stop_combo_conflicts(exclude_key=None):
    """停止 left/right combo 和 space_hold 功能，排除正在啟動的 key"""
    for key in ["left_combo", "right_combo", "space_hold"]:
        if key != exclude_key:
            running_flags[key] = False

def on_press(key):
    try:
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            if not running_flags["a"]:
                stop_all()
                running_flags["a"] = True
                print("開始長按 A...")
                pydirectinput.press('z')
                threads["a"] = threading.Thread(target=auto_press_a, daemon=True)
                threads["a"].start()
            else:
                print("A 已在運行中。")

        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            stop_all()

        elif isinstance(key, keyboard.KeyCode) and key.char == 'x':
            if not running_flags["left_combo"]:
                stop_combo_conflicts("left_combo")
                running_flags["left_combo"] = True
                threads["left_combo"] = threading.Thread(target=combo_press, args=('left', 'left_combo'), daemon=True)
                threads["left_combo"].start()

        elif isinstance(key, keyboard.KeyCode) and key.char == 'v':
            if not running_flags["right_combo"]:
                stop_combo_conflicts("right_combo")
                running_flags["right_combo"] = True
                threads["right_combo"] = threading.Thread(target=combo_press, args=('right', 'right_combo'), daemon=True)
                threads["right_combo"].start()

        elif isinstance(key, keyboard.KeyCode) and key.char == 'c':
            if not running_flags["space_hold"]:
                stop_combo_conflicts("space_hold")
                running_flags["space_hold"] = True
                threads["space_hold"] = threading.Thread(target=hold_space, daemon=True)
                threads["space_hold"].start()

        elif isinstance(key, keyboard.KeyCode) and key.char == 't':
            print("退出腳本中...")
            stop_all()
            running_flags["exit"] = True
            return False

        else:
            running_flags["paused"] = True

    except AttributeError:
        pass

def on_release(key):
    if running_flags["paused"]:
        time.sleep(0.01)
        running_flags["paused"] = False

def main():
    print("啟動腳本...")
    detect_active_window()
    print("- 按 Ctrl 開始長按 A")
    print("- 按 Alt 停止所有功能")
    print("- 按 C 啟動 左方向 + SPACE 連點")
    print("- 按 V 啟動 右方向 + SPACE 連點")
    print("- 按 B 長按 SPACE")
    print("- 按 T 退出腳本")
    print("- Ctrl + C 強制結束")

    threads["j"] = threading.Thread(target=auto_press_j, daemon=True)
    threads["j"].start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("腳本已退出。再見！")

if __name__ == "__main__":
    main()
