#!/usr/bin/env python3
"""
檢查 SRA 檔案完整性
Check SRA files integrity
"""

import subprocess
from pathlib import Path
import json
from datetime import datetime


def check_sra_file(sra_file, sra_bin):
    """檢查單個 SRA 檔案的完整性"""
    vdb_validate = sra_bin / "vdb-validate.exe"
    
    if not vdb_validate.exists():
        # 如果沒有 vdb-validate，使用 sra-stat 作為替代
        sra_stat = sra_bin / "sra-stat.exe"
        if not sra_stat.exists():
            return None, "檢查工具不存在"
    
    try:
        # 使用 vdb-validate 檢查檔案完整性
        result = subprocess.run(
            [str(vdb_validate), str(sra_file)],
            capture_output=True,
            text=True,
            timeout=300,  # 5分鐘超時
            encoding="utf-8",
            errors="ignore"
        )
        
        # vdb-validate 如果返回 0 表示檔案完整
        if result.returncode == 0:
            return True, "完整"
        else:
            return False, result.stderr[:200]
            
    except subprocess.TimeoutExpired:
        return False, "檢查超時"
    except Exception as e:
        return False, str(e)


def get_sra_info(sra_file, sra_bin):
    """獲取 SRA 檔案資訊"""
    sra_stat = sra_bin / "sra-stat.exe"
    
    try:
        result = subprocess.run(
            [str(sra_stat), "--meta", "--quick", str(sra_file)],
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8",
            errors="ignore"
        )
        
        if result.returncode == 0:
            # 解析輸出獲取讀取數量
            for line in result.stdout.split('\n'):
                if 'spots' in line.lower():
                    return line.strip()
            return "資訊可用"
        else:
            return "無法獲取資訊"
            
    except Exception as e:
        return f"錯誤: {str(e)}"


def check_all_sra_files():
    """檢查所有 SRA 檔案"""
    base_dir = Path("D:/OneDrive/學校上課/課程/四上/科學大數據專題/data_collector")
    sra_bin = base_dir / "sratoolkit.3.2.1-win64" / "bin"
    
    print(f"\n{'='*80}")
    print(f"🔍 SRA 檔案完整性檢查")
    print(f"{'='*80}")
    print(f"📁 掃描目錄: {base_dir}")
    print(f"🛠️  SRA Toolkit: {sra_bin}")
    print(f"{'='*80}\n")
    
    # 找出所有 SRA 檔案
    sra_files = list(base_dir.glob("*/SRR*.sra"))
    
    if not sra_files:
        print("❌ 找不到任何 SRA 檔案")
        return
    
    print(f"📊 找到 {len(sra_files)} 個 SRA 檔案\n")
    
    results = {
        "valid": [],
        "invalid": [],
        "unknown": [],
        "total_size_mb": 0,
        "check_time": datetime.now().isoformat()
    }
    
    # 檢查每個檔案
    for i, sra_file in enumerate(sra_files, 1):
        sample_id = sra_file.parent.name
        file_size = sra_file.stat().st_size / (1024 * 1024)  # MB
        results["total_size_mb"] += file_size
        
        print(f"[{i}/{len(sra_files)}] 檢查: {sample_id}")
        print(f"  📁 檔案: {sra_file.name}")
        print(f"  💾 大小: {file_size:.1f} MB")
        
        # 快速檢查: 使用 sra-stat 獲取資訊
        print(f"  🔍 快速檢查...", end="", flush=True)
        info = get_sra_info(sra_file, sra_bin)
        print(f" {info}")
        
        # 完整性驗證
        print(f"  ✓ 完整性驗證...", end="", flush=True)
        is_valid, message = check_sra_file(sra_file, sra_bin)
        
        if is_valid is True:
            print(f" ✅ {message}")
            results["valid"].append({
                "sample_id": sample_id,
                "file": str(sra_file),
                "size_mb": file_size,
                "info": info
            })
        elif is_valid is False:
            print(f" ❌ {message}")
            results["invalid"].append({
                "sample_id": sample_id,
                "file": str(sra_file),
                "size_mb": file_size,
                "error": message
            })
        else:
            print(f" ⚠️  {message}")
            results["unknown"].append({
                "sample_id": sample_id,
                "file": str(sra_file),
                "size_mb": file_size,
                "note": message
            })
        
        print()
    
    # 保存結果
    report_file = base_dir / "sra_integrity_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 顯示摘要
    print(f"\n{'='*80}")
    print(f"📊 檢查完成摘要")
    print(f"{'='*80}")
    print(f"  總檔案數: {len(sra_files)}")
    print(f"  ✅ 完整: {len(results['valid'])} ({len(results['valid'])/len(sra_files)*100:.1f}%)")
    print(f"  ❌ 損壞: {len(results['invalid'])} ({len(results['invalid'])/len(sra_files)*100:.1f}%)")
    print(f"  ⚠️  未知: {len(results['unknown'])} ({len(results['unknown'])/len(sra_files)*100:.1f}%)")
    print(f"  💾 總大小: {results['total_size_mb']:.1f} MB ({results['total_size_mb']/1024:.2f} GB)")
    print(f"  📄 報告: {report_file}")
    print(f"{'='*80}\n")
    
    # 顯示損壞的檔案
    if results["invalid"]:
        print(f"❌ 損壞的檔案列表:")
        for item in results["invalid"]:
            print(f"  - {item['sample_id']}: {item['error']}")
        print()
    
    return results


def quick_check_all_sra_files():
    """快速檢查所有 SRA 檔案 (只檢查檔案大小和可讀性)"""
    base_dir = Path("D:/OneDrive/學校上課/課程/四上/科學大數據專題/data_collector")
    
    print(f"\n{'='*80}")
    print(f"⚡ SRA 檔案快速檢查 (檔案大小檢查)")
    print(f"{'='*80}")
    print(f"📁 掃描目錄: {base_dir}\n")
    
    # 找出所有 SRA 檔案
    sra_files = list(base_dir.glob("*/SRR*.sra"))
    
    if not sra_files:
        print("❌ 找不到任何 SRA 檔案")
        return
    
    print(f"📊 找到 {len(sra_files)} 個 SRA 檔案\n")
    
    results = {
        "valid": [],
        "suspicious": [],  # 可疑 (檔案太小)
        "total_size_mb": 0
    }
    
    for i, sra_file in enumerate(sra_files, 1):
        sample_id = sra_file.parent.name
        file_size = sra_file.stat().st_size / (1024 * 1024)  # MB
        results["total_size_mb"] += file_size
        
        # 快速判斷: SRA 檔案通常應該 > 100 MB
        # 如果太小可能不完整
        if file_size < 10:  # 小於 10 MB 可能有問題
            status = "⚠️  可疑 (檔案太小)"
            results["suspicious"].append({
                "sample_id": sample_id,
                "size_mb": file_size
            })
        else:
            status = "✅ 正常"
            results["valid"].append({
                "sample_id": sample_id,
                "size_mb": file_size
            })
        
        print(f"[{i}/{len(sra_files)}] {sample_id}: {file_size:.1f} MB - {status}")
    
    # 顯示摘要
    print(f"\n{'='*80}")
    print(f"📊 快速檢查摘要")
    print(f"{'='*80}")
    print(f"  總檔案數: {len(sra_files)}")
    print(f"  ✅ 正常: {len(results['valid'])} ({len(results['valid'])/len(sra_files)*100:.1f}%)")
    print(f"  ⚠️  可疑: {len(results['suspicious'])} ({len(results['suspicious'])/len(sra_files)*100:.1f}%)")
    print(f"  💾 總大小: {results['total_size_mb']:.1f} MB ({results['total_size_mb']/1024:.2f} GB)")
    print(f"{'='*80}\n")
    
    if results["suspicious"]:
        print(f"⚠️  可疑檔案列表 (檔案太小):")
        for item in results["suspicious"]:
            print(f"  - {item['sample_id']}: {item['size_mb']:.1f} MB")
        print()
    
    return results


if __name__ == "__main__":
    # 直接執行完整檢查
    check_all_sra_files()
