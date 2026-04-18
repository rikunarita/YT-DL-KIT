import json
import subprocess
from typing import Dict, List, Optional
from ..models import YtDlpParameter


class ConfigParser:
    """yt-dlpパラメータ解析と検証"""
    
    def __init__(self, yt_dlp_path: Optional[str] = None):
        self.yt_dlp_path = yt_dlp_path
        self.parameters_metadata: Optional[Dict[str, YtDlpParameter]] = None
    
    async def generate_metadata(self) -> Dict[str, YtDlpParameter]:
        """yt-dlpのメタデータを生成"""
        if self.parameters_metadata:
            return self.parameters_metadata
        
        # yt-dlp --help の出力を取得
        try:
            result = subprocess.run(
                [self.yt_dlp_path, "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            help_text = result.stdout
        except Exception as e:
            print(f"⚠️  Failed to get yt-dlp help: {e}")
            return self._get_default_parameters()
        
        # メタデータを手動で定義（パース複雑性を考慮）
        self.parameters_metadata = self._define_parameters()
        
        return self.parameters_metadata
    
    def _define_parameters(self) -> Dict[str, YtDlpParameter]:
        """yt-dlpパラメータメタデータを定義"""
        return {
            # 基本パラメータ (~35個)
            "format": YtDlpParameter(
                name="format",
                category="Format Selection",
                description="動画形式を選択 (例: best, mp4, 720p)",
                type="string",
                default_value="best",
                ui_control="autocomplete_with_suggestions"
            ),
            "extract_audio": YtDlpParameter(
                name="extract_audio",
                category="Post-Processing",
                description="音声のみを抽出",
                type="bool",
                default_value=False,
                depends_on=["format"],
            ),
            "audio_format": YtDlpParameter(
                name="audio_format",
                category="Post-Processing",
                description="音声フォーマット (mp3, m4a, wav等)",
                type="choice",
                default_value="mp3",
                choices=["mp3", "m4a", "wav", "opus", "vorbis", "aac", "flac"],
                depends_on=["extract_audio"],
            ),
            "audio_quality": YtDlpParameter(
                name="audio_quality",
                category="Post-Processing",
                description="音声品質 (0-9, 0が最高)",
                type="int",
                default_value=5,
                depends_on=["extract_audio"],
            ),
            "write_subs": YtDlpParameter(
                name="write_subs",
                category="Subtitle Options",
                description="字幕をダウンロード",
                type="bool",
                default_value=False,
            ),
            "sub_langs": YtDlpParameter(
                name="sub_langs",
                category="Subtitle Options",
                description="字幕言語 (en, ja, all等)",
                type="string",
                default_value="en",
                depends_on=["write_subs"],
            ),
            "skip_unavailable_subs": YtDlpParameter(
                name="skip_unavailable_subs",
                category="Subtitle Options",
                description="利用できない字幕をスキップ",
                type="bool",
                default_value=True,
            ),
            "write_thumbnail": YtDlpParameter(
                name="write_thumbnail",
                category="Download Options",
                description="サムネイルをダウンロード",
                type="bool",
                default_value=False,
            ),
            "write_info_json": YtDlpParameter(
                name="write_info_json",
                category="Download Options",
                description="メタデータをJSON形式で保存",
                type="bool",
                default_value=False,
            ),
            "username": YtDlpParameter(
                name="username",
                category="Authentication Options",
                description="ログインユーザー名",
                type="string",
                default_value=None,
            ),
            "password": YtDlpParameter(
                name="password",
                category="Authentication Options",
                description="ログインパスワード",
                type="string",
                default_value=None,
            ),
            "proxy": YtDlpParameter(
                name="proxy",
                category="Network Options",
                description="プロキシURL",
                type="string",
                default_value=None,
            ),
            "socket_timeout": YtDlpParameter(
                name="socket_timeout",
                category="Network Options",
                description="ソケットタイムアウト (秒)",
                type="int",
                default_value=30,
            ),
            "retries": YtDlpParameter(
                name="retries",
                category="Download Options",
                description="リトライ回数",
                type="int",
                default_value=3,
            ),
            "fragment_retries": YtDlpParameter(
                name="fragment_retries",
                category="Download Options",
                description="フラグメントのリトライ回数",
                type="int",
                default_value=3,
            ),
            "skip_unavailable_fragments": YtDlpParameter(
                name="skip_unavailable_fragments",
                category="Download Options",
                description="利用できないフラグメントをスキップ",
                type="bool",
                default_value=True,
            ),
            "playlist_start": YtDlpParameter(
                name="playlist_start",
                category="Selection Options",
                description="プレイリスト開始インデックス",
                type="int",
                default_value=None,
            ),
            "playlist_end": YtDlpParameter(
                name="playlist_end",
                category="Selection Options",
                description="プレイリスト終了インデックス",
                type="int",
                default_value=None,
            ),
            "max_downloads": YtDlpParameter(
                name="max_downloads",
                category="Selection Options",
                description="最大ダウンロード数",
                type="int",
                default_value=None,
            ),
            "break_on_existing": YtDlpParameter(
                name="break_on_existing",
                category="Selection Options",
                description="既存ファイルで停止",
                type="bool",
                default_value=False,
            ),
            "date": YtDlpParameter(
                name="date",
                category="Selection Options",
                description="日付フィルタ (YYYYMMDD形式)",
                type="string",
                default_value=None,
            ),
            "dateafter": YtDlpParameter(
                name="dateafter",
                category="Selection Options",
                description="指定日付以後",
                type="string",
                default_value=None,
            ),
            "datebefore": YtDlpParameter(
                name="datebefore",
                category="Selection Options",
                description="指定日付以前",
                type="string",
                default_value=None,
            ),
            "no_warnings": YtDlpParameter(
                name="no_warnings",
                category="General Options",
                description="警告を非表示",
                type="bool",
                default_value=False,
            ),
            "simulate": YtDlpParameter(
                name="simulate",
                category="General Options",
                description="実際にはダウンロードしない",
                type="bool",
                default_value=False,
            ),
            "get_duration": YtDlpParameter(
                name="get_duration",
                category="General Options",
                description="動画の長さを取得",
                type="bool",
                default_value=False,
            ),
            "print": YtDlpParameter(
                name="print",
                category="General Options",
                description="メタデータを出力",
                type="string",
                default_value=None,
            ),
            "no_part": YtDlpParameter(
                name="no_part",
                category="Download Options",
                description="一時ファイルを使用しない",
                type="bool",
                default_value=False,
            ),
            "output": YtDlpParameter(
                name="output",
                category="Filesystem Options",
                description="出力ファイルテンプレート",
                type="string",
                default_value="%(title)s.%(ext)s",
            ),
            "restrict_filenames": YtDlpParameter(
                name="restrict_filenames",
                category="Filesystem Options",
                description="ファイル名を制限",
                type="bool",
                default_value=False,
            ),
            "verbose": YtDlpParameter(
                name="verbose",
                category="General Options",
                description="詳細ログ出力",
                type="bool",
                default_value=False,
            ),
            "quiet": YtDlpParameter(
                name="quiet",
                category="General Options",
                description="静かなモード",
                type="bool",
                default_value=False,
            ),
        }
    
    def _get_default_parameters(self) -> Dict[str, YtDlpParameter]:
        """デフォルトパラメータ定義"""
        return self._define_parameters()
    
    async def validate_parameters(self, parameters: Dict[str, any]) -> Dict[str, any]:
        """パラメータをバリデーション"""
        metadata = await self.generate_metadata()
        validated = {}
        
        for key, value in parameters.items():
            if key not in metadata:
                print(f"⚠️  Unknown parameter: {key}")
                continue
            
            param = metadata[key]
            
            # 型チェック
            try:
                if param.type == "bool":
                    validated[key] = bool(value)
                elif param.type == "int":
                    validated[key] = int(value)
                elif param.type == "string":
                    validated[key] = str(value)
                elif param.type == "choice":
                    if param.choices and value not in param.choices:
                        raise ValueError(f"Invalid choice: {value}")
                    validated[key] = str(value)
                else:
                    validated[key] = value
            
            except (ValueError, TypeError) as e:
                print(f"❌ Validation error for {key}: {e}")
        
        return validated
    
    async def apply_dependencies(self, parameters: Dict[str, any]) -> Dict[str, any]:
        """依存関係を適用して自動調整"""
        metadata = await self.generate_metadata()
        adjusted = dict(parameters)
        
        # extract_audio が有効な場合、format を bestaudio/best に設定
        if adjusted.get("extract_audio", False):
            if "format" not in adjusted or adjusted["format"] == "best":
                adjusted["format"] = "bestaudio/best"
        
        # simulate が有効な場合、extract-audio を無効化
        if adjusted.get("simulate", False):
            adjusted.pop("extract_audio", None)
        
        return adjusted
    
    async def export_as_json(self) -> str:
        """パラメータメタデータをJSON形式でエクスポート"""
        metadata = await self.generate_metadata()
        
        data = {
            param.name: {
                "category": param.category,
                "description": param.description,
                "type": param.type,
                "default": param.default_value,
                "required": param.required,
                "incompatible_with": param.incompatible_with,
                "depends_on": param.depends_on,
                "choices": param.choices,
                "ui_control": param.ui_control,
            }
            for param in metadata.values()
        }
        
        return json.dumps(data, ensure_ascii=False, indent=2)
