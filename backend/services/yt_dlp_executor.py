import os
import signal
import shlex
import subprocess
import asyncio
import re
from typing import Dict, List, Callable, Optional
from datetime import datetime
import json


class YtDlpExecutor:
    """yt-dlp subprocess 実行・制御"""
    
    def __init__(self, yt_dlp_path: str):
        self.yt_dlp_path = yt_dlp_path
        self.process: Optional[subprocess.Popen] = None
        self.progress_callback: Optional[Callable] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
    
    def set_progress_callback(self, callback: Callable):
        """プログレス更新コールバック設定"""
        self.progress_callback = callback
    
    async def execute(
        self,
        url: str,
        parameters: Dict[str, any],
        output_template: str = "%(title)s.%(ext)s"
    ) -> Dict:
        """yt-dlpを実行"""
        try:
            if not self.yt_dlp_path:
                raise RuntimeError("yt-dlp path is not configured")

            # パラメータからCLI引数を構築
            args = self._build_args(url, parameters, output_template)
            
            # プロセス起動
            self.process = subprocess.Popen(
                [self.yt_dlp_path] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self._loop = asyncio.get_running_loop()
            result = await asyncio.to_thread(self._read_output)
            return result
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filename": None,
            }
    
    def _dispatch_progress(self, progress_info: Dict):
        if not self.progress_callback or not self._loop:
            return

        if asyncio.iscoroutinefunction(self.progress_callback):
            asyncio.run_coroutine_threadsafe(self.progress_callback(progress_info), self._loop)
        else:
            self._loop.call_soon_threadsafe(self.progress_callback, progress_info)

    def _read_output(self) -> Dict:
        """プロセス出力を読み込み"""
        filename = None
        error_output = []
        
        try:
            while self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if not line:
                    break
                
                line = line.strip()
                
                # プログレス情報を抽出
                progress_info = self._parse_progress_line(line)
                if progress_info:
                    self._dispatch_progress(progress_info)
                
                # ファイル名を抽出
                if "Destination:" in line:
                    filename = line.split("Destination:")[-1].strip()
                
                # エラーメッセージをキャッチ
                if "ERROR" in line:
                    error_output.append(line)
            
            if self.process:
                remaining_stdout, remaining_stderr = self.process.communicate()
                if remaining_stdout:
                    for line in remaining_stdout.split("\n"):
                        if line.strip():
                            progress_info = self._parse_progress_line(line)
                            if progress_info:
                                self._dispatch_progress(progress_info)
                if remaining_stderr:
                    error_output.extend(remaining_stderr.split("\n"))
            
            return_code = self.process.returncode if self.process else -1
            
            if return_code == 0:
                return {
                    "success": True,
                    "filename": filename,
                    "return_code": return_code,
                }
            else:
                return {
                    "success": False,
                    "error": "\n".join(error_output),
                    "filename": filename,
                    "return_code": return_code,
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filename": filename,
            }
    
    def _parse_progress_line(self, line: str) -> Optional[Dict]:
        """プログレス行をパース"""
        # 例: "[download]  45.5% of 100.00MiB at 2.50MiB/s ETA 00:02:15"
        
        match = re.search(r'\[download\]\s+(\d+\.\d+)%', line)
        if match:
            percent = float(match.group(1))
            
            speed_match = re.search(r'at\s+([\d.]+MiB|KiB|GiB)/s', line)
            speed = speed_match.group(1) if speed_match else None
            
            eta_match = re.search(r'ETA\s+(\d{2}:\d{2}:\d{2})', line)
            eta = eta_match.group(1) if eta_match else None
            
            return {
                "percent": percent,
                "speed": speed,
                "eta": eta,
            }
        
        return None
    
    def pause(self):
        """プロセス一時停止"""
        if self.process:
            if os.name == "posix":
                self.process.send_signal(signal.SIGSTOP)
            else:
                print("⚠️ Pause is not supported on this platform.")
    
    def resume(self):
        """プロセス再開"""
        if self.process:
            if os.name == "posix":
                self.process.send_signal(signal.SIGCONT)
            else:
                print("⚠️ Resume is not supported on this platform.")
    
    def cancel(self):
        """プロセスキャンセル"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
    
    def _build_args(self, url: str, parameters: Dict[str, any], output_template: str) -> List[str]:
        """パラメータからCLI引数を構築"""
        args = [url]
        
        # 出力テンプレート
        args.extend(["-o", output_template])
        
        # パラメータをCLI引数に変換
        raw_options = None
        if "raw_options" in parameters:
            raw_options = parameters.pop("raw_options")

        for key, value in parameters.items():
            if value is None or value is False:
                continue

            cli_key = f"--{key.replace('_', '-') }"

            if isinstance(value, bool):
                if value:
                    args.append(cli_key)
            elif isinstance(value, list):
                args.append(cli_key)
                args.extend(str(item) for item in value)
            else:
                args.append(cli_key)
                args.append(str(value))

        if isinstance(raw_options, str) and raw_options.strip():
            try:
                args.extend(shlex.split(raw_options))
            except ValueError:
                args.extend(raw_options.strip().split())

        # 進捗表示を有効化
        args.append("--progress")

        return args
