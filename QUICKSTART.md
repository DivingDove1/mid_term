# 🚀 快速開始指南

恭喜你獲得完整的專案骨架！這份文件幫助你在 **10 分鐘內** 開始執行程式。

---

## ⚡ 10 分鐘快速啟動

### 步驟 1: 解壓縮（1 分鐘）

解壓 `collect_em_all_bot.zip` 到你的工作目錄。

### 步驟 2: 安裝套件（2-3 分鐘）

開啟終端機（Terminal / Command Prompt），進入專案目錄：

```bash
cd collect_em_all_bot
pip install -r requirements.txt --break-system-packages
```

**Windows 使用者如果遇到問題**：
```bash
pip install -r requirements.txt
```

### 步驟 3: 準備參考圖示（3-4 分鐘）

**這是最關鍵的步驟！**

1. 開啟遊戲：https://www.crazygames.com/game/collect-em-all
2. 等待完全載入
3. 截取一個**固定的 UI 元素**（如遊戲標題、分數框）
4. 儲存為 `assets/reference_icon.png`

📖 詳細說明請看：`assets/REFERENCE_GUIDE.md`

### 步驟 4: 測試執行（2-3 分鐘）

先測試各個模組：

```bash
# 測試瀏覽器啟動
python game_launcher.py

# 測試視覺辨識（最重要！）
python vision_module.py

# 測試遊戲邏輯
python game_logic.py
```

如果視覺辨識測試成功（找到盤面位置），你就可以：

```bash
# 執行完整程式
python main.py
```

---

## 📊 檢查點

執行 `python vision_module.py` 後，你應該看到：

✅ **成功的訊息**：
```
[視覺] 定位遊戲盤面...
[視覺] 盤面定位成功！位置: (450, 280)
[視覺] 分析盤面顏色...
```

❌ **失敗的訊息**：
```
[錯誤] 找不到參考圖示！
```

如果失敗，請：
1. 檢查 `assets/reference_icon.png` 是否存在
2. 降低 `config.py` 中的 `MATCH_CONFIDENCE`（從 0.8 降到 0.7）
3. 重新截取更簡單的參考圖示

---

## 🎯 第一次執行建議

**不要期待一次成功！** 第一次執行可能會遇到：
- 找不到參考圖示
- 盤面位置偏移
- 顏色辨識不準

**這是正常的！** 請：
1. 查看除錯圖片：`assets/debug/`
2. 根據結果調整 `config.py` 的參數
3. 重新執行測試

---

## 📁 重要檔案清單

| 檔案 | 用途 | 需要修改？ |
|------|------|----------|
| `main.py` | 主程式 | ❌ 不用 |
| `config.py` | 設定檔 | ✅ **必須調整** |
| `assets/reference_icon.png` | 參考圖示 | ✅ **必須準備** |
| `README.md` | 詳細說明 | 📖 閱讀 |
| `LEARNING.md` | 學習資源 | 📖 閱讀 |
| `assets/REFERENCE_GUIDE.md` | 圖示準備指南 | 📖 閱讀 |

---

## 🔧 必須調整的參數

編輯 `config.py`，根據實際情況調整：

```python
# 1. 參考圖示路徑（確認存在）
REFERENCE_ICON_PATH = "assets/reference_icon.png"

# 2. 圖像匹配信心度（如果找不到，降低這個值）
MATCH_CONFIDENCE = 0.8  # 試試 0.7, 0.6

# 3. 盤面相對偏移（根據除錯圖片調整）
BOARD_OFFSET_FROM_REFERENCE = (50, 100)  # 需要實驗

# 4. 格子大小（根據實際遊戲調整）
CELL_SIZE = 60  # 可能是 50-80

# 5. 球的顏色定義（用取色工具測量）
BALL_COLORS = {
    "RED": (255, 100, 100),    # 用遊戲實際顏色
    "BLUE": (100, 100, 255),   # 用取色工具測量
    # ... 其他顏色
}
```

---

## 📝 4 天完成計畫

### Day 1（今天）- 環境設定
- [x] 解壓縮專案 ✅
- [x] 安裝套件 ✅
- [ ] 準備參考圖示 ⏳
- [ ] 執行測試 ⏳
- [ ] 閱讀 `README.md` 和 `LEARNING.md` ⏳

### Day 2 - 視覺辨識調校
- [ ] 調整顏色定義
- [ ] 測試並調整盤面定位
- [ ] 確保顏色辨識準確率 > 90%

### Day 3 - 整合測試
- [ ] 執行完整程式
- [ ] 調整參數優化表現
- [ ] 測試多次確保穩定

### Day 4 - 錄影展示
- [ ] 準備錄影環境
- [ ] 錄製程式執行過程
- [ ] 錄製程式碼解說
- [ ] 打包提交

---

## 💡 專家建議

### 1. 除錯模式永遠開啟
在調整參數期間，保持：
```python
DEBUG_MODE = True
```
這樣你可以看到除錯圖片，知道哪裡出問題。

### 2. 分步驟測試
不要跳過模組測試直接執行 `main.py`！這樣很難找問題。

**正確流程**：
```
game_launcher.py ✅
↓
vision_module.py ✅  ← 最重要！
↓
game_logic.py ✅
↓
controller.py ✅
↓
main.py ✅
```

### 3. 善用除錯圖片
每次執行 `vision_module.py` 後，**一定要看**：
- `assets/debug/01_board_location.png` - 盤面位置對嗎？
- `assets/debug/02_color_detection.png` - 顏色對嗎？

### 4. 記錄你的調整
建議建立一個筆記檔案，記錄：
- 調整了什麼參數
- 結果如何
- 下一步要試什麼

---

## 🆘 遇到問題？

### 問題解決流程
```
遇到錯誤
↓
看終端機錯誤訊息
↓
查看除錯圖片（如果有）
↓
查閱 README.md 的「除錯指南」
↓
查閱 LEARNING.md 的相關章節
↓
調整參數
↓
重新測試
```

### 常見問題速查

| 錯誤訊息 | 查看哪裡 |
|---------|---------|
| `找不到參考圖示` | `assets/REFERENCE_GUIDE.md` |
| `顏色辨識不準` | `README.md` → 問題 2 |
| `盤面位置偏移` | `README.md` → 問題 3 |
| `ImportError` | `README.md` → 常見錯誤 |

---

## 📞 學習資源

- 📖 **完整說明**：`README.md`
- 🎓 **技術學習**：`LEARNING.md`
- 📸 **圖示準備**：`assets/REFERENCE_GUIDE.md`
- 💻 **程式碼註解**：每個 `.py` 檔案都有詳細註解

---

## ✨ 最後提醒

1. **不要害怕失敗** - 第一次一定會遇到問題，這是正常的學習過程
2. **善用除錯** - DEBUG_MODE 和除錯圖片是你的好朋友
3. **分步驟進行** - 一步一步來，不要跳步驟
4. **記錄過程** - 錄影時會需要解說你的開發過程
5. **提早開始** - 不要等到最後一天才開始

---

**現在就開始吧！先執行步驟 2 安裝套件，然後準備參考圖示！** 🚀

有任何問題都可以查閱對應的文件，或者問助教。

**Good luck! 你一定可以完成的！** 💪
