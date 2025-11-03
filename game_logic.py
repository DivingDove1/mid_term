"""
Collect Em All! 自動遊戲程式 - 遊戲邏輯模組
負責分析盤面、尋找可消除的球組、選擇最佳移動策略

學習資源:
- BFS 演算法: https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
- DFS 演算法: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
- 圖論連通組: https://en.wikipedia.org/wiki/Connected_component_(graph_theory)
"""

from collections import deque
import config


# ✅ COMPLETE: 檢查座標是否在盤面內
def is_valid_position(row, col):
    """
    檢查座標是否在盤面範圍內

    Args:
        row: 行索引
        col: 列索引

    Returns:
        bool: 是否為有效座標
    """
    return 0 <= row < config.GRID_ROWS and 0 <= col < config.GRID_COLS


# 📝 STUDY: 使用 BFS 尋找連通組
def find_connected_group(board_state, start_row, start_col, visited):
    """
    使用 BFS (廣度優先搜尋) 找出從指定位置開始的連通同色球組

    Args:
        board_state: 二維陣列，表示盤面狀態
        start_row: 起始行索引
        start_col: 起始列索引
        visited: 二維布林陣列，標記已訪問的位置

    Returns:
        list: 連通組中所有格子的座標列表 [(row, col), ...]

    學習重點 - BFS 演算法:
    1. 使用佇列 (queue) 儲存待訪問的節點
    2. 從起始點開始，將其加入佇列
    3. 不斷從佇列取出節點，檢查其相鄰節點
    4. 若相鄰節點顏色相同且未訪問，加入佇列和結果
    5. 重複直到佇列為空

    BFS vs DFS:
    - BFS: 逐層擴展，適合找最短路徑
    - DFS: 深入探索，適合找所有路徑
    - 在這個問題中兩者都可以，BFS 較直觀
    """
    target_color = board_state[start_row][start_col]

    # 如果起始位置不是有效顏色，返回空列表
    if target_color == "UNKNOWN" or target_color == "EMPTY":
        return []

    # 如果已經訪問過，返回空列表
    if visited[start_row][start_col]:
        return []

    # 📝 STUDY: BFS 初始化
    queue = deque([(start_row, start_col)])  # 使用 deque 作為佇列
    group = []  # 儲存連通組
    visited[start_row][start_col] = True

    # 📝 STUDY: BFS 主迴圈
    while queue:
        row, col = queue.popleft()  # 從佇列前端取出
        group.append((row, col))

        # 📝 STUDY: 檢查 8 個相鄰方向
        for dx, dy in config.DIRECTIONS:
            new_row = row + dx
            new_col = col + dy

            # 檢查新位置是否有效
            if not is_valid_position(new_row, new_col):
                continue

            # 檢查是否已訪問
            if visited[new_row][new_col]:
                continue

            # 檢查顏色是否相同
            if board_state[new_row][new_col] != target_color:
                continue

            # 加入佇列和已訪問集合
            visited[new_row][new_col] = True
            queue.append((new_row, new_col))

    return group


# ✅ COMPLETE: 尋找所有可消除組合
def find_all_groups(board_state):
    """
    尋找盤面上所有可消除的球組（>=3 顆同色相鄰）

    Args:
        board_state: 二維陣列，表示盤面狀態

    Returns:
        list: 所有可消除組合的列表
              格式: [[(row, col), ...], ...]

    學習重點:
    - 遍歷整個盤面
    - 對每個未訪問的位置執行 BFS
    - 只保留大小 >= MIN_GROUP_SIZE 的組合
    """
    # 建立訪問標記陣列
    visited = [[False] * config.GRID_COLS for _ in range(config.GRID_ROWS)]

    all_groups = []

    # 遍歷整個盤面
    for row in range(config.GRID_ROWS):
        for col in range(config.GRID_COLS):
            # 尋找連通組
            group = find_connected_group(board_state, row, col, visited)

            # 只保留大小足夠的組合
            if len(group) >= config.MIN_GROUP_SIZE:
                all_groups.append(group)

    return all_groups


# ✅ COMPLETE: 選擇最佳移動
def select_best_move(all_groups):
    """
    從所有可消除組合中選擇最佳的一個

    策略: 選擇最大的組合（得分更高）

    Args:
        all_groups: 所有可消除組合的列表

    Returns:
        list: 最佳組合的座標列表，若沒有可消除組合則返回 None
    """
    if not all_groups:
        return None

    # 📝 STUDY: 按組合大小排序，選最大的
    best_group = max(all_groups, key=len)

    return best_group


# ✅ COMPLETE: 計算移動起點
def find_best_start_point(group):
    """
    找出最佳的拖曳起點（邊緣的球）

        Args:
            group: 球組座標列表

        Returns:
            tuple: 最佳起點座標
    """
    group_set = set(group)

    # 計算每顆球有多少相鄰同組球
    neighbor_counts = {}
    for ball in group:
        count = 0
        for dr, dc in config.DIRECTIONS:
            neighbor = (ball[0] + dr, ball[1] + dc)
            if neighbor in group_set:
                count += 1
        neighbor_counts[ball] = count

    # 選擇鄰居最少的球（邊緣球）
    best_start = min(neighbor_counts.items(), key=lambda x: x[1])[0]
    return best_start


# ✅ COMPLETE: 計算移動路徑
def calculate_drag_path(group):
    """
    從連通組中找出可拖曳的路徑
    先選最佳起點，再貪心建立路徑

    Args:
        group: 球組座標列表 [(row, col), ...]

    Returns:
        list: 可拖曳的路徑（排序後的座標列表）
    """
    if not group:
        return []

    if len(group) == 1:
        return group

    # 找最佳起點
    start = find_best_start_point(group)

    remaining = set(group)
    current = start
    path = [current]
    remaining.remove(current)

    # 貪心建立路徑
    while remaining:
        # 找相鄰的球
        neighbors = []
        for dr, dc in config.DIRECTIONS:
            neighbor = (current[0] + dr, current[1] + dc)
            if neighbor in remaining:
                neighbors.append(neighbor)

        if not neighbors:
            # 嘗試回溯（找離當前最近的未訪問球）
            if remaining:
                # 選擇曼哈頓距離最近的
                next_ball = min(
                    remaining,
                    key=lambda p: abs(p[0] - current[0]) + abs(p[1] - current[1]),
                )
                # 但這樣可能無法拖曳，建議就此中斷
                break
        else:
            # 選擇第一個鄰居（或可以選擇啟發式最佳的）
            next_ball = neighbors[0]

        path.append(next_ball)
        remaining.remove(next_ball)
        current = next_ball

    # 如果無法訪問所有球，至少返回已找到的路徑
    return path


# ✅ COMPLETE: 分析並選擇移動
def analyze_and_select_move(board_state):
    """
    分析盤面並選擇最佳移動

    Args:
        board_state: 二維陣列，表示盤面狀態

    Returns:
        tuple: (group, path) 若有可消除組合
               group: 選中的球組
               path: 拖曳路徑
               若無可消除組合則返回 (None, None)
    """
    # 尋找所有可消除組合
    all_groups = find_all_groups(board_state)

    if config.DEBUG_MODE:
        print(f"[邏輯] 找到 {len(all_groups)} 個可消除組合")

    if not all_groups:
        print("[邏輯] 沒有可消除的組合")
        return None, None

    # 選擇最佳組合
    best_group = select_best_move(all_groups)

    if config.DEBUG_MODE:
        color = None
        if best_group:
            row, col = best_group[0]
            # 假設 board_state 在外部可訪問，這裡簡化處理
        print(f"[邏輯] 最佳組合: {len(best_group)} 顆球")

    # 計算拖曳路徑
    path = calculate_drag_path(best_group)

    return best_group, path


# ==================== 輔助函數 ====================


def print_group_info(group, board_state):
    """
    印出球組資訊（除錯用）

    Args:
        group: 球組座標列表
        board_state: 盤面狀態
    """
    if not group:
        return

    # 取得顏色
    row, col = group[0]
    color = board_state[row][col]
    emoji = config.COLOR_EMOJI.get(color, "❓")

    print(f"  {emoji} {color}: {len(group)} 顆球")
    print(f"  位置: {group[:5]}{'...' if len(group) > 5 else ''}")


def test_drag_path():
    """測試拖曳路徑計算"""
    print("\n=== 測試拖曳路徑計算 ===\n")

    # 測試案例 1：簡單直線
    group1 = [(0, 0), (0, 1), (0, 2), (0, 3)]
    path1 = calculate_drag_path(group1)
    print(f"案例1 - 直線組合:")
    print(f"  輸入: {group1}")
    print(f"  輸出: {path1}")
    print(f"  檢查: {'✅' if verify_path(path1) else '❌'}\n")

    # 測試案例 2：L 型
    group2 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    path2 = calculate_drag_path(group2)
    print(f"案例2 - L型組合:")
    print(f"  輸入: {group2}")
    print(f"  輸出: {path2}")
    print(f"  檢查: {'✅' if verify_path(path2) else '❌'}\n")

    # 測試案例 3：複雜形狀
    group3 = [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3)]
    path3 = calculate_drag_path(group3)
    print(f"案例3 - 複雜組合:")
    print(f"  輸入: {group3}")
    print(f"  輸出: {path3}")
    print(f"  檢查: {'✅' if verify_path(path3) else '❌'}\n")


def verify_path(path):
    """驗證路徑是否有效（每步都相鄰）"""
    if len(path) <= 1:
        return True

    for i in range(len(path) - 1):
        current = path[i]
        next_ball = path[i + 1]

        # 檢查是否相鄰
        dr = abs(current[0] - next_ball[0])
        dc = abs(current[1] - next_ball[1])

        # 相鄰定義：8方向，距離為1
        if not ((dr <= 1 and dc <= 1) and (dr + dc > 0)):
            return False

    return True


# ==================== 測試函數 ====================


def test_game_logic():
    """
    測試遊戲邏輯模組
    使用預設的測試盤面
    """
    print("\n" + "=" * 50)
    print("測試: 遊戲邏輯模組")
    print("=" * 50 + "\n")

    # 📝 STUDY: 建立測試盤面
    test_board = [
        ["RED", "BLUE", "GREEN", "BLUE", "YELLOW", "RED"],
        ["BLUE", "BLUE", "GREEN", "GREEN", "GREEN", "YELLOW"],
        ["RED", "YELLOW", "RED", "GREEN", "BLUE", "BLUE"],
        ["GREEN", "GREEN", "RED", "RED", "YELLOW", "YELLOW"],
        ["BLUE", "RED", "YELLOW", "GREEN", "BLUE", "RED"],
        ["YELLOW", "BLUE", "GREEN", "RED", "YELLOW", "GREEN"],
    ]

    print("測試盤面:")
    for row in test_board:
        row_display = " ".join([config.COLOR_EMOJI.get(color, "❓") for color in row])
        print(row_display)
    print()

    # 尋找所有組合
    all_groups = find_all_groups(test_board)

    print(f"找到 {len(all_groups)} 個可消除組合:\n")
    for i, group in enumerate(all_groups, 1):
        print(f"組合 {i}:")
        print_group_info(group, test_board)
        print()

    # 選擇最佳移動
    best_group, path = analyze_and_select_move(test_board)

    if best_group:
        print("最佳選擇:")
        print_group_info(best_group, test_board)
        print(f"拖曳路徑: {len(path)} 個點")
    else:
        print("沒有可消除的組合")

    print("\n[測試] 測試完成！")


if __name__ == "__main__":
    # 當直接執行這個檔案時，運行測試
    test_game_logic()
