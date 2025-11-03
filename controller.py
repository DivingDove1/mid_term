"""
Collect Em All! 自動遊戲程式 - 操作控制模組
負責執行滑鼠操作、拖曳球、關閉廣告等

學習資源:
- PyAutoGUI 文檔: https://pyautogui.readthedocs.io/
- 滑鼠控制: https://pyautogui.readthedocs.io/en/latest/mouse.html
"""

import pyautogui
import time
from PIL import ImageDraw
import config
import vision_module


# ✅ COMPLETE: 計算格子中心的螢幕座標
def grid_to_screen(row, col, board_x, board_y):
    """
    將格子索引轉換為螢幕座標（格子中心）

    Args:
        row: 格子行索引
        col: 格子列索引
        board_x: 盤面左上角 x 座標
        board_y: 盤面左上角 y 座標

    Returns:
        tuple: (x, y) 螢幕座標

    學習重點:
    - 座標轉換：格子索引 -> 盤面相對座標 -> 螢幕絕對座標
    - 計算格子中心：索引 * 格子大小 + 半個格子大小
    """
    # 計算格子中心（相對於盤面）
    relative_x = col * config.CELL_SIZE + config.CELL_SIZE // 2
    relative_y = row * config.CELL_SIZE + config.CELL_SIZE // 2

    # 轉換為螢幕絕對座標
    screen_x_actual = board_x + relative_x
    screen_y_actual = board_y + relative_y

    # 使用 config 中的縮放係數
    screen_x_logical = screen_x_actual / config.DISPLAY_SCALE_FACTOR
    screen_y_logical = screen_y_actual / config.DISPLAY_SCALE_FACTOR

    return int(screen_x_logical), int(screen_y_logical)


# ✅ COMPLETE: 執行滑鼠拖曳
def perform_drag(path, board_x, board_y):
    """
    執行滑鼠拖曳操作來消除球

    Args:
        path: 拖曳路徑（格子座標列表）[(row, col), ...]
        board_x: 盤面左上角 x 座標
        board_y: 盤面左上角 y 座標

    學習重點:
    - pyautogui.moveTo(): 移動滑鼠到指定位置
    - pyautogui.mouseDown(): 按下滑鼠左鍵
    - pyautogui.mouseUp(): 釋放滑鼠左鍵
    - duration: 移動時間（秒），讓動作更像人類
    """
    if not path or len(path) < config.MIN_GROUP_SIZE:
        print("[操作] 無效的拖曳路徑")
        return False

    print(f"[操作] 執行拖曳: {len(path)} 個點")

    try:
        # 📝 STUDY: 拖曳第一顆球到最後一顆
        # 方法 1: 簡單拖曳（從起點到終點）
        start_row, start_col = path[0]
        end_row, end_col = path[-1]

        start_x, start_y = grid_to_screen(start_row, start_col, board_x, board_y)
        end_x, end_y = grid_to_screen(end_row, end_col, board_x, board_y)

        # 移動到起點
        pyautogui.moveTo(start_x, start_y, duration=config.MOUSE_MOVE_DURATION)
        time.sleep(0.1)

        # 按下滑鼠左鍵
        pyautogui.mouseDown()
        time.sleep(0.1)

        # 📝 STUDY: 拖曳到終點
        # 如果需要經過中間點，可以改用迴圈
        pyautogui.moveTo(end_x, end_y, duration=config.MOUSE_DRAG_DURATION)

        # 方法 2: 經過所有點（更保險，但較慢）
        # for row, col in path[1:]:
        #     x, y = grid_to_screen(row, col, board_x, board_y)
        #     pyautogui.moveTo(x, y, duration=0.1)

        time.sleep(0.1)

        # 釋放滑鼠
        pyautogui.mouseUp()

        print(f"[操作] 拖曳完成: ({start_row},{start_col}) -> ({end_row},{end_col})")

        # 等待消除動畫
        time.sleep(config.WAIT_ANIMATION)

        return True

    except Exception as e:
        print(f"[錯誤] 拖曳操作失敗: {e}")
        return False


# 📝 STUDY: 執行完整拖曳路徑（備用方案）
def perform_drag_full_path(path, board_x, board_y):
    """
    執行完整的拖曳路徑，經過每一個點
    （如果簡單拖曳不work，可以試試這個）

    Args:
        path: 拖曳路徑（格子座標列表）
        board_x: 盤面左上角 x 座標
        board_y: 盤面左上角 y 座標
    """
    if not path or len(path) < config.MIN_GROUP_SIZE:
        return False

    print(f"[操作] 執行完整路徑拖曳: {len(path)} 個點")

    try:
        # 移動到起點
        start_row, start_col = path[0]
        start_x, start_y = grid_to_screen(start_row, start_col, board_x, board_y)
        pyautogui.moveTo(start_x, start_y, duration=config.MOUSE_MOVE_DURATION)
        time.sleep(0.1)

        # 按下滑鼠
        pyautogui.mouseDown()
        time.sleep(0.1)

        # 依序經過每個點
        for row, col in path[1:]:
            x, y = grid_to_screen(row, col, board_x, board_y)
            pyautogui.moveTo(x, y, duration=0.1)
            time.sleep(0.05)

        # 釋放滑鼠
        pyautogui.mouseUp()

        print("[操作] 完整路徑拖曳完成")
        time.sleep(config.WAIT_ANIMATION)

        return True

    except Exception as e:
        print(f"[錯誤] 完整路徑拖曳失敗: {e}")
        return False


# 📝 STUDY: 嘗試關閉廣告彈窗
def close_ad_popup():
    """
    偵測並關閉遊戲結束彈窗

    策略：
    1. 尋找「不能再移動」文字
    2. 根據文字位置計算關閉按鈕位置
    3. 點擊關閉按鈕

    Returns:
        bool: 是否成功關閉
    """
    print("[操作] 偵測並關閉彈窗...")

    import os

    # 檢查圖片是否存在
    if not os.path.exists(config.POPUP_TEXT_IMAGE):
        print(f"[錯誤] 找不到彈窗文字圖片: {config.POPUP_TEXT_IMAGE}")
        print("[提示] 請截取「不能再移動」文字並儲存為 assets/popup_text.png")
        return False

    try:
        # 偵測縮放係數（處理 HiDPI 顯示器）
        screenshot = pyautogui.screenshot()
        screen_size = pyautogui.size()
        scale_factor = screenshot.size[0] / screen_size[0]

        print(f"[操作] 尋找彈窗文字... (縮放係數: {scale_factor})")

        # 方法 1: 尋找「不能再移動」文字
        popup_location = pyautogui.locateOnScreen(
            config.POPUP_TEXT_IMAGE, confidence=0.7
        )

        if popup_location:
            print(f"[操作] ✅ 找到彈窗！文字位置: {popup_location}")

            # 計算文字中心點
            text_center_x = popup_location.left + popup_location.width // 2
            text_center_y = popup_location.top + popup_location.height // 2

            # 根據偏移量計算關閉按鈕位置（實際像素座標）
            close_x_actual = text_center_x + config.CLOSE_BUTTON_OFFSET_X
            close_y_actual = text_center_y + config.CLOSE_BUTTON_OFFSET_Y

            # 轉換為邏輯座標（處理 HiDPI）
            if scale_factor != 1.0:
                close_x = close_x_actual / scale_factor
                close_y = close_y_actual / scale_factor
            else:
                close_x = close_x_actual
                close_y = close_y_actual

            print(f"[操作] 計算關閉按鈕位置: ({close_x:.0f}, {close_y:.0f})")

            # 先移動滑鼠讓你確認位置（除錯模式）
            if config.DEBUG_MODE:
                print("[除錯] 移動滑鼠到關閉按鈕位置（2秒後點擊）")
                pyautogui.moveTo(close_x, close_y, duration=0.5)
                time.sleep(2)

            # 點擊關閉按鈕
            pyautogui.click(close_x, close_y)
            time.sleep(1)

            print("[操作] ✅ 已點擊關閉按鈕")
            return True

        else:
            print("[操作] ❌ 未找到彈窗文字")

            # 方法 2: 備用 - 直接尋找關閉按鈕圖片
            if os.path.exists(config.CLOSE_BUTTON_IMAGE):
                print("[操作] 嘗試直接尋找關閉按鈕...")

                close_location = pyautogui.locateOnScreen(
                    config.CLOSE_BUTTON_IMAGE, confidence=0.7
                )

                if close_location:
                    center_x = close_location.left + close_location.width // 2
                    center_y = close_location.top + close_location.height // 2

                    if scale_factor != 1.0:
                        center_x = center_x / scale_factor
                        center_y = center_y / scale_factor

                    print(f"[操作] 找到關閉按鈕: ({center_x:.0f}, {center_y:.0f})")
                    pyautogui.click(center_x, center_y)
                    time.sleep(1)
                    print("[操作] ✅ 已關閉彈窗（備用方法）")
                    return True

            return False

    except Exception as e:
        print(f"[錯誤] 關閉彈窗時發生錯誤: {e}")
        import traceback

        traceback.print_exc()
        return False


# ==================== 除錯函數 ====================


def save_debug_move(board_image, path, board_state):
    """
    儲存標記當前移動的除錯圖片

    Args:
        board_image: 盤面截圖
        path: 移動路徑
        board_state: 盤面狀態
    """
    debug_image = board_image.copy()
    draw = ImageDraw.Draw(debug_image)

    # 標記路徑上的點
    for i, (row, col) in enumerate(path):
        # 計算格子中心
        center_x = col * config.CELL_SIZE + config.CELL_SIZE // 2
        center_y = row * config.CELL_SIZE + config.CELL_SIZE // 2

        # 畫圓圈
        radius = 5
        draw.ellipse(
            [
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
            ],
            outline="red",
            width=2,
        )

        # 畫數字（表示順序）
        draw.text((center_x + 10, center_y), str(i), fill="red")

    # 畫路徑線
    if len(path) > 1:
        for i in range(len(path) - 1):
            row1, col1 = path[i]
            row2, col2 = path[i + 1]

            x1 = col1 * config.CELL_SIZE + config.CELL_SIZE // 2
            y1 = row1 * config.CELL_SIZE + config.CELL_SIZE // 2
            x2 = col2 * config.CELL_SIZE + config.CELL_SIZE // 2
            y2 = row2 * config.CELL_SIZE + config.CELL_SIZE // 2

            draw.line([x1, y1, x2, y2], fill="red", width=2)

    # 儲存圖片
    debug_image.save(config.DEBUG_CURRENT_MOVE)
    print(f"[除錯] 移動路徑圖片已儲存: {config.DEBUG_CURRENT_MOVE}")


# ==================== 測試函數 ====================


def test_controller():
    """
    測試操作控制模組
    注意: 執行前請確保遊戲已開啟且定位成功
    """
    print("\n" + "=" * 50)
    print("測試: 操作控制模組")
    print("=" * 50 + "\n")

    print("[測試] 請確保遊戲視窗已開啟")
    print("[測試] 按 Enter 繼續...")
    input()

    # 定位盤面
    board_pos = vision_module.locate_game_board()

    if not board_pos:
        print("[測試] 定位失敗！")
        return

    board_x, board_y = board_pos

    # 測試：移動滑鼠到格子 (2, 3)
    print("\n[測試] 測試滑鼠移動到格子 (2, 3)")
    test_x, test_y = grid_to_screen(2, 3, board_x, board_y)
    pyautogui.moveTo(test_x, test_y, duration=1)
    print(f"[測試] 滑鼠已移動到 ({test_x}, {test_y})")

    time.sleep(1)

    # 測試：簡單拖曳
    print("\n[測試] 測試拖曳: (0,0) -> (2,2)")
    test_path = [(0, 0), (1, 1), (2, 2)]
    perform_drag(test_path, board_x, board_y)

    print("\n[測試] 測試完成！")
    print("[測試] 請檢查滑鼠是否正確移動和拖曳")


if __name__ == "__main__":
    # 當直接執行這個檔案時，運行測試
    test_controller()
