import cv2
import numpy as np
import pyautogui
import time

def clickFreeMarket(icon_path="icon.png", threshold=0.8, sleep_time=5):
    """
    自動尋找並點擊遊戲內的 FREE MARKET 按鈕。

    參數:
    - icon_path: 按鈕圖示的檔案路徑 (預設 "icon.png")
    - threshold: 模板匹配的信心度門檻 (預設 0.8)
    - sleep_time: 每次執行的間隔時間 (預設 5 秒)

    回傳:
    - 若找到並成功點擊，回傳 (center_x, center_y)
    - 若未找到按鈕，回傳 None
    """

    # 停 1 秒
    time.sleep(5)

    # 讀取按鈕圖示
    icon_img = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
    if icon_img is None:
        print("無法讀取按鈕圖示，請檢查檔案路徑")
        return None

    # 如果 icon_img 是 4 通道 (RGBA)，轉換為 3 通道 (BGR)
    if icon_img.shape[-1] == 4:
        icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGRA2BGR)

    # 擷取螢幕截圖
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)  # 轉換為 NumPy 陣列
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # 轉換為 OpenCV 格式

    # 確保格式相符
    screenshot = screenshot.astype(np.uint8)
    icon_img = icon_img.astype(np.uint8)

    # 使用模板匹配來尋找按鈕
    result = cv2.matchTemplate(screenshot, icon_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        icon_w, icon_h = icon_img.shape[1], icon_img.shape[0]
        top_left = max_loc
        bottom_right = (top_left[0] + icon_w, top_left[1] + icon_h)

        # 計算按鈕中心座標
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2

        print(f"按鈕座標: 左上角 {top_left}, 右下角 {bottom_right}, 中心點 ({center_x}, {center_y}), 信心度: {max_val}")

        # 停 1 秒
        time.sleep(1)
        # 平滑移動滑鼠到中心座標
        pyautogui.moveTo(center_x, center_y, duration=0.5)
        # 再等 1 秒
        time.sleep(1)
        # 點擊按鈕
        pyautogui.click()
        print("已點擊按鈕")

        return (center_x, center_y)

    else:
        print("未找到按鈕")
        return None

def detectMap(port_path="port.png", threshold=0.8, sleep_time=3):
    """
    自動偵測腳色是否在練功地圖中。

    藉由週期性地通過螢幕截圖和port.png做比對，有無傳送點來判斷
    - 若有傳送點，則印出:"在一般地圖"，並且回傳為真
    - 若
    """

def main():
    print("啟動腳本...")
    clickFreeMarket()

if __name__ == "__main__":
    main()