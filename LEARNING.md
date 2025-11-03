# 📚 學習資源與技術解說

這份文件幫助你快速理解專案中用到的關鍵技術。

---

## 🎯 學習路徑建議

根據你的 4 天時間規劃：

### Day 1: 基礎工具（3-4 小時）
- [ ] Selenium 基礎
- [ ] PyAutoGUI 基礎
- [ ] 執行 game_launcher.py 測試

### Day 2: 視覺處理（4-5 小時）
- [ ] Pillow 圖像處理
- [ ] 顏色空間概念
- [ ] 座標系統理解
- [ ] 執行 vision_module.py 測試

### Day 3: 演算法與整合（4-5 小時）
- [ ] BFS 演算法
- [ ] 圖論連通組
- [ ] 執行完整程式
- [ ] 參數調優

### Day 4: 除錯與展示（2-3 小時）
- [ ] 測試和除錯
- [ ] 錄製影片
- [ ] 準備解說

---

## 1️⃣ Selenium 網頁自動化

### 核心概念

**Selenium** 讓你用程式控制瀏覽器，就像人類操作一樣。

### 基本用法

```python
from selenium import webdriver

# 建立瀏覽器實例
driver = webdriver.Chrome()

# 開啟網址
driver.get("https://example.com")

# 尋找元素
element = driver.find_element(By.ID, "button_id")

# 點擊元素
element.click()

# 關閉瀏覽器
driver.quit()
```

### 本專案中的使用

在 `game_launcher.py` 中：
```python
# 初始化驅動
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 開啟遊戲
driver.get(config.GAME_URL)

# 等待載入
time.sleep(3)
```

### 學習資源
- [官方文檔](https://selenium-python.readthedocs.io/)
- [快速入門](https://selenium-python.readthedocs.io/getting-started.html)

### 重點筆記
1. WebDriver 是瀏覽器的「遙控器」
2. 需要對應的 Driver（Chrome → ChromeDriver）
3. `webdriver-manager` 可以自動管理 Driver 版本

---

## 2️⃣ PyAutoGUI 螢幕控制

### 核心概念

**PyAutoGUI** 讓程式控制滑鼠、鍵盤和螢幕截圖。

### 基本用法

```python
import pyautogui

# 截圖
screenshot = pyautogui.screenshot()

# 移動滑鼠
pyautogui.moveTo(100, 200, duration=1)

# 點擊
pyautogui.click(100, 200)

# 拖曳
pyautogui.mouseDown()
pyautogui.moveTo(300, 400, duration=0.5)
pyautogui.mouseUp()

# 在螢幕上尋找圖片
location = pyautogui.locateOnScreen('image.png', confidence=0.8)
```

### 本專案中的使用

**截圖和定位**（在 `vision_module.py`）:
```python
# 截圖
screenshot = pyautogui.screenshot()

# 尋找參考圖示
location = pyautogui.locateOnScreen(
    config.REFERENCE_ICON_PATH,
    confidence=config.MATCH_CONFIDENCE
)
```

**滑鼠控制**（在 `controller.py`）:
```python
# 拖曳球
pyautogui.moveTo(start_x, start_y, duration=0.2)
pyautogui.mouseDown()
pyautogui.moveTo(end_x, end_y, duration=0.5)
pyautogui.mouseUp()
```

### 學習資源
- [官方文檔](https://pyautogui.readthedocs.io/)
- [滑鼠控制](https://pyautogui.readthedocs.io/en/latest/mouse.html)
- [鍵盤控制](https://pyautogui.readthedocs.io/en/latest/keyboard.html)

### 重點筆記
1. 座標系統：(0,0) 在螢幕左上角
2. `duration` 參數讓動作看起來更自然
3. `confidence` 控制圖像匹配的嚴格程度（0.0-1.0）

---

## 3️⃣ Pillow 圖像處理

### 核心概念

**Pillow (PIL)** 用於處理圖片，包括讀取、修改、分析圖片。

### 基本用法

```python
from PIL import Image

# 開啟圖片
img = Image.open("image.png")

# 裁切圖片
cropped = img.crop((x1, y1, x2, y2))  # (left, top, right, bottom)

# 取得像素值
pixel = img.getpixel((x, y))  # 返回 (R, G, B) 或 (R, G, B, A)

# 儲存圖片
img.save("output.png")
```

### 本專案中的使用

**顏色分析**（在 `vision_module.py`）:
```python
# 裁切取樣區域
sample_region = board_image.crop((left, top, right, bottom))

# 轉換為 numpy array 計算平均顏色
sample_array = np.array(sample_region)
avg_color = sample_array.mean(axis=(0, 1))  # 計算平均 RGB
```

### 學習資源
- [官方文檔](https://pillow.readthedocs.io/)
- [圖像操作教學](https://pillow.readthedocs.io/en/stable/handbook/tutorial.html)

### 重點筆記
1. PIL 使用 (x, y) 座標，x 向右，y 向下
2. `crop()` 使用 (left, top, right, bottom)
3. 像素值是 tuple: (R, G, B) 或 (R, G, B, A)

---

## 4️⃣ 顏色空間與 RGB

### RGB 顏色模型

每個像素由三個數值組成：
- **R (Red)**: 紅色，0-255
- **G (Green)**: 綠色，0-255
- **B (Blue)**: 藍色，0-255

### 顏色比較

如何判斷兩個顏色是否相似？使用**歐幾里得距離**：

```python
import numpy as np

color1 = (255, 100, 100)  # 紅色
color2 = (250, 105, 95)   # 接近紅色

# 計算距離
distance = np.sqrt(
    (color1[0] - color2[0])**2 +
    (color1[1] - color2[1])**2 +
    (color1[2] - color2[2])**2
)

# 如果距離小於閾值，認為是同一顏色
if distance < 50:
    print("顏色相似")
```

### 本專案中的使用

在 `vision_module.py` 的 `detect_cell_color()`:
```python
# 計算每個預定義顏色的距離
for color_name, (r, g, b) in config.BALL_COLORS.items():
    distance = np.sqrt(
        (avg_r - r)**2 + (avg_g - g)**2 + (avg_b - b)**2
    )
    
    # 找最小距離
    if distance < min_distance and distance < COLOR_TOLERANCE:
        best_match = color_name
```

### 學習資源
- [RGB 顏色模型](https://en.wikipedia.org/wiki/RGB_color_model)
- [線上取色工具](https://imagecolorpicker.com/)

### 實用技巧

**如何找出遊戲中球的 RGB 值？**

1. 截取遊戲畫面
2. 用小畫家或線上工具開啟
3. 使用「取色器」工具點擊球
4. 記下 RGB 值
5. 更新到 `config.py` 的 `BALL_COLORS`

---

## 5️⃣ 座標系統轉換

### 三種座標系統

本專案使用三種座標：

```
1. 格子索引 (Grid Index)
   - 範圍: (0,0) 到 (5,5)
   - 用途: 表示盤面位置

2. 盤面相對座標 (Board Relative)
   - 範圍: (0,0) 到 (360,360)  # 假設 6x6 格，每格 60px
   - 用途: 盤面內的像素位置

3. 螢幕絕對座標 (Screen Absolute)
   - 範圍: (0,0) 到 (1920,1080)  # 依螢幕解析度
   - 用途: PyAutoGUI 操作滑鼠
```

### 轉換公式

**格子索引 → 盤面相對座標**:
```python
relative_x = col * CELL_SIZE + CELL_SIZE // 2  # 格子中心
relative_y = row * CELL_SIZE + CELL_SIZE // 2
```

**盤面相對座標 → 螢幕絕對座標**:
```python
screen_x = board_x + relative_x
screen_y = board_y + relative_y
```

**完整轉換**（在 `controller.py`）:
```python
def grid_to_screen(row, col, board_x, board_y):
    # 步驟 1: 格子 → 盤面相對
    relative_x = col * config.CELL_SIZE + config.CELL_SIZE // 2
    relative_y = row * config.CELL_SIZE + config.CELL_SIZE // 2
    
    # 步驟 2: 盤面相對 → 螢幕絕對
    screen_x = board_x + relative_x
    screen_y = board_y + relative_y
    
    return screen_x, screen_y
```

### 視覺化範例

```
螢幕 (1920x1080)
┌────────────────────────────────┐
│                                │
│   盤面 (board_x=100, board_y=200)
│   ┌─────────────┐              │
│   │ (0,0) (0,1) │              │
│   │ (1,0) (1,1) │  ← 格子索引  │
│   └─────────────┘              │
│                                │
└────────────────────────────────┘

格子 (1,1) 的座標:
1. 格子索引: (1, 1)
2. 盤面相對: (90, 90)  # 假設 CELL_SIZE=60, 中心在 (1*60+30, 1*60+30)
3. 螢幕絕對: (190, 290) # 100+90, 200+90
```

---

## 6️⃣ BFS 演算法（重要！）

### 什麼是 BFS？

**BFS (Breadth-First Search)** = **廣度優先搜尋**

想像你在迷宮中，BFS 就是：
1. 先檢查你旁邊的所有格子
2. 再檢查旁邊格子的旁邊格子
3. 一層一層向外擴展

### 為什麼用 BFS？

在這個遊戲中，我們要找「連通的同色球」，BFS 很適合：
- 從一顆球開始
- 找出所有相鄰的同色球
- 這些球就是一個「連通組」

### BFS 實作（在 `game_logic.py`）

```python
from collections import deque

def find_connected_group(board_state, start_row, start_col, visited):
    target_color = board_state[start_row][start_col]
    
    # 步驟 1: 建立佇列，放入起點
    queue = deque([(start_row, start_col)])
    group = []
    visited[start_row][start_col] = True
    
    # 步驟 2: 當佇列不為空時，持續處理
    while queue:
        row, col = queue.popleft()  # 取出佇列最前面的點
        group.append((row, col))
        
        # 步驟 3: 檢查 8 個相鄰方向
        for dx, dy in DIRECTIONS:  # 8 個方向
            new_row = row + dx
            new_col = col + dy
            
            # 檢查是否有效、未訪問、顏色相同
            if (is_valid(new_row, new_col) and
                not visited[new_row][new_col] and
                board_state[new_row][new_col] == target_color):
                
                # 加入佇列
                visited[new_row][new_col] = True
                queue.append((new_row, new_col))
    
    return group
```

### 視覺化範例

假設盤面：
```
🔴 🔵 🔴
🔴 🔵 🔴
🔴 🔴 🔴
```

從 (0,0) 的紅球開始 BFS：

```
步驟 1: 佇列 = [(0,0)]
       訪問 (0,0) ✓
       檢查相鄰: (1,0) 是紅球 → 加入佇列
       佇列 = [(1,0)]

步驟 2: 佇列 = [(1,0)]
       訪問 (1,0) ✓
       檢查相鄰: (0,0) 已訪問, (2,0) 是紅球 → 加入
       佇列 = [(2,0)]

步驟 3: 佇列 = [(2,0)]
       訪問 (2,0) ✓
       檢查相鄰: (1,0) 已訪問, (2,1) 是紅球 → 加入
       佇列 = [(2,1)]

... 繼續直到佇列為空

結果: 找到連通組 [(0,0), (1,0), (2,0), (2,1), (2,2), ...]
```

### 學習資源
- [BFS 視覺化](https://visualgo.net/en/dfsbfs)
- [GeeksforGeeks BFS 教學](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)

### 重點筆記
1. BFS 使用**佇列** (queue)，FIFO（先進先出）
2. 需要 `visited` 陣列避免重複訪問
3. 適合找最短路徑、連通組

---

## 7️⃣ 除錯技巧

### print() 除錯

在關鍵位置加入 print：
```python
print(f"[除錯] 目前處理格子: ({row}, {col})")
print(f"[除錯] 辨識顏色: {color}")
print(f"[除錯] 找到組合大小: {len(group)}")
```

### 視覺化除錯

程式會產生除錯圖片：
```python
# 在圖片上標記資訊
from PIL import ImageDraw

draw = ImageDraw.Draw(image)
draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
draw.text((x, y), "標記", fill="white")
image.save("debug_output.png")
```

### 分步驟測試

不要一次執行全部！分別測試每個模組：
```bash
python game_launcher.py   # 測試啟動
python vision_module.py   # 測試視覺
python game_logic.py      # 測試邏輯
python controller.py      # 測試控制
python main.py            # 完整執行
```

---

## 8️⃣ 常見程式模式

### try-except 錯誤處理

```python
try:
    # 可能出錯的程式碼
    result = risky_operation()
except Exception as e:
    # 處理錯誤
    print(f"發生錯誤: {e}")
    # 可以選擇繼續或結束
```

### 迴圈遍歷二維陣列

```python
# 遍歷所有格子
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        value = board[row][col]
        # 處理 value
```

### 列表推導式

```python
# 建立二維陣列
visited = [[False] * COLS for _ in range(ROWS)]

# 等同於：
visited = []
for _ in range(ROWS):
    row = [False] * COLS
    visited.append(row)
```

---

## 📖 推薦閱讀順序

1. **先快速瀏覽**所有學習資源，有個概念
2. **執行測試程式**，看實際效果
3. **遇到不懂的地方**，回來查閱對應章節
4. **參考程式碼註解**，理解實作細節
5. **嘗試修改參數**，觀察變化

---

## 💡 學習小技巧

1. **不要一次理解所有東西**
   - 先讓程式跑起來
   - 再慢慢理解細節

2. **善用官方文檔**
   - 所有套件都有詳細文檔
   - 用 Ctrl+F 搜尋功能

3. **實驗精神**
   - 改改看參數會怎樣
   - 加 print 看看執行過程

4. **記錄問題**
   - 記下你不懂的地方
   - 之後統一查詢或詢問

---

## ❓ 快速查詢

| 想做什麼 | 看哪個章節 | 在哪個檔案 |
|---------|----------|-----------|
| 控制瀏覽器 | 1. Selenium | game_launcher.py |
| 截圖、定位圖片 | 2. PyAutoGUI | vision_module.py |
| 處理圖片、讀取顏色 | 3. Pillow | vision_module.py |
| 比較顏色 | 4. 顏色空間 | vision_module.py |
| 座標轉換 | 5. 座標系統 | controller.py |
| 找連通球組 | 6. BFS 演算法 | game_logic.py |
| 除錯技巧 | 7. 除錯技巧 | 所有檔案 |

---

**記住：程式設計是實作出來的，不是讀出來的。動手做才是王道！** 💪
