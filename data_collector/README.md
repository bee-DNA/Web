# MGnify Insecta 資料收集工具

這個資料夾包含一個自動化腳本，會透過 [MGnify JSON:API](https://www.ebi.ac.uk/metagenomics/api/docs) 抓取昆蟲 (`Insecta`) 相關生物域的樣本資訊，彙整並輸出 `CSV` 檔案。輸出的欄位包含：

- `biome_lineage`：MGnify 生物域路徑
- `biome_name`：易讀的生物域名稱
- `sample_accession`：樣本代碼
- `host_scientific_name`：宿主的學名
- `run_accession`：Run ID
- `experiment_type`：實驗類型

## 需求套件

- Python 3.9 以上
- `requests`

### 安裝套件

```powershell
C:/Python313/python.exe -m pip install requests
```

## 使用方式

```powershell
C:/Python313/python.exe mgnify_insecta_scraper.py --output insecta_runs.csv
```

執行後會在目前資料夾產生 `insecta_runs.csv`，內容即為整理好的主檔。腳本會自動處理分頁，並且去除重複的樣本／Run 組合。

> **注意**：MGnify API 為公開資源，請勿大量並行請求；本腳本已內建節流設定。若 API 回應失敗，腳本會自動重試三次。
