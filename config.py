"""
Collect Em All! 自動遊戲程式 - 設定檔
包含所有可調整的參數和常數定義
"""

# ==================== 基本設定 ====================

# 🔍 ADJUST: 除錯模式（開發時設為 True，正式執行可設為 False）
DEBUG_MODE = True

# 🔍 ADJUST: 遊戲網址
GAME_URL = "https://www.crazygames.com/game/collect-em-all"

# 🔍 ADJUST: 瀏覽器設定
BROWSER_TYPE = "chrome"  # 支援: "chrome", "firefox", "edge"
HEADLESS_MODE = False  # True: 不顯示瀏覽器視窗（正式執行可用）

# 🔍 ADJUST: 視窗位置和大小（macOS 專用）
# 如果你使用多桌面或不想最大化，可以設定固定的視窗位置
USE_CUSTOM_WINDOW_SIZE = True  # 是否使用自訂視窗大小
WINDOW_X = 0  # 視窗左上角 x 座標
WINDOW_Y = 20  # 視窗左上角 y 座標
WINDOW_WIDTH = 1050  # 視窗寬度
WINDOW_HEIGHT = 1080  # 視窗高度
# 建議: 把視窗放在螢幕右側，左側留給終端機


# ==================== 視覺辨識設定 ====================

# 🔍 ADJUST: 參考圖示路徑（用於定位遊戲盤面）
REFERENCE_ICON_PATH = "assets/reference_icon.png"

# 🔍 ADJUST: 圖像匹配信心度（0.0-1.0，越高越嚴格）
MATCH_CONFIDENCE = 0.7

# 🔍 ADJUST: 盤面格子數量
GRID_ROWS = 6
GRID_COLS = 6

# 📝 STUDY: 盤面相對位置偏移（相對於參考圖示）
# 這些值需要根據實際遊戲介面調整
# 格式：(x_offset, y_offset)
BOARD_OFFSET_FROM_REFERENCE = (692, 415)  # 🔍 可能需要調整

# 📝 STUDY: 格子大小（像素）
CELL_SIZE = 97  # 🔍 可能需要調整

# 📝 STUDY: 顏色採樣區域大小（從格子中心向外擴展的像素數）
COLOR_SAMPLE_RADIUS = 15  # 取 30x30 像素區域的平均顏色

# 🔍 ADJUST: 顯示器縮放設定（針對 HiDPI/4K 顯示器）
# 如果使用 4K 顯示器設定為 1920x1080，設為 2.0
# 如果使用 Retina 顯示器，設為 2.0
# 如果使用一般顯示器，設為 1.0
DISPLAY_SCALE_FACTOR = 2.0  # 你的 4K 顯示器應該是 2.0


# ==================== 顏色定義 ====================

# 📝 STUDY: 球的顏色定義（RGB 值）
# 格式：顏色名稱 -> (R, G, B)
# 這些值需要根據實際遊戲調整
BALL_COLORS = {
    "RED": (238, 60, 40),  # 紅色球
    "BLUE": (105, 127, 248),  # 藍色球
    "GREEN": (93, 183, 30),  # 綠色球
    "PURPLE": (151, 51, 238),  # 紫色球
    "ORANGE": (236, 148, 40),  # 橙色球
}

# 📝 STUDY: 顏色容忍度（判斷顏色相似度的閾值）
# 越小越嚴格，越大越寬鬆
COLOR_TOLERANCE = 80

# 除錯用：顏色對應的 emoji
COLOR_EMOJI = {
    "RED": "🔴",
    "BLUE": "🔵",
    "GREEN": "🟢",
    "PURPLE": "🟣",
    "ORANGE": "🟠",
    "EMPTY": "⚫",
    "UNKNOWN": "❓",
}


# ==================== 遊戲邏輯設定 ====================

# 最小消除數量
MIN_GROUP_SIZE = 3

# 📝 STUDY: 8方向相鄰定義（上、下、左、右、左上、右上、左下、右下）
DIRECTIONS = [
    (-1, 0),  # 上
    (1, 0),  # 下
    (0, -1),  # 左
    (0, 1),  # 右
    (-1, -1),  # 左上
    (-1, 1),  # 右上
    (1, -1),  # 左下
    (1, 1),  # 右下
]


# ==================== 操作控制設定 ====================

# 🔍 ADJUST: 滑鼠移動速度（秒）
MOUSE_MOVE_DURATION = 0.1

# 🔍 ADJUST: 滑鼠拖曳速度（秒）
MOUSE_DRAG_DURATION = 0.3

# 🔍 ADJUST: 等待時間設定（秒）
WAIT_PAGE_LOAD = 3  # 等待頁面載入
WAIT_GAME_START = 2  # 等待遊戲開始
WAIT_AFTER_MOVE = 2  # 每次移動後等待
WAIT_ANIMATION = 1  # 等待消除動畫


# ==================== 遊戲結束偵測 ====================

# 🔍 ADJUST: 廣告彈窗偵測（如果有參考圖片）
AD_POPUP_IMAGE = "assets/add_popup.png"  # 可以設定為廣告按鈕的截圖路徑
CLOSE_BUTTON_IMAGE = "assets/close_button.png"  # 「關閉按鈕」圖片
POPUP_TEXT_IMAGE = "assets/popup_text.png"  # 「不能再移動」文字圖片

# 🔍 ADJUST: 關閉按鈕相對於文字的位置偏移
# 這個值需要根據實際彈窗調整
CLOSE_BUTTON_OFFSET_X = 160  # 關閉按鈕在文字右側約 120 像素
CLOSE_BUTTON_OFFSET_Y = -100  # 關閉按鈕在文字上方約 80 像素

# 🔍 ADJUST: 彈窗偵測關鍵字
GAME_OVER_KEYWORDS = ["不能再移動"]

# 遊戲結束的判斷方式
# - "no_moves": 找不到可消除組合
# - "popup": 偵測到廣告彈窗
GAME_END_DETECTION = "pop_up"


# ==================== 除錯輸出設定 ====================

# 除錯圖片輸出資料夾
DEBUG_OUTPUT_DIR = "assets/debug"

# 除錯圖片檔名
DEBUG_BOARD_LOCATION = f"{DEBUG_OUTPUT_DIR}/01_board_location.png"
DEBUG_COLOR_DETECTION = f"{DEBUG_OUTPUT_DIR}/02_color_detection.png"
DEBUG_CURRENT_MOVE = f"{DEBUG_OUTPUT_DIR}/03_current_move.png"
DEBUG_BOARD_STATE = f"{DEBUG_OUTPUT_DIR}/04_board_state.txt"


# ==================== 學習資源連結 ====================

LEARNING_RESOURCES = {
    "selenium": "https://selenium-python.readthedocs.io/",
    "pyautogui": "https://pyautogui.readthedocs.io/",
    "pillow": "https://pillow.readthedocs.io/",
    "bfs": "https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/",
    "color_space": "https://en.wikipedia.org/wiki/RGB_color_model",
}


# ==================== 輔助函數 ====================


def print_config():
    """印出當前設定（除錯用）"""
    print("=== 當前設定 ===")
    print(f"除錯模式: {DEBUG_MODE}")
    print(f"遊戲網址: {GAME_URL}")
    print(f"盤面大小: {GRID_ROWS}x{GRID_COLS}")
    print(f"格子大小: {CELL_SIZE}px")
    print(f"顏色數量: {len(BALL_COLORS)}")
    print(f"最小消除: {MIN_GROUP_SIZE}")
    print("=" * 40)


if __name__ == "__main__":
    # 測試：印出設定
    print_config()
