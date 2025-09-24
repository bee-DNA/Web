# 🌍 世界資料互動地圖專案

## 📖 專案概述

這是一個基於 **Dash + Plotly** 建立的互動式世界資料視覺化平台，專為科學大數據分析而設計。

## ✨ 主要功能

### 🎯 核心特色

- 🌍 **互動式世界地圖** - 即時顯示各國資料
- 📊 **多重資料指標** - 人口、GDP、平均壽命等
- 🎨 **可客製化視覺效果** - 多種色彩主題
- 📋 **智慧資料表** - 排序、篩選、搜尋功能
- 📈 **即時統計資訊** - 動態統計卡片
- 🌏 **地區篩選** - 按洲別查看資料

### 🛠️ 技術架構

- **後端框架**: Dash (基於 Flask)
- **視覺化**: Plotly
- **資料處理**: Pandas
- **地理資料**: Geopandas
- **樣式**: Dash Bootstrap Components

## 🚀 快速開始

### 1. 環境設置

```powershell
# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 確認套件安裝
pip list
```

### 2. 運行應用程式

#### 基本版地圖應用

```powershell
python world_map_app.py
```

📍 開啟瀏覽器訪問: http://127.0.0.1:8050/

#### 進階版地圖應用

```powershell
python advanced_world_map.py
```

📍 開啟瀏覽器訪問: http://127.0.0.1:8051/

### 3. 資料處理工具

```powershell
python data_processor.py
```

## 📁 專案結構

```
科學大數據專題/
├── README.md                    # 專案說明
├── world_map_app.py            # 基本地圖應用
├── advanced_world_map.py       # 進階地圖應用
├── data_processor.py           # 資料處理工具
├── world_data_sample.csv       # 範例資料集
├── venv/                       # Python 虛擬環境
└── .git/                       # Git 版本控制
```

## 📊 支援的資料格式

### 必要欄位

- `country`: 國家名稱
- `iso_alpha`: ISO 3166-1 alpha-3 國家代碼

### 可選欄位

- `population`: 人口數量
- `gdp`: GDP (十億美元)
- `life_expectancy`: 平均壽命
- `continent`: 洲別
- `capital`: 首都

## 🎯 應用場景

### 🎓 教育研究

- 人口統計學分析
- 經濟發展比較
- 地理資訊系統教學

### 💼 商業分析

- 市場規模評估
- 投資機會分析
- 國際業務規劃

### 📈 數據科學

- 地理空間分析
- 相關性研究
- 預測建模

## 🔧 客製化指南

### 1. 添加新的資料指標

在 `world_map_app.py` 中修改：

```python
# 在 create_sample_data() 函數中添加新欄位
'new_metric': [values...]

# 在 dropdown options 中添加選項
{'label': '新指標', 'value': 'new_metric'}
```

### 2. 修改色彩主題

```python
# 在色彩下拉選單中添加新主題
{'label': '新主題', 'value': 'YourColorScale'}
```

### 3. 載入自己的資料

使用 `data_processor.py`：

```python
from data_processor import WorldDataProcessor

processor = WorldDataProcessor()
df = processor.load_csv_data('your_data.csv')
df = processor.add_country_codes(df, 'country_column_name')
```

## 📋 TODO 清單

- [ ] 支援更多地圖投影方式
- [ ] 添加時間序列動畫
- [ ] 整合外部 API 資料源
- [ ] 支援地區層級資料 (州/省)
- [ ] 匯出功能 (PDF/PNG)
- [ ] 使用者自訂資料上傳
- [ ] 多語言介面

## 🤝 貢獻指南

1. Fork 這個專案
2. 建立功能分支: `git checkout -b feature/AmazingFeature`
3. 提交變更: `git commit -m 'Add some AmazingFeature'`
4. 推送分支: `git push origin feature/AmazingFeature`
5. 開啟 Pull Request

## 📝 版本歷史

- **v1.0.0** - 基本地圖功能
- **v1.1.0** - 進階統計功能
- **v1.2.0** - 資料處理工具

## 🐛 問題回報

如遇到問題，請在 GitHub Issues 中提報：
https://github.com/bee-DNA/Web/issues

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 📞 聯絡資訊

- 專案倉庫: https://github.com/bee-DNA/Web
- 電子郵件: 123321123axx@gmail.com

---

🌟 **如果這個專案對您有幫助，請給我們一個 Star！** ⭐
