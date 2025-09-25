# 🗺️ Mapbox GL JS 互動式地圖系統

## 📋 項目概述

這是一個基於 **Mapbox GL JS** 前端地圖框架的專業地理視覺化系統，使用 **OpenStreetMap** 作為底層地圖資料，並支援自定義圖層疊加，包括標記、熱圖、聚類分析等功能。

## 🏗️ 技術架構

### 前端技術棧
- **地圖框架**: Mapbox GL JS v3.6.0
- **底層地圖**: OpenStreetMap (免費) + Mapbox 樣式 (需 Token)
- **前端語言**: HTML5, CSS3, JavaScript (ES6+)
- **響應式設計**: 支援桌面和行動裝置

### 後端技術棧
- **API 框架**: Flask (Python)
- **資料處理**: Pandas, NumPy
- **跨域支援**: Flask-CORS
- **資料格式**: JSON, GeoJSON, CSV

### 資料來源
- **地圖瓦片**: OpenStreetMap, CartoDB, Mapbox
- **地理資料**: 自定義 CSV/JSON 檔案
- **API 端點**: RESTful API 提供即時資料

## 📁 檔案結構

```
mapbox-interactive-map/
├── mapbox_interactive_map.html    # 前端地圖介面
├── mapbox_api_server.py          # 後端 API 服務
├── mapbox_config.py              # 配置檔案
├── requirements.txt              # Python 相依套件
└── README.md                     # 專案說明文件
```

## 🚀 快速開始

### 1. 環境準備

```bash
# 安裝 Python 相依套件
pip install flask flask-cors pandas numpy

# 或使用 requirements.txt
pip install -r requirements.txt
```

### 2. 啟動後端 API

```bash
python mapbox_api_server.py
```

服務將啟動在 `http://localhost:5000`

### 3. 開啟地圖介面

在瀏覽器中訪問：
- **地圖介面**: http://localhost:5000/map
- **API 文件**: http://localhost:5000

## 🗺️ 地圖樣式支援

### 免費樣式 (無需 Token)
- **OpenStreetMap 明亮版**: 標準 OSM 地圖樣式
- **OpenStreetMap 深色版**: 深色主題的 OSM 樣式
- **CartoDB Positron**: 簡約明亮的地圖樣式
- **CartoDB Dark Matter**: 深色簡約地圖樣式

### Mapbox 樣式 (需要 Token)
- **Mapbox Streets**: 官方街道樣式
- **Mapbox 衛星圖**: 高解析度衛星影像
- **Mapbox 衛星街道圖**: 衛星影像 + 街道標籤

### 取得 Mapbox Token
1. 註冊 [Mapbox 帳號](https://www.mapbox.com/)
2. 在控制台建立新的 Access Token
3. 在地圖介面中輸入 Token 或在配置檔案中設定

## 📍 圖層功能

### 🏙️ 城市標記圖層
- **功能**: 顯示地理位置點
- **視覺化**: 可變大小和顏色的圓形標記
- **互動**: 點擊顯示詳細資訊彈窗
- **自定義**: 支援數值對應顏色和大小

### 🔥 熱力圖圖層
- **功能**: 顯示資料密度分布
- **視覺化**: 漸層色彩表示數值強度
- **適用場景**: 大量資料點的密度視覺化
- **效能**: 適合處理 1000+ 資料點

### 📊 聚類分析圖層
- **功能**: 自動聚合相近的資料點
- **視覺化**: 聚類圓圈顯示聚合數量
- **互動**: 點擊聚類可展開查看詳細點
- **效能**: 改善大量資料的載入效能

### 🌐 國家邊界圖層
- **功能**: 顯示國家/地區邊界線
- **資料來源**: Mapbox Vector Tiles
- **用途**: 提供地理參考框架

## 📊 API 端點

### 資料查詢 API

```http
GET /api/cities
# 取得所有城市資料

GET /api/cities?country=台灣
# 篩選特定國家

GET /api/cities?min_value=80&max_value=90
# 篩選數值範圍

GET /api/cities?category=A
# 篩選特定分類
```

### GeoJSON API

```http
GET /api/cities/geojson
# 取得 GeoJSON 格式資料

GET /api/cities/geojson?country=日本
# 篩選特定國家的 GeoJSON 資料
```

### 統計資料 API

```http
GET /api/statistics
# 取得資料統計摘要

GET /api/cities/台北
# 取得特定城市詳細資料
```

### 資料上傳 API

```http
POST /api/upload
Content-Type: multipart/form-data

# 上傳 CSV 檔案新增地理資料
```

## 🎨 自定義配置

### 修改地圖樣式

在 `mapbox_config.py` 中新增自定義樣式：

```python
MAPBOX_CONFIG['STYLES']['custom_style'] = {
    'name': '自定義樣式',
    'description': '您的自定義地圖樣式',
    'requires_token': False,
    'style': {
        # Mapbox Style Specification
    }
}
```

### 調整圖層配置

修改 `LAYER_CONFIG` 中的圖層設定：

```python
LAYER_CONFIG['cities']['paint']['circle-color'] = [
    'interpolate',
    ['linear'],
    ['get', 'value'],
    0, '#your_color_1',
    50, '#your_color_2',
    100, '#your_color_3'
]
```

### 資料格式要求

上傳的 CSV 檔案必須包含以下欄位：
- `city`: 城市名稱 (必需)
- `latitude`: 緯度 (必需)
- `longitude`: 經度 (必需)
- `value`: 數值資料 (選填)
- `category`: 分類資料 (選填)
- `country`: 國家名稱 (選填)

範例 CSV 格式：
```csv
city,latitude,longitude,value,category,country
台北,25.0330,121.5654,85,A,台灣
東京,35.6895,139.6917,92,B,日本
```

## 🔧 進階功能

### 效能最佳化
- **自動聚類**: 超過 500 個點時自動啟用聚類
- **標籤管理**: 超過 100 個點時隱藏標籤
- **瓦片快取**: 256MB 地圖瓦片快取
- **懒載入**: 按需載入圖層資料

### 互動功能
- **縮放控制**: 滑鼠滾輪和觸控縮放
- **平移拖拽**: 拖拽移動地圖視角
- **全螢幕模式**: 支援全螢幕地圖檢視
- **資訊彈窗**: 點擊標記顯示詳細資訊

### 響應式設計
- **桌面版**: 側邊欄 + 主地圖佈局
- **平板**: 自適應佈局調整
- **手機**: 垂直堆疊佈局

## 🛠️ 故障排除

### 常見問題

**Q: 地圖無法載入**
- 檢查網路連線
- 確認 API 服務是否正常運行
- 查看瀏覽器控制台錯誤訊息

**Q: Mapbox 樣式無法使用**
- 確認已輸入有效的 Mapbox Token
- 檢查 Token 權限設定
- 驗證 Token 是否過期

**Q: 資料無法顯示**
- 檢查資料格式是否正確
- 確認緯經度數值範圍 (-90~90, -180~180)
- 查看 API 回應狀態

### 效能問題

**大量資料載入緩慢**
- 啟用聚類功能
- 使用熱力圖代替點標記
- 實施資料分頁載入

**地圖渲染卡頓**
- 降低資料點數量
- 簡化圖層樣式
- 關閉不必要的圖層

## 📈 未來擴展

### 計劃功能
- [ ] 即時資料更新 (WebSocket)
- [ ] 時間序列動畫
- [ ] 3D 地形視覺化
- [ ] 自定義標記圖示
- [ ] 資料匯出功能
- [ ] 使用者帳號系統
- [ ] 地圖分享功能

### 技術升級
- [ ] TypeScript 支援
- [ ] Vue.js/React 整合
- [ ] PostgreSQL + PostGIS 資料庫
- [ ] Docker 容器化部署
- [ ] CI/CD 自動化流程

## 📝 授權資訊

- **Mapbox GL JS**: 遵循 Mapbox ToS
- **OpenStreetMap**: ODbL 1.0 授權
- **專案程式碼**: MIT 授權

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📧 聯絡資訊

如有問題或建議，歡迎透過以下方式聯絡：
- 建立 GitHub Issue
- 發送 Email

---

**🌍 讓地理資料視覺化變得簡單而強大！**