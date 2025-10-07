# SRA 下載與檢查工具使用指南

## 📚 目錄

- [工具概述](#工具概述)
- [1. 批量下載工具](#1-批量下載工具)
- [2. 完整性檢查工具](#2-完整性檢查工具)
- [3. 進度管理](#3-進度管理)
- [4. 常見問題](#4-常見問題)
- [5. 文件結構](#5-文件結構)

---

## 工具概述

本專案包含兩個主要 Python 工具：

1. **`batch_fastq_downloader.py`** - 批量下載 SRA 檔案並解壓為 FASTQ
2. **`check_sra_integrity.py`** - 檢查已下載 SRA 檔案的完整性

---

## 1. 批量下載工具

### 📁 檔案路徑
```
D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\batch_fastq_downloader.py
```

### 🎯 功能特點

- ✅ **並行下載**: 支援同時下載 10 個樣本 (`MAX_WORKERS=10`)
- ✅ **自動重試**: 失敗的任務會自動記錄，可重新執行
- ✅ **進度追蹤**: 實時顯示下載進度和預估剩餘時間
- ✅ **斷點續傳**: 支援中斷後繼續下載
- ✅ **四步驟流程**:
  1. `prefetch` - 下載 SRA 檔案到 D 槽
  2. `fasterq-dump` - 解壓為 FASTQ 檔案到 E 槽
  3. 備份 SRA 到 E:\sra_files
  4. 清理 D 槽臨時檔案

### 📋 使用方法

#### 基本用法

```powershell
# 進入工作目錄
cd "D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector"

# 執行下載程式
python batch_fastq_downloader.py
```

#### 進階設定

**修改並行數量**:
```python
# 編輯 batch_fastq_downloader.py 第 253 行
MAX_WORKERS = 10  # 可改為 5、15、20 等
```

**修改超時設定**:
```python
# prefetch 超時 (第 97 行)
timeout=7200  # 120分鐘，可改為 3600 (60分鐘) 或 10800 (180分鐘)

# fasterq-dump 超時 (第 123 行)
timeout=9000  # 150分鐘，可改為 7200 (120分鐘) 或 12000 (200分鐘)
```

### 📊 輸出資訊

執行時會顯示：

```
============================================================
🚀 FASTQ 批量下載器
============================================================
  總任務: 606
  已完成: 141 (23.3%)
  失敗: 24
  剩餘: 465
  並行數: 10
  輸出: E:\fastq_data
============================================================

[109/606] 進度: 18.0% | ⏱️  預估剩餘: 45小時23分鐘15秒

============================================================
📥 處理: SRR10810029
============================================================
  步驟 1/4: prefetch SRR10810029...
  執行中... 124秒
  ✅ 完成 (124.3秒)
  步驟 2/4: fasterq-dump SRR10810029...
  執行中... 3456秒
  ✅ 完成 (3456.7秒)
  步驟 3/4: 備份 SRA 到 E:\sra_files...
  ✅ 完成 (12.1秒)
  步驟 4/4: 清理 OneDrive 臨時檔案...
  ✅ 完成 (1.2秒)
  ⏱️  總時間: 3594.3 秒
```

### 📂 目錄結構

```
D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\
├── batch_fastq_downloader.py          # 主程式
├── runs.txt                            # 樣本列表 (606 個 SRR ID)
├── download_progress.json              # 進度追蹤檔案
├── sratoolkit.3.2.1-win64\             # SRA Toolkit 工具
│   └── bin\
│       ├── prefetch.exe
│       ├── fasterq-dump.exe
│       └── vdb-validate.exe
├── SRR*******\                         # 臨時 SRA 下載目錄
│   └── SRR*******.sra
└── ...

E:\fastq_data\                          # FASTQ 輸出目錄
├── SRR10810025_1.fastq
├── SRR10810025_2.fastq
├── SRR10810029_1.fastq
├── SRR10810029_2.fastq
└── ...

E:\sra_files\                           # SRA 備份目錄
├── SRR10810025.sra
├── SRR10810029.sra
└── ...
```

### 🔧 暫停與繼續

**暫停下載**:
```powershell
# 方法1: 按 Ctrl+C (推薦)
# 程式會安全停止並顯示:
#   ⚠️  收到中斷信號,正在安全停止...
#   ⏸️  等待當前任務完成後退出...
#   💾 進度已保存到 download_progress.json
#   🔄 下次執行將從斷點繼續

# 方法2: 關閉終端機視窗
# 進度會自動保存
```

**暫停行為說明**:
- ⏱️ 正在執行的 10 個並行任務會完成當前步驟
- 💾 已完成的任務自動保存到 `download_progress.json`
- 🚫 新的任務不會啟動
- ⏸️ 通常在 1-3 分鐘內完全停止 (取決於當前任務進度)

**繼續下載**:
```powershell
cd "D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector"
python batch_fastq_downloader.py
# 程式會自動跳過已完成的樣本,從剩餘樣本繼續下載
```

### ⚙️ 關鍵參數說明

| 參數 | 位置 | 預設值 | 說明 |
|------|------|--------|------|
| `MAX_WORKERS` | 第 253 行 | 10 | 並行下載數量 |
| `prefetch timeout` | 第 97 行 | 7200秒 (120分鐘) | prefetch 超時時間 |
| `fasterq-dump timeout` | 第 123 行 | 9000秒 (150分鐘) | 解壓超時時間 |
| `output_dir` | 第 260 行 | `E:/fastq_data` | FASTQ 輸出目錄 |
| `sra_backup_dir` | 第 142 行 | `E:/sra_files` | SRA 備份目錄 |

---

## 2. 完整性檢查工具

### 📁 檔案路徑
```
D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\check_sra_integrity.py
```

### 🎯 功能特點

- ✅ **快速檢查模式**: 只檢查檔案大小 (秒級完成)
- ✅ **完整驗證模式**: 使用 `vdb-validate` 檢查內部結構 (分鐘級完成)
- ✅ **詳細報告**: 生成 JSON 格式的檢查報告
- ✅ **問題偵測**: 自動識別損壞或可疑的檔案

### 📋 使用方法

#### 快速檢查 (推薦先用)

```powershell
cd "D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector"
python check_sra_integrity.py
```

**預設執行完整檢查**，如需快速檢查，修改最後一行：

```python
# 編輯 check_sra_integrity.py 最後一行
if __name__ == "__main__":
    quick_check_all_sra_files()  # 快速檢查
    # check_all_sra_files()      # 完整檢查
```

#### 完整驗證

```python
# 編輯 check_sra_integrity.py 最後一行
if __name__ == "__main__":
    check_all_sra_files()  # 完整檢查
```

### 📊 輸出範例

#### 快速檢查輸出

```
================================================================================
⚡ SRA 檔案快速檢查 (檔案大小檢查)
================================================================================
📁 掃描目錄: D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector

📊 找到 14 個 SRA 檔案

[1/14] SRR10810025: 3698.8 MB - ✅ 正常
[2/14] SRR10810029: 4717.7 MB - ✅ 正常
[3/14] SRR12180939: 35.1 MB - ✅ 正常
...

================================================================================
📊 快速檢查摘要
================================================================================
  總檔案數: 14
  ✅ 正常: 14 (100.0%)
  ⚠️  可疑: 0 (0.0%)
  💾 總大小: 43223.5 MB (42.21 GB)
================================================================================
```

#### 完整驗證輸出

```
================================================================================
🔍 SRA 檔案完整性檢查
================================================================================
📁 掃描目錄: D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector
🛠️  SRA Toolkit: D:\OneDrive\...\sratoolkit.3.2.1-win64\bin
================================================================================

📊 找到 14 個 SRA 檔案

[1/14] 檢查: SRR10810025
  📁 檔案: SRR10810025.sra
  💾 大小: 3698.8 MB
  🔍 快速檢查... 資訊可用
  ✓ 完整性驗證... ✅ 完整

[3/14] 檢查: SRR12180939
  📁 檔案: SRR12180939.sra
  💾 大小: 35.1 MB
  🔍 快速檢查... 無法獲取資訊
  ✓ 完整性驗證... ❌ zombie file detected

================================================================================
📊 檢查完成摘要
================================================================================
  總檔案數: 14
  ✅ 完整: 11 (78.6%)
  ❌ 損壞: 3 (21.4%)
  ⚠️  未知: 0 (0.0%)
  💾 總大小: 43223.5 MB (42.21 GB)
  📄 報告: D:\...\sra_integrity_report.json
================================================================================

❌ 損壞的檔案列表:
  - SRR12180939: zombie file detected
  - SRR12181006: zombie file detected
  - SRR12181036: zombie file detected
```

### 📄 檢查報告

完整檢查會生成報告檔案：
```
D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\sra_integrity_report.json
```

**報告格式**:
```json
{
  "valid": [
    {
      "sample_id": "SRR10810025",
      "file": "D:\\OneDrive\\...\\SRR10810025\\SRR10810025.sra",
      "size_mb": 3698.8,
      "info": "資訊可用"
    }
  ],
  "invalid": [
    {
      "sample_id": "SRR12180939",
      "file": "D:\\OneDrive\\...\\SRR12180939\\SRR12180939.sra",
      "size_mb": 35.1,
      "error": "zombie file detected..."
    }
  ],
  "unknown": [],
  "total_size_mb": 43223.5,
  "check_time": "2025-10-07T10:54:38.123456"
}
```

### 🔍 檢查模式比較

| 模式 | 速度 | 準確度 | 適用場景 |
|------|------|--------|----------|
| **快速檢查** | ⚡ 秒級 | 基本 | 快速掃描，找出明顯異常的檔案 |
| **完整驗證** | 🐌 分鐘級 | 高 | 確認檔案內部結構完整性 |

---

## 3. 進度管理

### 📄 進度追蹤檔案

**檔案路徑**:
```
D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\download_progress.json
```

**檔案結構**:
```json
{
  "completed": [
    "SRR16972395",
    "SRR16972409",
    "SRR10810025"
  ],
  "failed": [
    {
      "run_id": "SRR7986801",
      "step": "prefetch",
      "error": "Timeout after 7200s",
      "time": "2025-10-06T16:36:33.511156"
    }
  ],
  "total_size_mb": 1507474.5919837952,
  "timestamp": "2025-10-02 01:28:38",
  "last_update": "2025-10-06T17:03:07.082627"
}
```

### 🔄 手動編輯進度

**重新下載特定樣本**:

1. 打開 `download_progress.json`
2. 從 `completed` 陣列中移除樣本 ID
3. 刪除對應的 SRA 目錄
4. 重新執行下載程式

```powershell
# 範例：重新下載 SRR12180939
# 1. 刪除目錄
Remove-Item -Recurse -Force "D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\SRR12180939"

# 2. 編輯 download_progress.json，移除 "SRR12180939" 從 completed 陣列

# 3. 重新執行
python batch_fastq_downloader.py
```

### 📊 查看統計

```powershell
cd "D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector"

# 使用 Python 快速統計
python -c "
import json
with open('download_progress.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
completed = len(data.get('completed', []))
failed = len(data.get('failed', []))
total = 606
print(f'已完成: {completed}/{total} ({completed/total*100:.1f}%)')
print(f'失敗: {failed}')
print(f'剩餘: {total - completed}')
print(f'總大小: {data.get(\"total_size_mb\", 0)/1024:.1f} GB')
"
```

---

## 4. 常見問題

### ❓ Q1: 下載速度太慢怎麼辦？

**A**: 
- 檢查網路連線速度
- 降低 `MAX_WORKERS` 避免頻寬分散
- 考慮使用 Aspera 加速（需額外配置）
- 避開 NCBI 伺服器高峰時段

### ❓ Q2: 遇到 "disk-limit exceeded" 錯誤

**A**:
```powershell
# 檢查磁碟空間
Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.DeviceID -in @('E:', 'D:') } | Select-Object DeviceID, @{Name='FreeSpaceGB'; Expression={[math]::Round($_.FreeSpace / 1GB, 2)}}

# 清理空間或修改 fasterq-dump 參數
# 編輯 batch_fastq_downloader.py 第 123 行，添加：
["run_id", "-O", str(output_dir), "--split-files", "--disk-limit", "500G"]
```

### ❓ Q3: 如何處理 "zombie file detected" 錯誤？

**A**: 
這表示 SRA 檔案損壞，需要重新下載：
```powershell
# 刪除損壞的檔案
Remove-Item -Recurse -Force "D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\SRR12180939"

# 從 download_progress.json 移除該樣本
# 重新執行下載
python batch_fastq_downloader.py
```

### ❓ Q4: 程式中斷後如何繼續？

**A**:
直接重新執行即可，程式會自動跳過已完成的樣本：
```powershell
python batch_fastq_downloader.py
```

### ❓ Q7: 按 Ctrl+C 後程式沒有立即停止？

**A**:
這是正常行為！程式使用優雅退出機制：
- ⏸️ 會等待當前正在執行的任務完成（最多 10 個並行任務）
- 💾 確保已完成的任務正確保存到進度檔案
- 🚫 不會啟動新的任務
- ⏱️ 通常在 1-3 分鐘內完全停止

**如果需要強制終止**:
```powershell
# 查找 Python 進程
Get-Process python

# 強制結束 (可能導致進度丟失)
Stop-Process -Name python -Force
```

### ❓ Q5: 如何只下載 SRA 不解壓？

**A**:
修改 `download_fastq()` 函數，註解掉步驟 2-4：
```python
# 註解掉第 118-174 行 (fasterq-dump、備份、清理步驟)
```

### ❓ Q6: 下載過程中 OneDrive 同步干擾

**A**:
```powershell
# 暫停 OneDrive 同步
# 右鍵點擊系統托盤的 OneDrive 圖標 -> 暫停同步 -> 24小時

# 或修改環境變數
$env:NCBI_HOME = "D:\ncbi"
```

---

## 5. 文件結構

### 📂 完整目錄樹

```
D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\
│
├── 📄 batch_fastq_downloader.py          # 批量下載主程式
├── 📄 check_sra_integrity.py             # 完整性檢查工具
├── 📄 runs.txt                            # 606 個樣本 ID 列表
├── 📄 download_progress.json              # 下載進度追蹤
├── 📄 sra_integrity_report.json           # 檢查報告 (執行檢查後生成)
├── 📄 SRA下載與檢查工具使用指南.md        # 本文檔
│
├── 📁 sratoolkit.3.2.1-win64\             # SRA Toolkit
│   └── 📁 bin\
│       ├── prefetch.exe                   # 下載工具
│       ├── fasterq-dump.exe               # 解壓工具
│       ├── vdb-validate.exe               # 驗證工具
│       └── sra-stat.exe                   # 統計工具
│
├── 📁 SRR10810025\                        # 臨時 SRA 目錄 (下載中)
│   └── SRR10810025.sra
├── 📁 SRR10810029\
│   └── SRR10810029.sra
└── ...

E:\fastq_data\                             # FASTQ 輸出
├── SRR10810025_1.fastq                    # 正向讀取
├── SRR10810025_2.fastq                    # 反向讀取
└── ...

E:\sra_files\                              # SRA 備份
├── SRR10810025.sra
└── ...
```

### 📋 關鍵檔案說明

| 檔案 | 用途 | 位置 |
|------|------|------|
| `batch_fastq_downloader.py` | 批量下載與解壓 | D 槽 data_collector |
| `check_sra_integrity.py` | 檢查檔案完整性 | D 槽 data_collector |
| `runs.txt` | 樣本 ID 列表 (606 個) | D 槽 data_collector |
| `download_progress.json` | 進度追蹤 | D 槽 data_collector |
| `sra_integrity_report.json` | 檢查報告 | D 槽 data_collector |
| `*.sra` | SRA 原始檔案 | E:\sra_files |
| `*.fastq` | FASTQ 解壓檔案 | E:\fastq_data |

---

## 📞 技術支援

### 相關資源

- **NCBI SRA Toolkit**: https://github.com/ncbi/sra-tools
- **SRA 資料庫**: https://www.ncbi.nlm.nih.gov/sra
- **fasterq-dump 文檔**: https://github.com/ncbi/sra-tools/wiki/HowTo:-fasterq-dump

### 日誌位置

- 下載日誌: 終端輸出
- 錯誤記錄: `download_progress.json` 的 `failed` 陣列
- 檢查報告: `sra_integrity_report.json`

---

## 📝 更新日誌

### 2025-10-07 v1.1
- ✅ 修復暫停功能 (加入信號處理器)
- ✅ 優雅退出機制 (等待當前任務完成)
- ✅ 改進中斷提示訊息

### 2025-10-07 v1.0
- ✅ 加入並行下載功能 (MAX_WORKERS=10)
- ✅ 建立完整性檢查工具
- ✅ 優化進度追蹤機制
- ✅ 增加實時秒數顯示

### 2025-10-06
- ✅ 延長超時設定 (120/150 分鐘)
- ✅ 解決 disk-limit 錯誤
- ✅ 修復 lock file 問題

### 2025-10-02
- ✅ 初始版本
- ✅ 四步驟自動化流程

---

**文檔版本**: 1.1  
**最後更新**: 2025-10-07  
**作者**: GitHub Copilot  
**專案路徑**: `D:\OneDrive\學校上課\課程\四上\科學大數據專題\data_collector\`

---

## 🔧 故障排除

### 程式控制問題

**問題**: 按 Ctrl+C 後等待時間過長  
**原因**: 並行任務需要完成當前步驟  
**解決**: 耐心等待 1-3 分鐘,或使用 `Stop-Process -Force` 強制終止 (可能丟失進度)

**問題**: 重新啟動後重複下載已完成的樣本  
**原因**: `download_progress.json` 未正確保存  
**解決**: 檢查檔案完整性,必要時手動編輯

**問題**: 並行數量過高導致系統卡頓  
**原因**: `MAX_WORKERS=10` 佔用過多系統資源  
**解決**: 降低至 `MAX_WORKERS=5` 或 `MAX_WORKERS=3`
