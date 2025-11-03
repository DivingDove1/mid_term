"""
Collect Em All! 自動遊戲程式 - 遊戲啟動模組
負責使用 Selenium 開啟瀏覽器並進入遊戲頁面

學習資源：
- Selenium 官方文檔: https://selenium-python.readthedocs.io/
- WebDriver 管理: https://github.com/SergeyPirogov/webdriver_manager
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import config


# ✅ COMPLETE: 初始化瀏覽器驅動
def init_driver():
    """
    初始化並返回 Selenium WebDriver

    Returns:
        webdriver: 瀏覽器驅動實例

    學習重點:
    - webdriver.Chrome(): 建立 Chrome 瀏覽器實例
    - Service(): 設定 ChromeDriver 路徑
    - ChromeDriverManager().install(): 自動下載並安裝 ChromeDriver
    """
    print("[啟動] 初始化瀏覽器驅動...")

    try:
        # 📝 STUDY: 設定 Chrome 選項
        options = webdriver.ChromeOptions()

        # 如果開啟無頭模式（不顯示瀏覽器視窗）
        if config.HEADLESS_MODE:
            options.add_argument("--headless")

        # 其他有用的選項
        options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )  # 避免被偵測為機器人

        # 📝 macOS 視窗大小設定
        # 如果不想最大化，可以設定固定大小
        # options.add_argument('--start-maximized')  # 最大化（macOS 可能無效）
        # options.add_argument('--window-size=1280,800')  # 固定大小

        # 建立 WebDriver 實例
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        print("[啟動] 瀏覽器驅動初始化成功")
        return driver

    except Exception as e:
        print(f"[錯誤] 初始化瀏覽器失敗: {e}")
        raise


# ✅ COMPLETE: 開啟遊戲頁面
def open_game(driver):
    """
    使用 WebDriver 開啟遊戲頁面

    Args:
        driver: Selenium WebDriver 實例

    學習重點:
    - driver.get(): 開啟網址
    - time.sleep(): 等待頁面載入
    """
    print(f"[啟動] 開啟遊戲頁面: {config.GAME_URL}")

    try:
        # 開啟網址
        driver.get(config.GAME_URL)

        # 等待頁面載入
        time.sleep(config.WAIT_PAGE_LOAD)

        print("[啟動] 頁面載入完成")
        return True

    except Exception as e:
        print(f"[錯誤] 開啟頁面失敗: {e}")
        return False


# 📝 STUDY: 等待遊戲開始
def wait_for_game_start(driver):
    """
    等待遊戲完全載入並開始

    Args:
        driver: Selenium WebDriver 實例

    Returns:
        bool: 是否成功偵測到遊戲開始

    學習重點:
    - WebDriverWait: 等待特定條件出現
    - expected_conditions: 預期條件（如元素可見）
    - By.ID/CLASS_NAME/TAG_NAME: 定位元素的方式

    注意: 這個函數可能需要根據實際遊戲網頁調整
    你可以使用瀏覽器的開發者工具（F12）查看遊戲元素
    """
    print("[啟動] 等待遊戲載入...")

    try:
        # 📝 STUDY: 等待特定元素出現（表示遊戲已載入）
        # 這裡需要根據實際遊戲調整！
        # 例如: 等待 canvas 元素、遊戲標題、開始按鈕等

        # 方法 1: 簡單等待固定時間
        time.sleep(config.WAIT_GAME_START)

        # 方法 2: 等待特定元素（需要檢查遊戲實際結構）
        # wait = WebDriverWait(driver, 10)
        # game_canvas = wait.until(
        #     EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        # )

        print("[啟動] 遊戲載入完成")
        return True

    except Exception as e:
        print(f"[警告] 等待遊戲載入時發生錯誤: {e}")
        print("[警告] 繼續執行，但可能需要手動確認遊戲已開始")
        return True  # 即使出錯也繼續（可能遊戲已經開始了）


# ✅ COMPLETE: 關閉瀏覽器
def close_driver(driver):
    """
    關閉瀏覽器並清理資源

    Args:
        driver: Selenium WebDriver 實例
    """
    print("[啟動] 關閉瀏覽器...")

    try:
        driver.quit()
        print("[啟動] 瀏覽器已關閉")

    except Exception as e:
        print(f"[警告] 關閉瀏覽器時發生錯誤: {e}")


# ✅ COMPLETE: 設定視窗位置和大小（macOS 專用）
def set_window_position(driver, x=0, y=20, width=1050, height=1080):
    """
    設定瀏覽器視窗的位置和大小
    適用於 macOS 不想最大化的情況

    Args:
        driver: Selenium WebDriver 實例
        x: 視窗左上角 x 座標
        y: 視窗左上角 y 座標
        width: 視窗寬度
        height: 視窗高度

    學習重點:
    - driver.set_window_position(): 設定視窗位置
    - driver.set_window_size(): 設定視窗大小

    使用範例:
        # 將視窗放在螢幕右半邊
        set_window_position(driver, x=800, y=0, width=1200, height=900)
    """
    print(f"[啟動] 設定視窗位置: ({x}, {y}), 大小: {width}x{height}")

    try:
        driver.set_window_position(x, y)
        driver.set_window_size(width, height)
        time.sleep(0.5)  # 等待視窗調整完成
        print("[啟動] 視窗位置設定完成")

    except Exception as e:
        print(f"[警告] 設定視窗位置時發生錯誤: {e}")
        print("[提示] 你可以手動調整瀏覽器視窗位置")


# 📝 STUDY: 處理彈窗和廣告
def handle_popups(driver):
    """
    嘗試關閉可能出現的彈窗或廣告

    Args:
        driver: Selenium WebDriver 實例

    Returns:
        bool: 是否成功關閉彈窗

    學習重點:
    - 尋找並點擊關閉按鈕
    - 處理可能不存在的元素（try-except）

    注意: 這個函數需要根據實際遊戲的彈窗樣式調整
    """
    print("[啟動] 檢查是否有彈窗...")

    try:
        # 📝 STUDY: 常見的關閉按鈕選擇器
        # 這裡列出幾種常見的關閉按鈕定位方式
        close_button_selectors = [
            (By.CLASS_NAME, "close-button"),
            (By.CLASS_NAME, "modal-close"),
            (By.XPATH, "//button[contains(text(), 'Close')]"),
            (By.XPATH, "//button[contains(text(), '×')]"),
        ]

        for selector_type, selector_value in close_button_selectors:
            try:
                close_button = driver.find_element(selector_type, selector_value)
                close_button.click()
                print(f"[啟動] 關閉彈窗成功")
                time.sleep(0.5)
                return True
            except:
                continue

        print("[啟動] 沒有發現彈窗")
        return False

    except Exception as e:
        print(f"[警告] 處理彈窗時發生錯誤: {e}")
        return False


# ==================== 測試函數 ====================


def test_launcher():
    """
    測試遊戲啟動模組
    運行此函數可以測試是否能成功開啟遊戲
    """
    print("\n" + "=" * 50)
    print("測試: 遊戲啟動模組")
    print("=" * 50 + "\n")

    # 初始化驅動
    driver = init_driver()

    # 開啟遊戲
    if open_game(driver):
        # 等待遊戲開始
        wait_for_game_start(driver)

        # 嘗試處理彈窗
        handle_popups(driver)

        # 保持視窗開啟 10 秒讓你檢查
        print("\n[測試] 視窗將保持開啟 10 秒，請檢查遊戲是否正確載入")
        time.sleep(10)

    # 關閉瀏覽器
    close_driver(driver)

    print("\n[測試] 測試完成！")


if __name__ == "__main__":
    # 當直接執行這個檔案時，運行測試
    test_launcher()
