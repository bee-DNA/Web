#!/usr/bin/env python3
"""
Robust FASTQ batch downloader
穩定的批量FASTQ下載器
"""

import subprocess
import os
import sys
import time
import json
import signal
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 全局中斷標誌
interrupt_flag = False

def signal_handler(signum, frame):
    """處理 Ctrl+C 中斷信號"""
    global interrupt_flag
    print("\n\n⚠️  收到中斷信號，正在安全停止...")
    print("⏸️  等待當前任務完成後退出...")
    interrupt_flag = True


def run_sra_command_with_timer(sra_bin, command, args, timeout=3600):
    """執行SRA命令並顯示即時秒數"""
    import threading

    executable = sra_bin / f"{command}.exe"
    cmd = [str(executable)] + args

    start_time = time.time()
    completed = False

    def show_timer():
        while not completed:
            elapsed = int(time.time() - start_time)
            print(f"\r  執行中... {elapsed}秒", end="", flush=True)
            time.sleep(1)

    # 啟動計時器線程
    timer_thread = threading.Thread(target=show_timer, daemon=True)
    timer_thread.start()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="ignore",
        )
        completed = True
        time.sleep(0.1)  # 等待計時器線程更新
        print("\r", end="")  # 清除計時器顯示
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        completed = True
        time.sleep(0.1)
        print("\r", end="")
        return False, "", f"Timeout after {timeout}s"
    except Exception as e:
        completed = True
        time.sleep(0.1)
        print("\r", end="")
        return False, "", str(e)


def run_sra_command(sra_bin, command, args, timeout=3600):
    """執行SRA命令(無計時器版本)"""
    executable = sra_bin / f"{command}.exe"
    cmd = [str(executable)] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="ignore",
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", f"Timeout after {timeout}s"
    except Exception as e:
        return False, "", str(e)


def download_fastq(run_id, sra_bin, output_dir, progress_data, base_dir):
    """下載單個FASTQ"""
    global interrupt_flag
    
    # 檢查中斷標誌
    if interrupt_flag:
        print(f"\n⏸️  跳過 {run_id} (用戶中斷)")
        return False
    
    print(f"\n{'='*60}")
    print(f"📥 處理: {run_id}")
    print(f"{'='*60}")

    # 檢查是否已完成
    if run_id in progress_data.get("completed", []):
        print(f"✅ 已完成，跳過")
        return True

    start_time = time.time()

    # Step 1: prefetch (下載到 OneDrive 臨時目錄)
    print(f"  步驟 1/4: prefetch {run_id}...")
    step1_start = time.time()
    success, stdout, stderr = run_sra_command_with_timer(
        sra_bin, "prefetch", [run_id, "--max-size", "100G"], timeout=7200  # 120分鐘超時
    )
    step1_time = time.time() - step1_start

    if not success:
        print(f" ❌ 失敗 ({step1_time:.1f}秒)")
        print(f"  錯誤: {stderr[:100]}")
        progress_data["failed"].append(
            {
                "run_id": run_id,
                "step": "prefetch",
                "error": stderr[:200],
                "time": datetime.now().isoformat(),
            }
        )
        save_progress(progress_data)
        return False

    print(f"  ✅ 完成 ({step1_time:.1f}秒)")

    # Step 2: fasterq-dump (解壓到 E:\fastq_data)
    print(f"  步驟 2/4: fasterq-dump {run_id}...")
    step2_start = time.time()
    success, stdout, stderr = run_sra_command_with_timer(
        sra_bin,
        "fasterq-dump",
        [run_id, "-O", str(output_dir), "--split-files"],
        timeout=9000,  # 150分鐘超時
    )
    step2_time = time.time() - step2_start

    if not success:
        print(f"  ❌ 失敗 ({step2_time:.1f}秒)")
        print(f"  錯誤: {stderr[:100]}")
        progress_data["failed"].append(
            {
                "run_id": run_id,
                "step": "fasterq-dump",
                "error": stderr[:200],
                "time": datetime.now().isoformat(),
            }
        )
        save_progress(progress_data)
        return False

    print(f"  ✅ 完成 ({step2_time:.1f}秒)")

    # 檢查 FASTQ 檔案
    fastq_files = list(output_dir.glob(f"{run_id}*"))
    if not fastq_files:
        print(f"  ⚠️  找不到輸出檔案")
        return False

    total_size = sum(f.stat().st_size for f in fastq_files) / (1024 * 1024)

    print(f"  📁 FASTQ 檔案: {len(fastq_files)} 個")
    print(f"  💾 大小: {total_size:.1f} MB")

    # Step 3: 備份 SRA 到 E 槽
    print(f"  步驟 3/4: 備份 SRA 到 E 槽...", end="", flush=True)
    step3_start = time.time()
    sra_source = base_dir / run_id / f"{run_id}.sra"
    sra_backup_dir = Path("E:/sra_files") / run_id

    try:
        if sra_source.exists():
            sra_backup_dir.mkdir(parents=True, exist_ok=True)
            sra_dest = sra_backup_dir / f"{run_id}.sra"

            # 複製 SRA 檔案到 E 槽
            import shutil

            shutil.copy2(sra_source, sra_dest)

            step3_time = time.time() - step3_start
            sra_size = sra_source.stat().st_size / (1024 * 1024)
            print(f" ✅ 完成 ({sra_size:.1f} MB, {step3_time:.1f}秒)")
        else:
            step3_time = time.time() - step3_start
            print(f" ⚠️  找不到 SRA 檔案 ({step3_time:.1f}秒)")
    except Exception as e:
        step3_time = time.time() - step3_start
        print(f" ⚠️  警告: {str(e)} ({step3_time:.1f}秒)")

    # Step 4: 清理 OneDrive 臨時資料夾
    print(f"  步驟 4/4: 清理臨時資料夾...", end="", flush=True)
    step4_start = time.time()
    sra_temp_dir = base_dir / run_id

    try:
        if sra_temp_dir.exists():
            import shutil

            shutil.rmtree(sra_temp_dir)
            step4_time = time.time() - step4_start
            print(f" ✅ 完成 ({step4_time:.1f}秒)")
        else:
            step4_time = time.time() - step4_start
            print(f" ⚠️  資料夾不存在 ({step4_time:.1f}秒)")
    except Exception as e:
        step4_time = time.time() - step4_start
        print(f" ⚠️  警告: {str(e)} ({step4_time:.1f}秒)")

    elapsed = time.time() - start_time
    print(f"  ⏱️  總時間: {elapsed:.1f} 秒")

    progress_data["completed"].append(run_id)
    progress_data["total_size_mb"] = progress_data.get("total_size_mb", 0) + total_size

    # 每完成一個就保存
    save_progress(progress_data)

    return True


def save_progress(progress_data):
    """保存進度"""
    progress_file = Path(__file__).parent / "download_progress.json"
    progress_data["last_update"] = datetime.now().isoformat()

    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)


def load_progress():
    """載入進度"""
    progress_file = Path(__file__).parent / "download_progress.json"

    if progress_file.exists():
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 確保completed是列表
                if "completed" in data and isinstance(data["completed"], list):
                    # 處理舊格式（dict）轉新格式（string）
                    data["completed"] = [
                        item["run_id"] if isinstance(item, dict) else item
                        for item in data["completed"]
                    ]
                return data
        except:
            pass

    return {
        "completed": [],
        "failed": [],
        "total_size_mb": 0,
        "start_time": datetime.now().isoformat(),
    }


def main():
    """主程序"""
    global interrupt_flag
    
    # 註冊信號處理器
    signal.signal(signal.SIGINT, signal_handler)
    
    # 設定並行下載數量
    MAX_WORKERS = 10

    # 設定環境變數，避免OneDrive同步鎖定問題
    os.environ["NCBI_HOME"] = "D:\\ncbi"
    os.environ["VDB_CONFIG"] = str(Path(__file__).parent / ".ncbirc")

    # 設定路徑
    base_dir = Path(__file__).parent
    sra_bin = base_dir / "sratoolkit.3.2.1-win64" / "bin"
    output_dir = Path("E:/fastq_data")  # 改為 E 槽
    runs_file = base_dir / "runs.txt"

    # 檢查
    if not sra_bin.exists():
        print(f"❌ SRA Toolkit 不存在: {sra_bin}")
        return

    if not runs_file.exists():
        print(f"❌ runs.txt 不存在: {runs_file}")
        return

    # 創建輸出目錄
    output_dir.mkdir(parents=True, exist_ok=True)

    # 讀取任務列表
    with open(runs_file, "r") as f:
        all_runs = [line.strip() for line in f if line.strip()]

    # 載入進度
    progress_data = load_progress()

    completed = len(progress_data.get("completed", []))
    failed = len(progress_data.get("failed", []))
    total = len(all_runs)
    remaining = total - completed

    print(f"\n{'='*60}")
    print(f"🚀 FASTQ 批量下載器")
    print(f"{'='*60}")
    print(f"  總任務: {total}")
    print(f"  已完成: {completed} ({completed/total*100:.1f}%)")
    print(f"  失敗: {failed}")
    print(f"  剩餘: {remaining}")
    print(f"  並行數: {MAX_WORKERS}")
    print(f"  輸出: {output_dir}")
    print(f"{'='*60}\n")

    if remaining == 0:
        print("🎉 所有任務已完成！")
        return

    # 開始下載
    success_count = 0
    fail_count = 0
    batch_start_time = time.time()
    processed_in_batch = 0
    lock = threading.Lock()

    # 過濾出需要處理的任務
    pending_runs = [
        run_id
        for run_id in all_runs
        if run_id not in progress_data.get("completed", [])
    ]

    # 使用並行下載
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任務
        future_to_run = {
            executor.submit(
                download_fastq, run_id, sra_bin, output_dir, progress_data, base_dir
            ): run_id
            for run_id in pending_runs
        }

        for future in as_completed(future_to_run):
            # 檢查中斷標誌
            if interrupt_flag:
                print("\n⏸️  停止接收新結果...")
                break
                
            run_id = future_to_run[future]
            try:
                success = future.result()

                with lock:
                    if success:
                        success_count += 1
                        processed_in_batch += 1
                    else:
                        fail_count += 1

                    # 計算預估剩餘時間
                    if processed_in_batch > 0:
                        elapsed_time = time.time() - batch_start_time
                        avg_time_per_item = elapsed_time / processed_in_batch
                        remaining_items = len(pending_runs) - processed_in_batch
                        estimated_seconds = avg_time_per_item * remaining_items

                        hours = int(estimated_seconds // 3600)
                        minutes = int((estimated_seconds % 3600) // 60)
                        seconds = int(estimated_seconds % 60)

                        if hours > 0:
                            eta_str = f"{hours}小時{minutes}分鐘{seconds}秒"
                        elif minutes > 0:
                            eta_str = f"{minutes}分鐘{seconds}秒"
                        else:
                            eta_str = f"{seconds}秒"

                        print(
                            f"\n[{processed_in_batch}/{len(pending_runs)}] 進度: {processed_in_batch/len(pending_runs)*100:.1f}% | ⏱️  預估剩餘: {eta_str}"
                        )

                    # 每10個顯示統計
                    if processed_in_batch % 10 == 0:
                        current_completed = len(progress_data.get("completed", []))
                        current_failed = len(progress_data.get("failed", []))
                        total_size = progress_data.get("total_size_mb", 0)

                        elapsed_time = time.time() - batch_start_time
                        avg_time = (
                            elapsed_time / processed_in_batch
                            if processed_in_batch > 0
                            else 0
                        )

                        print(f"\n{'='*60}")
                        print(f"📊 中期報告 [{processed_in_batch}/{total}]")
                        print(f"  成功: {current_completed}")
                        print(f"  失敗: {current_failed}")
                        print(
                            f"  總大小: {total_size:.1f} MB ({total_size/1024:.2f} GB)"
                        )
                        print(f"  平均處理時間: {avg_time:.1f} 秒/個")
                        print(f"{'='*60}\n")

            except Exception as e:
                with lock:
                    fail_count += 1
                    print(f"\n❌ 處理 {run_id} 時發生錯誤: {e}")

    # 最終報告
    final_completed = len(progress_data.get("completed", []))
    final_failed = len(progress_data.get("failed", []))
    final_size = progress_data.get("total_size_mb", 0)

    print(f"\n{'='*60}")
    print(f"🎉 下載完成！")
    print(f"{'='*60}")
    print(f"  總任務: {total}")
    print(f"  成功: {final_completed} ({final_completed/total*100:.1f}%)")
    print(f"  失敗: {final_failed} ({final_failed/total*100:.1f}%)")
    print(f"  總大小: {final_size:.1f} MB ({final_size/1024:.2f} GB)")
    print(f"{'='*60}\n")

    if final_failed > 0:
        print("❌ 失敗的任務:")
        for item in progress_data.get("failed", [])[-10:]:
            print(f"  - {item.get('run_id')}: {item.get('step')}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        interrupt_flag = True
        print("\n\n⚠️  下載被用戶中斷")
        print("💾 進度已保存到 download_progress.json")
        print("🔄 下次執行將從斷點繼續")
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        import traceback

        traceback.print_exc()
