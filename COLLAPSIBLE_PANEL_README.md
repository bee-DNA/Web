# 可收納統計面板系統 - 技術文件

## 🎯 系統概述

這個項目提供了兩個版本的可收納統計面板地圖系統：

1. **HTML 版本** (`collapsible_stats_map.html`) - 純前端實現，使用 Mapbox GL JS
2. **Dash 版本** (`collapsible_stats_dash.py`) - Python Dash 框架實現，使用 Plotly

## 🚀 快速開始

### HTML 版本

```bash
# 直接在瀏覽器中開啟
start collapsible_stats_map.html
```

### Dash 版本

```bash
# 安裝依賴
pip install dash plotly pandas numpy

# 運行應用
python collapsible_stats_dash.py

# 開啟瀏覽器訪問
# http://127.0.0.1:8050/
```

## ✨ 核心功能

### 1. 可收納統計面板

- **智能收納**: 點擊展開後自動開始倒計時收納
- **可配置時間**: 3 秒、5 秒、8 秒、10 秒或關閉自動收納
- **流暢動畫**: CSS3 動畫效果，包括滑動和淡入淡出
- **懸停暫停**: 滑鼠懸停時暫停自動收納計時

### 2. 實時數據更新

- **展開觸發**: 每次展開面板時自動刷新所有統計數據
- **動畫提示**: 數據更新時具備脈衝動畫效果
- **實時監控**: 顯示地圖縮放、座標、數據點等即時資訊

### 3. 地圖互動功能

- **多種樣式**: 開放街圖、衛星圖、地形圖等 5 種地圖樣式
- **數據重生成**: 一鍵重新產生隨機地理數據
- **視角重設**: 快速回到台灣地區預設視角
- **互動統計**: 地圖操作實時反映在統計面板中

## 🎨 視覺設計

### CSS 動畫效果

```css
/* 滑動展開動畫 */
@keyframes slideDown {
  from {
    max-height: 0;
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    max-height: 500px;
    opacity: 1;
    transform: translateY(0);
  }
}

/* 脈衝更新動畫 */
@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(40, 167, 69, 0);
  }
}
```

### 顏色主題

- **主色調**: 翠綠色 (#28a745) 漸層設計
- **背景**: 淺灰漸層 (#f8f9fa → #e9ecef)
- **強調色**: 藍色按鈕 (#3498db)、紅色重設 (#e74c3c)
- **文字**: 深灰色 (#495057) 高對比度設計

## 📊 統計數據項目

| 統計項目        | 說明                   | 更新方式       |
| --------------- | ---------------------- | -------------- |
| 🔍 當前縮放級別 | 地圖的縮放倍數         | 地圖操作觸發   |
| 📍 中心座標     | 地圖中心點經緯度       | 地圖移動觸發   |
| 📊 資料點數量   | 當前顯示的數據點總數   | 數據重生成觸發 |
| 🎨 地圖樣式     | 當前使用的地圖樣式名稱 | 樣式切換觸發   |
| ⏰ 最後更新     | 統計數據最後更新時間   | 實時更新       |
| 🔄 更新次數     | 累計統計更新次數       | 每次更新累加   |

## ⚙️ 配置選項

### 自動收納設定

```javascript
// HTML版本配置
const AUTO_COLLAPSE_OPTIONS = {
  DISABLED: 0, // 關閉自動收納
  FAST: 3000, // 3秒後收納
  NORMAL: 5000, // 5秒後收納（預設）
  SLOW: 8000, // 8秒後收納
  VERY_SLOW: 10000, // 10秒後收納
};
```

### 地圖樣式選項

```python
# Dash版本樣式映射
mapbox_styles = {
    'open-street-map': '🗺️ 開放街圖',
    'satellite': '🛰️ 衛星圖',
    'stamen-terrain': '🌍 地形圖',
    'carto-positron': '🌫️ 淺色地圖',
    'carto-darkmatter': '🌙 深色地圖'
}
```

## 🛠️ 技術實現

### HTML 版本技術棧

- **地圖引擎**: Mapbox GL JS v3.6.0
- **UI 框架**: 純 HTML5/CSS3/JavaScript
- **動畫**: CSS3 Transitions & Animations
- **響應式**: Flexbox 佈局設計

### Dash 版本技術棧

- **後端框架**: Python Dash v2.14+
- **地圖組件**: Plotly Scattermapbox
- **數據處理**: Pandas + NumPy
- **狀態管理**: Dash Store 組件
- **回調系統**: Dash Callback 裝飾器

## 🔧 開發者指南

### 添加新的統計項目

1. **HTML 版本**:

```html
<!-- 在統計面板中添加新項目 -->
<div class="stat-item">
  <div class="stat-label">📈 新統計項目</div>
  <div class="stat-value" id="new-stat">載入中...</div>
</div>
```

2. **Dash 版本**:

```python
# 在佈局中添加新的統計項目
html.Div([
    html.Div("📈 新統計項目", className="stat-label-dash"),
    html.Div("載入中...", id="new-stat", className="stat-value-dash")
], className="stat-item-dash")
```

### 自定義動畫效果

```css
/* 添加新的動畫關鍵幀 */
@keyframes customAnimation {
  0% {
    /* 起始狀態 */
  }
  50% {
    /* 中間狀態 */
  }
  100% {
    /* 結束狀態 */
  }
}

/* 應用到元素 */
.custom-element {
  animation: customAnimation 0.5s ease-in-out;
}
```

## 🎯 使用場景

### 1. 數據監控儀表板

適合需要實時監控地理數據變化的場景，統計面板提供關鍵指標概覽。

### 2. 教育展示系統

可收納設計避免界面雜亂，適合教學演示時的清爽展示需求。

### 3. 數據分析工具

支持多種地圖樣式和數據重生成，適合進行地理數據分析和可視化。

### 4. 研究項目展示

專業的動畫效果和統計展示，適合學術研究成果的展示。

## 📈 性能優化

### 動畫性能

- 使用 CSS3 硬體加速動畫
- 避免在動畫中使用 layout 屬性
- 合理控制動畫執行頻率

### 數據更新優化

- 僅在面板展開時更新統計
- 防抖處理頻繁的地圖操作
- 智能緩存地圖狀態數據

## 🔍 故障排除

### 常見問題

1. **統計面板無法展開**

   - 檢查 CSS 動畫是否載入完成
   - 確認 JavaScript 事件綁定正確

2. **自動收納功能失效**

   - 驗證定時器設定是否正確
   - 檢查懸停事件是否干擾計時

3. **地圖無法載入**

   - 確認網路連接正常
   - 檢查 Mapbox API 配置

4. **數據更新異常**
   - 檢查回調函數邏輯
   - 驗證狀態管理機制

## 🌟 未來增強計劃

- [ ] 添加更多地圖樣式選項
- [ ] 支持自定義統計項目
- [ ] 增加數據匯出功能
- [ ] 實現多語言界面支持
- [ ] 添加鍵盤快捷鍵操作
- [ ] 支持觸控手勢操作
- [ ] 集成更多地圖服務商
- [ ] 添加統計圖表視圖

## 📞 技術支持

如有任何技術問題或功能建議，歡迎聯繫開發團隊或提交 Issue。

---

_最後更新: 2024 年 12 月_
