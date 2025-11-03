"""
Collect Em All! 自動遊戲程式 - 主程式
整合所有模組，執行完整的自動遊戲流程

執行方式:
    python main.py

作者: [你的學號/姓名]
日期: 2024
"""

import time
import sys
import config
import game_launcher
import vision_module
import game_logic
import controller
import pyautogui


def print_header():
    """印出程式標題"""
    print("\n" + "=" * 60)
    print(" " * 10 + "Collect Em All! 自動遊戲程式")
    print("=" * 60 + "\n")

    if config.DEBUG_MODE:
        print("🐛 除錯模式：開啟")
        print(f"📁 除錯輸出: {config.DEBUG_OUTPUT_DIR}\n")


def detect_game_over_popup():
    """
    偵測遊戲結束彈窗

    Returns:
        bool: True 表示偵測到彈窗
    """
    import os

    # 🔧 詳細日誌
    if config.DEBUG_MODE:
        print("[除錯] detect_game_over_popup() 執行中...")

    if not os.path.exists(config.POPUP_TEXT_IMAGE):
        if config.DEBUG_MODE:
            print(f"[除錯] 圖片不存在: {config.POPUP_TEXT_IMAGE}")
        return False

    try:
        # 🔧 關鍵：確保使用正確的 pyautogui
        location = pyautogui.locateOnScreen(config.POPUP_TEXT_IMAGE, confidence=0.9)

        # 找到了
        print(f"[遊戲] ✅ 偵測到彈窗！位置: {location}")
        return True

    except pyautogui.ImageNotFoundException:
        # 正常情況：沒找到
        if config.DEBUG_MODE:
            print("[除錯] 未找到彈窗（ImageNotFoundException）")
        return False

    except NameError as e:
        # pyautogui 沒有正確 import
        print(f"[錯誤] NameError: {e}")
        print("[錯誤] 可能原因：main.py 沒有 import pyautogui")
        return False

    except Exception as e:
        print(f"[錯誤] 偵測彈窗時發生錯誤: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return False


def initialize_game():
    """
    初始化遊戲

    Returns:
        tuple: (driver, board_x, board_y) 若成功
               None 若失敗
    """
    print("【階段 1】遊戲初始化\n")

    # 1. 啟動瀏覽器
    try:
        driver = game_launcher.init_driver()
    except Exception as e:
        print(f"\n❌ 啟動瀏覽器失敗: {e}")
        return None

    # 2. 開啟遊戲頁面
    if not game_launcher.open_game(driver):
        print("\n❌ 開啟遊戲頁面失敗")
        game_launcher.close_driver(driver)
        return None

    # 2.5. 設定視窗位置（macOS 專用）
    if config.USE_CUSTOM_WINDOW_SIZE:
        game_launcher.set_window_position(
            driver,
            x=config.WINDOW_X,
            y=config.WINDOW_Y,
            width=config.WINDOW_WIDTH,
            height=config.WINDOW_HEIGHT,
        )

    # 3. 等待遊戲載入
    game_launcher.wait_for_game_start(driver)

    # 4. 處理可能的彈窗
    game_launcher.handle_popups(driver)

    # 5. 定位遊戲盤面
    print("\n【階段 2】定位遊戲盤面\n")
    board_pos = vision_module.locate_game_board()

    if not board_pos:
        print("\n❌ 定位盤面失敗")
        print("請檢查:")
        print("  1. 參考圖示是否正確")
        print("  2. 遊戲視窗是否完全可見")
        print("  3. config.py 中的參數設定")
        game_launcher.close_driver(driver)
        return None

    board_x, board_y = board_pos
    print(f"✅ 盤面定位成功: ({board_x}, {board_y})\n")

    return driver, board_x, board_y


def play_game(driver, board_x, board_y):
    """
    主遊戲迴圈

    Args:
        driver: Selenium WebDriver
        board_x: 盤面 x 座標
        board_y: 盤面 y 座標

    Returns:
        int: 執行的移動次數
    """
    print("【階段 3】開始遊戲\n")

    move_count = 0
    previous_board_state = None  # 🔧 記錄上一次的盤面
    same_board_count = 0  # 🔧 相同盤面計數

    while True:
        print(f"\n--- 回合 {move_count + 1} ---")

        # 1. 截圖並分析盤面
        try:
            board_state, has_popup = vision_module.detect_board_state(board_x, board_y)

            # 🔧 檢查彈窗
            if has_popup:
                print("[遊戲] 偵測到彈窗！")
                break

            if board_state is None:
                print("[遊戲] 無法分析盤面")
                break

            # 🔧 檢查盤面是否與上次相同
            if previous_board_state is not None:
                if board_state == previous_board_state:
                    same_board_count += 1
                    print(f"[警告] 盤面與上次相同（連續 {same_board_count} 次）")

                    if same_board_count >= 3:
                        print("[遊戲] 盤面持續不變，遊戲可能已結束")
                        break
                else:
                    same_board_count = 0  # 重置計數

            previous_board_state = [row[:] for row in board_state]  # 深拷貝

        except Exception as e:
            print(f"❌ 分析盤面失敗: {e}")
            break

        # 2. 尋找可消除組合
        try:
            best_group, path = game_logic.analyze_and_select_move(board_state)
        except Exception as e:
            print(f"❌ 分析移動失敗: {e}")
            break

        # 3. 檢查是否有可執行的移動
        if not best_group or not path:
            print("[遊戲] 沒有可消除的組合")

            # 可能是遊戲結束了，檢查彈窗
            time.sleep(0.5)
            if detect_game_over_popup():
                print("[遊戲] 確認遊戲結束（偵測到彈窗）")
                break
            else:
                print("[遊戲] 沒有彈窗，可能盤面分析錯誤")
                # 等待一下再試
                time.sleep(config.WAIT_AFTER_MOVE)
                continue

        # 4. 除錯：顯示選中的組合
        if config.DEBUG_MODE:
            color = board_state[best_group[0][0]][best_group[0][1]]
            emoji = config.COLOR_EMOJI.get(color, "❓")
            print(f"[遊戲] 選中: {emoji} {color} × {len(best_group)}")

        # 5. 執行移動
        try:
            success = controller.perform_drag_full_path(path, board_x, board_y)

            if not success:
                print("⚠️ 移動執行失敗，嘗試繼續...")
                time.sleep(config.WAIT_AFTER_MOVE)
                continue

        except Exception as e:
            print(f"❌ 執行移動失敗: {e}")
            break

        # 6. 移動成功
        move_count += 1
        print(f"✅ 移動 {move_count} 完成")

        # 7. 等待動畫和盤面更新
        time.sleep(config.WAIT_AFTER_MOVE)

    return move_count


def cleanup(driver):
    """清理資源並結束程式"""
    print("\n【階段 4】結束遊戲\n")

    # 🔧 關閉彈窗（應該已經在螢幕上了）
    print("[清理] 關閉彈窗...")
    controller.close_ad_popup()
    time.sleep(1)

    # 等待一下
    print("\n[清理] 3 秒後關閉瀏覽器...")
    time.sleep(3)

    # 關閉瀏覽器
    game_launcher.close_driver(driver)

    print("\n✅ 程式執行完畢")


def main():
    """主函數"""
    # 印出標題
    print_header()

    # 印出當前設定
    if config.DEBUG_MODE:
        config.print_config()
        print()

    # 初始化遊戲
    result = initialize_game()

    if result is None:
        print("\n❌ 初始化失敗，程式結束")
        sys.exit(1)

    driver, board_x, board_y = result

    try:
        # 執行遊戲
        move_count = play_game(driver, board_x, board_y)

        # 顯示統計
        print("\n" + "=" * 60)
        print(f"🎮 遊戲統計")
        print("=" * 60)
        print(f"總移動次數: {move_count}")
        print("=" * 60 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️ 使用者中斷程式（Ctrl+C）")

    except Exception as e:
        print(f"\n\n❌ 程式發生錯誤: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # 清理資源
        cleanup(driver)


if __name__ == "__main__":
    main()
