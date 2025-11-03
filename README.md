# Collect Em All! 自動遊戲程式

Python 自動化專案：使用電腦視覺和遊戲邏輯自動完成 Collect Em All! 消除遊戲

---

## 📋 專案說明

本專案使用以下技術：
- **Selenium**: 自動化瀏覽器操作
- **PyAutoGUI**: 螢幕截圖和滑鼠控制
- **Pillow**: 圖像處理和顏色辨識
- **BFS 演算法**: 尋找連通球組

---

## 🚀 快速開始

### 1. 安裝相依套件

```bash
pip install -r requirements.txt --break-system-packages
```

### 2. 準備參考圖示

**這是最重要的步驟！**

你需要截取遊戲介面的一個參考圖示：

1. 手動開啟遊戲網址：https://www.crazygames.com/game/collect-em-all
2. 等待遊戲完全載入
3. 找一個**獨特且固定**的介面元素（建議：分數顯示區域、遊戲標題圖示）
4. 使用截圖工具（Windows: Snipping Tool, Mac: Cmd+Shift+4）截取該元素
5. 將截圖儲存為 `assets/reference_icon.png`
6. 建議大小：50x50 到 100x100 像素

**參考圖示選擇技巧**：
- ✅ 選擇：固定不變的 UI 元素（標題、圖示、邊框）
- ❌ 避免：會變化的內容（分數數字、球的圖案）

### 3. 調整設定

編輯 `config.py`，調整以下參數：

```python
# 🔍 必須調整的參數
BOARD_OFFSET_FROM_REFERENCE = (50, 100)  # 盤面相對參考圖示的偏移
CELL_SIZE = 60  # 格子大小（像素）
COLOR_SAMPLE_RADIUS = 15  # 顏色採樣半徑

# 🔍 可能需要調整的參數
BALL_COLORS = {
    "RED": (255, 100, 100),
    # ... 根據實際遊戲顏色調整
}
COLOR_TOLERANCE = 80  # 顏色容忍度
```

**如何找到正確的參數？**
1. 先用預設值執行
2. 查看除錯圖片（`assets/debug/`）
3. 根據結果調整參數
4. 重複測試直到準確

### 4. 執行程式

```bash
python main.py
```

---

## 📁 專案結構

```
collect_em_all_bot/
├── assets/                    # 資源檔案
│   ├── reference_icon.png     # 參考圖示（需自己準備）
│   └── debug/                 # 除錯輸出資料夾
├── config.py                  # 設定檔
├── game_launcher.py           # 遊戲啟動模組
├── vision_module.py           # 視覺辨識模組
├── game_logic.py              # 遊戲邏輯模組
├── controller.py              # 操作控制模組
├── main.py                    # 主程式
├── requirements.txt           # 套件依賴
└── README.md                  # 本文件
```

---

## 🧪 分模組測試

在整合前，建議先測試各個模組：

### 測試遊戲啟動
```bash
python game_launcher.py
```
檢查：瀏覽器是否正確開啟遊戲頁面

### 測試視覺辨識
```bash
python vision_module.py
```
檢查：
- 是否找到參考圖示
- 盤面位置是否正確
- 顏色辨識是否準確
- 查看 `assets/debug/` 中的圖片

### 測試遊戲邏輯
```bash
python game_logic.py
```
檢查：BFS 演算法是否正確找出連通組

### 測試操作控制
```bash
python controller.py
```
檢查：滑鼠是否正確移動和拖曳

---

## 🐛 除錯指南

### 問題 1: 找不到參考圖示

**症狀**: `[錯誤] 找不到參考圖示！`

**解決方法**:
1. 確認 `assets/reference_icon.png` 存在
2. 確認遊戲介面與截圖時一致
3. 降低 `MATCH_CONFIDENCE` 值（如：從 0.8 降到 0.7）
4. 重新截取更清晰的參考圖示

### 問題 2: 顏色辨識不準確

**症狀**: 除錯圖片中顏色標記錯誤

**解決方法**:
1. 查看 `assets/debug/02_color_detection.png`
2. 用取色工具（如 Paint）取得實際遊戲中球的 RGB 值
3. 更新 `config.py` 中的 `BALL_COLORS` 定義
4. 調整 `COLOR_TOLERANCE` 值
5. 調整 `COLOR_SAMPLE_RADIUS` 值

### 問題 3: 盤面位置偏移

**症狀**: 除錯圖片中盤面框選位置不對

**解決方法**:
1. 查看 `assets/debug/01_board_location.png`
2. 調整 `BOARD_OFFSET_FROM_REFERENCE` 值
3. 調整 `CELL_SIZE` 值
4. 重新測試直到框選正確

### 問題 4: 拖曳操作無效

**症狀**: 滑鼠有移動但沒有消除球

**解決方法**:
1. 檢查滑鼠速度設定（`MOUSE_DRAG_DURATION`）
2. 在 `controller.py` 中改用 `perform_drag_full_path`（經過所有點）
3. 增加等待時間（`WAIT_ANIMATION`）

### 問題 5: 程式卡住或停止

**解決方法**:
1. 按 Ctrl+C 中斷程式
2. 檢查終端機的錯誤訊息
3. 查看除錯圖片找出問題點
4. 調整相關參數後重新執行

---

## 📊 除錯圖片說明

程式執行時會產生以下除錯圖片（在 `assets/debug/` 資料夾）：

| 檔案 | 說明 | 用途 |
|------|------|------|
| `01_board_location.png` | 標記盤面位置 | 檢查定位是否正確 |
| `02_color_detection.png` | 顯示顏色辨識結果 | 檢查顏色識別準確度 |
| `03_current_move.png` | 標記當前移動路徑 | 檢查移動選擇邏輯 |
| `04_board_state.txt` | 盤面狀態文字 | 查看內部表示 |

---

## ⚙️ 重要參數說明

### config.py 中的關鍵參數

| 參數 | 說明 | 建議值 |
|------|------|--------|
| `MATCH_CONFIDENCE` | 圖像匹配信心度 | 0.7-0.9 |
| `CELL_SIZE` | 格子大小（像素） | 50-80 |
| `COLOR_SAMPLE_RADIUS` | 顏色採樣半徑 | 10-20 |
| `COLOR_TOLERANCE` | 顏色容忍度 | 60-100 |
| `MOUSE_DRAG_DURATION` | 拖曳速度 | 0.3-0.8 |
| `WAIT_ANIMATION` | 動畫等待時間 | 0.5-1.5 |

---

## 🎓 學習資源

### 必讀文檔
- [Selenium 教學](https://selenium-python.readthedocs.io/)
- [PyAutoGUI 教學](https://pyautogui.readthedocs.io/)
- [Pillow 教學](https://pillow.readthedocs.io/)

### 演算法學習
- [BFS 演算法](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
- [圖論連通組](https://en.wikipedia.org/wiki/Connected_component_(graph_theory))

### 程式碼中的學習標記
- ✅ `COMPLETE`: 完整實作，可直接使用
- 📝 `STUDY`: 已實作但建議學習理解
- 🔍 `ADJUST`: 可能需要根據環境調整

---

## 📝 開發日誌

記錄你的開發過程和遇到的問題：

### Day 1: 環境設定和基本測試
- [x] 安裝所有套件
- [x] 測試 Selenium 啟動
- [x] 準備參考圖示
- [x] 測試盤面定位

### Day 2: 視覺辨識調校
- [x] 調整顏色定義
- [x] 測試顏色辨識準確度
- [x] 確認盤面位置正確

### Day 3: 整合和測試
- [ ] 執行完整流程
- [ ] 調整參數優化
- [ ] 測試多次確保穩定

### Day 4: 錄影和展示
- [ ] 準備展示環境
- [ ] 錄製操作影片
- [ ] 準備程式碼解說

---

## 🎯 完成檢查清單

提交前確認：
- [x] 程式可以自動開啟瀏覽器
- [x] 可以正確定位遊戲盤面
- [x] 可以準確辨識球的顏色
- [x] 可以找出可消除組合
- [x] 可以執行拖曳操作
- [ ] 可以持續遊玩直到結束
- [ ] 可以處理遊戲結束彈窗
- [x] 除錯模式可正常運作
- [ ] 錄影包含程式執行過程
- [ ] 錄影包含程式碼解說
- [ ] 壓縮檔不包含 .venv 等環境檔案

---

## ⚠️ 常見錯誤

### ImportError: No module named 'xxx'
**原因**: 套件未安裝
**解決**: `pip install -r requirements.txt --break-system-packages`

### Selenium WebDriver 錯誤
**原因**: ChromeDriver 版本不符
**解決**: 使用 webdriver-manager 會自動處理

### PyAutoGUI 在 Linux 的錯誤
**原因**: 缺少 X11 相依
**解決**: `sudo apt-get install python3-tk python3-dev`

---

## 💡 進階優化建議

完成基本功能後，可以嘗試：

1. **改善顏色辨識**
   - 使用 HSV 色彩空間代替 RGB
   - 實作顏色聚類演算法

2. **優化移動策略**
   - 考慮連鎖反應
   - 實作得分預測
   - 使用 A* 搜尋最佳路徑

3. **提升穩定性**
   - 加入錯誤重試機制
   - 實作遊戲狀態監控
   - 自動調整參數

4. **效能優化**
   - 減少不必要的截圖
   - 快取顏色辨識結果
   - 平行處理分析

---

## 📧 問題回報

如果遇到無法解決的問題：
1. 檢查除錯圖片
2. 記錄錯誤訊息
3. 記錄你的環境（作業系統、Python 版本）
4. 聯絡助教

---

## 📄 授權

本專案為教育用途，僅供學習參考。

---

**祝你順利完成專案！🎉**
