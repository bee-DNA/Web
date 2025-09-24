"""
資料處理工具模組
用於處理各種格式的地理資料
"""

import pandas as pd
import json
import requests
from typing import Dict, List, Optional


class WorldDataProcessor:
    """世界資料處理器"""

    def __init__(self):
        self.country_codes = self._load_country_codes()

    def _load_country_codes(self) -> Dict[str, str]:
        """載入國家代碼對照表"""
        # 簡化的國家代碼對照
        codes = {
            "China": "CHN",
            "India": "IND",
            "United States": "USA",
            "Indonesia": "IDN",
            "Pakistan": "PAK",
            "Brazil": "BRA",
            "Nigeria": "NGA",
            "Bangladesh": "BGD",
            "Russia": "RUS",
            "Mexico": "MEX",
            "Japan": "JPN",
            "Germany": "DEU",
            "Iran": "IRN",
            "Turkey": "TUR",
            "Vietnam": "VNM",
            "Philippines": "PHL",
            "Ethiopia": "ETH",
            "Egypt": "EGY",
            "United Kingdom": "GBR",
            "France": "FRA",
            "Italy": "ITA",
            "South Africa": "ZAF",
            "Tanzania": "TZA",
            "Kenya": "KEN",
            "Uganda": "UGA",
            "Algeria": "DZA",
            "Sudan": "SDN",
            "Ukraine": "UKR",
            "Iraq": "IRQ",
            "Afghanistan": "AFG",
            "Poland": "POL",
            "Canada": "CAN",
            "Morocco": "MAR",
            "Saudi Arabia": "SAU",
            "Uzbekistan": "UZB",
            "Peru": "PER",
            "Angola": "AGO",
            "Malaysia": "MYS",
            "Mozambique": "MOZ",
            "Ghana": "GHA",
            "Yemen": "YEM",
            "Nepal": "NPL",
            "Venezuela": "VEN",
            "Madagascar": "MDG",
            "Cameroon": "CMR",
        }
        return codes

    def load_csv_data(self, file_path: str) -> pd.DataFrame:
        """載入 CSV 資料"""
        try:
            df = pd.read_csv(file_path, encoding="utf-8")
            return df
        except UnicodeDecodeError:
            # 嘗試其他編碼
            for encoding in ["gbk", "big5", "latin-1"]:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    return df
                except:
                    continue
            raise ValueError(f"無法讀取檔案 {file_path}")

    def add_country_codes(
        self, df: pd.DataFrame, country_column: str = "country"
    ) -> pd.DataFrame:
        """為資料框加上國家ISO代碼"""
        df = df.copy()
        df["iso_alpha"] = df[country_column].map(self.country_codes)

        # 找出沒有對應代碼的國家
        missing_codes = df[df["iso_alpha"].isna()][country_column].unique()
        if len(missing_codes) > 0:
            print(f"⚠️ 以下國家沒有ISO代碼對照：{list(missing_codes)}")

        return df

    def validate_data(self, df: pd.DataFrame) -> Dict[str, any]:
        """驗證資料品質"""
        validation_report = {
            "total_rows": len(df),
            "missing_data": {},
            "data_types": {},
            "summary_stats": {},
        }

        # 檢查缺失值
        for col in df.columns:
            missing_count = df[col].isna().sum()
            missing_pct = (missing_count / len(df)) * 100
            validation_report["missing_data"][col] = {
                "count": missing_count,
                "percentage": round(missing_pct, 2),
            }

        # 檢查資料類型
        validation_report["data_types"] = df.dtypes.to_dict()

        # 數值欄位的統計摘要
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
        for col in numeric_cols:
            validation_report["summary_stats"][col] = {
                "min": df[col].min(),
                "max": df[col].max(),
                "mean": df[col].mean(),
                "median": df[col].median(),
            }

        return validation_report

    def create_sample_world_data(self) -> pd.DataFrame:
        """建立範例世界資料集"""
        data = {
            "country": [
                "China",
                "India",
                "United States",
                "Indonesia",
                "Pakistan",
                "Brazil",
                "Nigeria",
                "Bangladesh",
                "Russia",
                "Mexico",
                "Japan",
                "Germany",
                "Iran",
                "Turkey",
                "Vietnam",
                "Philippines",
                "Ethiopia",
                "Egypt",
                "United Kingdom",
                "France",
                "Italy",
                "South Africa",
                "Tanzania",
                "Kenya",
                "Uganda",
            ],
            "population_2023": [
                1439323776,
                1380004385,
                331002651,
                273523615,
                220892340,
                212559417,
                206139589,
                164689383,
                145934462,
                128932753,
                126476461,
                83783942,
                83992949,
                84339067,
                97338579,
                109581078,
                114963588,
                102334404,
                67886011,
                65273511,
                60461826,
                59308690,
                59734218,
                53771296,
                45741007,
            ],
            "gdp_2023": [
                17734.1,
                3735.9,
                25462.7,
                1417.4,
                374.7,
                2055.5,
                440.8,
                460.2,
                2240.4,
                1688.9,
                4937.4,
                4259.9,
                231.3,
                815.3,
                408.8,
                394.1,
                111.3,
                469.4,
                3131.4,
                2937.5,
                2107.7,
                419.0,
                67.8,
                109.1,
                47.7,
            ],
            "life_expectancy": [
                76.9,
                69.4,
                78.9,
                71.7,
                67.3,
                75.9,
                54.7,
                72.6,
                72.6,
                75.1,
                84.6,
                81.3,
                76.7,
                77.7,
                75.4,
                71.2,
                66.6,
                72.0,
                81.3,
                82.7,
                83.4,
                64.1,
                65.5,
                66.7,
                63.4,
            ],
            "continent": [
                "Asia",
                "Asia",
                "North America",
                "Asia",
                "Asia",
                "South America",
                "Africa",
                "Asia",
                "Europe",
                "North America",
                "Asia",
                "Europe",
                "Asia",
                "Asia",
                "Asia",
                "Asia",
                "Africa",
                "Africa",
                "Europe",
                "Europe",
                "Europe",
                "Africa",
                "Africa",
                "Africa",
                "Africa",
            ],
            "capital": [
                "Beijing",
                "New Delhi",
                "Washington D.C.",
                "Jakarta",
                "Islamabad",
                "Brasília",
                "Abuja",
                "Dhaka",
                "Moscow",
                "Mexico City",
                "Tokyo",
                "Berlin",
                "Tehran",
                "Ankara",
                "Hanoi",
                "Manila",
                "Addis Ababa",
                "Cairo",
                "London",
                "Paris",
                "Rome",
                "Cape Town",
                "Dodoma",
                "Nairobi",
                "Kampala",
            ],
        }

        df = pd.DataFrame(data)
        df = self.add_country_codes(df)
        return df


def export_sample_data():
    """匯出範例資料到CSV檔案"""
    processor = WorldDataProcessor()
    df = processor.create_sample_world_data()

    # 儲存為CSV
    output_file = "world_data_sample.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ 範例資料已儲存到: {output_file}")

    # 顯示資料驗證報告
    report = processor.validate_data(df)
    print("\n📊 資料驗證報告:")
    print(f"總筆數: {report['total_rows']}")
    print("\n缺失值統計:")
    for col, info in report["missing_data"].items():
        if info["count"] > 0:
            print(f"  {col}: {info['count']} ({info['percentage']}%)")

    return df


if __name__ == "__main__":
    # 執行範例
    print("🌍 世界資料處理工具")
    print("=" * 40)

    # 建立並匯出範例資料
    df = export_sample_data()

    print(f"\n📋 資料預覽:")
    print(df.head())

    print(f"\n📊 資料摘要:")
    print(df.describe())
