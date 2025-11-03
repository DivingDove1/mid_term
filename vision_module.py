"""
Collect Em All! 自動遊戲程式 - 視覺辨識模組
負責截圖、定位遊戲盤面、辨識球的顏色

學習資源:
- PyAutoGUI 文檔: https://pyautogui.readthedocs.io/
- Pillow 文檔: https://pillow.readthedocs.io/
- 顏色空間: https://en.wikipedia.org/wiki/RGB_color_model
"""

import pyautogui
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time
import config


# ✅ COMPLETE: 截圖整個螢幕
def capture_screen():
    """
    截圖整個螢幕

    Returns:
        PIL.Image: 螢幕截圖

    學習重點:
    - pyautogui.screenshot(): 截取整個螢幕
    """
    if config.DEBUG_MODE:
        print("[視覺] 截圖螢幕...")

    screenshot = pyautogui.screenshot()
    return screenshot


# 📝 STUDY: 定位遊戲盤面
def locate_game_board():
    """
    使用參考圖示定位遊戲盤面的位置

    Returns:
        tuple: (x, y) 盤面左上角座標，若失敗則返回 None

    學習重點:
    - pyautogui.locateOnScreen(): 在螢幕上尋找圖片
    - confidence: 匹配信心度（0.0-1.0）
    - 返回值: Box(left, top, width, height) 或 None

    重要提示:
    1. 需要先準備參考圖示（assets/reference_icon.png）
    2. 參考圖示應該是遊戲介面中獨特且固定的元素
    3. 如果找不到，可以降低 MATCH_CONFIDENCE 值
    """
    print("[視覺] 定位遊戲盤面...")

    try:
        # 📝 STUDY: 在螢幕上尋找參考圖示
        location = pyautogui.locateOnScreen(
            config.REFERENCE_ICON_PATH, confidence=config.MATCH_CONFIDENCE
        )

        if location is None:
            print("[錯誤] 找不到參考圖示！")
            print(f"[提示] 請確認 {config.REFERENCE_ICON_PATH} 存在")
            print(
                f"[提示] 或嘗試降低 MATCH_CONFIDENCE 值（目前: {config.MATCH_CONFIDENCE}）"
            )
            return None

        # 📝 STUDY: 計算盤面位置
        # location 的格式: Box(left, top, width, height)
        ref_x = location.left
        ref_y = location.top

        # 根據偏移量計算盤面左上角
        board_x = ref_x + config.BOARD_OFFSET_FROM_REFERENCE[0]
        board_y = ref_y + config.BOARD_OFFSET_FROM_REFERENCE[1]

        print(f"[視覺] 盤面定位成功！位置: ({board_x}, {board_y})")

        # 除錯模式：標記盤面位置
        if config.DEBUG_MODE:
            save_debug_board_location(board_x, board_y)

        return (board_x, board_y)

    except Exception as e:
        print(f"[錯誤] 定位盤面失敗: {e}")
        print("[提示] 可能原因:")
        print("  1. 參考圖示不存在或路徑錯誤")
        print("  2. 遊戲畫面與參考圖示不匹配")
        print("  3. 信心度設定太高")
        return None


# 📝 STUDY: 截取盤面區域
def capture_board(board_x, board_y):
    """
    截取遊戲盤面區域

    Args:
        board_x: 盤面左上角 x 座標
        board_y: 盤面左上角 y 座標

    Returns:
        PIL.Image: 盤面截圖

    學習重點:
    - 計算盤面區域大小
    - 使用 pyautogui.screenshot(region=...) 截取特定區域
    - region 格式: (x, y, width, height)
    """
    if config.DEBUG_MODE:
        print("[視覺] 截取盤面區域...")

    # 📝 STUDY: 計算盤面區域大小
    board_width = config.GRID_COLS * config.CELL_SIZE
    board_height = config.GRID_ROWS * config.CELL_SIZE

    # 截取盤面區域
    # region = (board_x, board_y, board_width, board_height)
    # board_image = pyautogui.screenshot(region=region)

    # 🔧 修改：先截全螢幕，再裁切
    full_screenshot = pyautogui.screenshot()
    board_image = full_screenshot.crop(
        (board_x, board_y, board_x + board_width, board_y + board_height)
    )

    return board_image


# 📝 STUDY: 辨識單個格子的顏色
def detect_cell_color(board_image, row, col):
    """
    辨識指定格子的球顏色

    Args:
        board_image: 盤面截圖
        row: 格子行索引 (0-based)
        col: 格子列索引 (0-based)

    Returns:
        str: 顏色名稱（如 "RED", "BLUE"），或 "UNKNOWN"

    學習重點:
    - 計算格子中心座標
    - 取樣區域內所有像素
    - 計算平均 RGB 值
    - 比較與預定義顏色的距離

    顏色匹配演算法:
    1. 取格子中心周圍的小區域
    2. 計算這個區域的平均顏色
    3. 找出與哪個預定義顏色最接近（歐幾里得距離）
    """
    # 📝 STUDY: 計算格子中心座標（相對於盤面截圖）
    center_x = col * config.CELL_SIZE + config.CELL_SIZE // 2
    center_y = row * config.CELL_SIZE + config.CELL_SIZE // 2

    # 📝 STUDY: 定義取樣區域（中心周圍的正方形）
    sample_left = max(0, center_x - config.COLOR_SAMPLE_RADIUS)
    sample_top = max(0, center_y - config.COLOR_SAMPLE_RADIUS)
    sample_right = min(board_image.width, center_x + config.COLOR_SAMPLE_RADIUS)
    sample_bottom = min(board_image.height, center_y + config.COLOR_SAMPLE_RADIUS)

    # 裁切取樣區域
    sample_region = board_image.crop(
        (sample_left, sample_top, sample_right, sample_bottom)
    )

    # 📝 STUDY: 計算平均顏色
    # 轉換為 numpy array 以便計算
    sample_array = np.array(sample_region)
    avg_color = sample_array.mean(axis=(0, 1))  # 在寬和高維度上取平均
    avg_r, avg_g, avg_b = avg_color[:3]  # 只取 RGB，忽略 alpha

    # 📝 STUDY: 找出最接近的預定義顏色
    min_distance = float("inf")
    best_match = "UNKNOWN"

    for color_name, (r, g, b) in config.BALL_COLORS.items():
        # 計算歐幾里得距離
        distance = np.sqrt((avg_r - r) ** 2 + (avg_g - g) ** 2 + (avg_b - b) ** 2)

        if distance < min_distance and distance < config.COLOR_TOLERANCE:
            min_distance = distance
            best_match = color_name

    return best_match


def detect_popup_in_board(board_image):
    """在盤面截圖中偵測彈窗（方案 1：藍色區域）"""

    try:
        img_array = np.array(board_image)
        height, width = img_array.shape[:2]

        blue_pixel_count = 0
        total_pixels = 0

        for y in range(0, height, 10):
            for x in range(0, width, 10):
                try:
                    r, g, b = img_array[y, x][:3]

                    if 30 < r < 90 and 90 < g < 150 and 150 < b < 210:
                        blue_pixel_count += 1

                    total_pixels += 1
                except:
                    continue

        if total_pixels > 0:
            blue_ratio = blue_pixel_count / total_pixels

            if blue_ratio > 0.4:
                print(f"[視覺] ✅ 偵測到彈窗！藍色比例: {blue_ratio:.1%}")
                return True

        return False

    except Exception as e:
        if config.DEBUG_MODE:
            print(f"[除錯] 偵測彈窗時出錯: {e}")
        return False


def detect_popup_in_board_state(board_state):
    """檢查盤面狀態是否異常（方案 3）"""
    unknown_count = 0
    total_cells = 0

    for row in board_state:
        for color in row:
            if color == "UNKNOWN":
                unknown_count += 1
            total_cells += 1

    if total_cells > 0:
        unknown_ratio = unknown_count / total_cells

        if unknown_ratio > 0.3:
            print(f"[視覺] ⚠️ UNKNOWN 比例過高: {unknown_ratio:.1%}，可能有彈窗")
            return True

    return False


def detect_board_state(board_x, board_y):
    """
    辨識整個盤面的狀態

    Returns:
        tuple: (board_state, has_popup)
               board_state: 二維陣列
               has_popup: bool，是否偵測到彈窗
    """
    if config.DEBUG_MODE:
        print("[視覺] 分析盤面顏色...")

    # 截取盤面
    board_image = capture_board(board_x, board_y)

    # 🔧 檢查彈窗
    has_popup = detect_popup_in_board(board_image)

    if has_popup:
        # 如果有彈窗，返回空盤面
        return None, True

    # 建立二維陣列儲存盤面狀態
    board_state = []

    for row in range(config.GRID_ROWS):
        row_colors = []
        for col in range(config.GRID_COLS):
            color = detect_cell_color(board_image, row, col)
            row_colors.append(color)
        board_state.append(row_colors)

    # 除錯模式：視覺化盤面狀態
    if config.DEBUG_MODE:
        save_debug_color_detection(board_image, board_state)
        print_board_state(board_state)

    # 🔧 額外檢查盤面狀態
    has_popup = detect_popup_in_board_state(board_state)

    return board_state, has_popup


# ✅ COMPLETE: 印出盤面狀態
def print_board_state(board_state):
    """
    以 emoji 形式印出盤面狀態

    Args:
        board_state: 二維陣列，表示盤面狀態
    """
    print("\n當前盤面:")
    for row in board_state:
        row_display = " ".join([config.COLOR_EMOJI.get(color, "❓") for color in row])
        print(row_display)
    print()


# ==================== 除錯函數 ====================


def save_debug_board_location(board_x, board_y):
    """
    儲存標記盤面位置的除錯圖片
    """
    screenshot = capture_screen()
    draw = ImageDraw.Draw(screenshot)

    # 計算盤面矩形
    board_width = config.GRID_COLS * config.CELL_SIZE
    board_height = config.GRID_ROWS * config.CELL_SIZE

    # 畫出盤面邊界（紅色矩形）
    draw.rectangle(
        [board_x, board_y, board_x + board_width, board_y + board_height],
        outline="red",
        width=3,
    )

    # 儲存圖片
    screenshot.save(config.DEBUG_BOARD_LOCATION)
    print(f"[除錯] 盤面位置圖片已儲存: {config.DEBUG_BOARD_LOCATION}")


def save_debug_color_detection(board_image, board_state):
    """
    儲存標記顏色辨識結果的除錯圖片
    """
    debug_image = board_image.copy()
    draw = ImageDraw.Draw(debug_image)

    # 嘗試載入字體，失敗則使用預設
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # 在每個格子上標記顏色
    for row in range(config.GRID_ROWS):
        for col in range(config.GRID_COLS):
            color = board_state[row][col]
            emoji = config.COLOR_EMOJI.get(color, "❓")

            # 計算文字位置（格子中心）
            text_x = col * config.CELL_SIZE + config.CELL_SIZE // 2 - 10
            text_y = row * config.CELL_SIZE + config.CELL_SIZE // 2 - 10

            # 畫文字
            draw.text((text_x, text_y), emoji, fill="white", font=font)

    # 儲存圖片
    debug_image.save(config.DEBUG_COLOR_DETECTION)
    print(f"[除錯] 顏色辨識圖片已儲存: {config.DEBUG_COLOR_DETECTION}")


# ==================== 測試函數 ====================


def test_vision():
    """
    測試視覺辨識模組
    注意: 執行前請確保遊戲已開啟
    """
    print("\n" + "=" * 50)
    print("測試: 視覺辨識模組")
    print("=" * 50 + "\n")

    print("[測試] 請確保遊戲視窗已開啟並可見")
    print("[測試] 按 Enter 繼續...")
    input()

    # 定位盤面
    board_pos = locate_game_board()

    if board_pos:
        board_x, board_y = board_pos

        # 辨識盤面狀態
        board_state = detect_board_state(board_x, board_y)

        print("\n[測試] 視覺辨識完成！")
        print(f"[測試] 請檢查除錯圖片: {config.DEBUG_OUTPUT_DIR}")
    else:
        print("\n[測試] 定位失敗！")
        print("[提示] 請檢查:")
        print("  1. 參考圖示是否存在")
        print("  2. 遊戲視窗是否完全可見")
        print("  3. 信心度設定是否合適")


if __name__ == "__main__":
    # 當直接執行這個檔案時，運行測試
    test_vision()
