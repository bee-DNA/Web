# MGnify Insecta 資料收集工具

這個資料夾包含一個自動化腳本，會透過 [MGnify JSON:API](https://www.ebi.ac.uk/metagenomics/api/docs) 抓取昆蟲 (`Insecta`) 相關生物域的樣本資訊，彙整並輸出 `CSV` 檔案。

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

## 輸出檔案

- `insecta_runs.csv`：預設輸出的完整主檔，涵蓋 Insecta 與其消化系統兩個生物域下，所有已有分析結果的樣本與 Run 對應關係。
- `insecta_runs_sample.csv`：同欄位格式的示範檔案，方便快速檢視欄位內容與排版；資料取自最新執行結果的前幾頁。

### 欄位用途

| 欄位名稱 | 來源 / 內容 | 用途 |
| --- | --- | --- |
| `biome_lineage` | MGnify 生物域的層級代碼 (如 `root:Host-associated:Insecta`) | 讓使用者依層級篩選或比對不同生物域資料 |
| `biome_name` | 生物域對應的易讀名稱 | 報表或圖表呈現時的顯示欄位 |
| `sample_accession` | MGnify / ENA 樣本 accession (SRS*) | 對應到樣本詳細資訊或進一步下載 metadata |
| `host_scientific_name` | 樣本 metadata 中的宿主學名 | 確認樣本來源昆蟲種類，支援分群統計 |
| `run_accession` | 具分析結果的 Run accession (SRR*等) | 連結到對應的測序資料與分析報告 |
| `experiment_type` | Run 的實驗類型 (如 amplicon、metagenomic 等) | 區分資料生成流程，有助於後續資料清理與分析 |

> **注意**：MGnify API 為公開資源，請勿大量並行請求；本腳本已內建節流設定。若 API 回應失敗，腳本會自動重試三次。
