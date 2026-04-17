import { useState } from 'react'
import { Copy, Download } from 'lucide-react'

export default function RawOptions() {
  const [rawOptions, setRawOptions] = useState('')
  const [copied, setCopied] = useState(false)

  const copyToClipboard = () => {
    navigator.clipboard.writeText(rawOptions)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadOptions = () => {
    const blob = new Blob([rawOptions], { type: 'text/plain' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `yt-dlp-options-${new Date().toISOString().split('T')[0]}.txt`
    link.click()
  }

  return (
    <div className="space-y-4">
      <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg">
        <h3 className="font-bold text-yellow-900 dark:text-yellow-100 mb-2">⚠️ 生のyt-dlpオプション</h3>
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          ここで入力したオプションは、yt-dlp に直接渡されます。完全な制御が可能ですが、
          構文エラーがあるとダウンロードが失敗する可能性があります。
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">yt-dlp CLI オプション</label>
        <textarea
          value={rawOptions}
          onChange={(e) => setRawOptions(e.target.value)}
          placeholder={`例:
--format best
--extract-audio --audio-format mp3
--write-subs --sub-langs en,ja
--output "/home/user/Downloads/%(title)s.%(ext)s"`}
          className="w-full h-64 p-3 border border-slate-300 dark:border-slate-600 rounded font-mono text-sm"
          spellCheck="false"
        />
        <p className="text-xs text-slate-500 mt-2">
          💡 各行が 1 つのオプションになります。yt-dlp --help で全オプション確認可能
        </p>
      </div>

      <div className="grid grid-cols-2 gap-2">
        <button
          onClick={copyToClipboard}
          className="btn btn-secondary flex items-center justify-center gap-2"
        >
          <Copy size={18} />
          {copied ? 'コピー完了' : 'コピー'}
        </button>
        <button
          onClick={downloadOptions}
          className="btn btn-secondary flex items-center justify-center gap-2"
        >
          <Download size={18} />
          ダウンロード
        </button>
      </div>

      <div className="p-4 bg-slate-50 dark:bg-slate-800 rounded border border-slate-200 dark:border-slate-700">
        <h4 className="font-bold text-sm mb-3">よく使うオプション</h4>
        <div className="space-y-2">
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">高品質ダウンロード:</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --format bestvideo+bestaudio/best
            </code>
          </div>
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">音声抽出 (MP3):</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --extract-audio --audio-format mp3 --audio-quality 192
            </code>
          </div>
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">字幕付きダウンロード:</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --write-subs --sub-langs en,ja --sub-format vtt
            </code>
          </div>
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">プレイリスト処理:</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --yes-playlist --playlist-items 1-10
            </code>
          </div>
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">出力ファイル名カスタマイズ:</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --output "%(uploader)s/%(playlist)s/%(title)s.%(ext)s"
            </code>
          </div>
        </div>
      </div>

      <div className="text-xs text-slate-600 dark:text-slate-400 space-y-1">
        <p>📚 参考リンク:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>
            <a
              href="https://github.com/yt-dlp/yt-dlp#usage-and-options"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              yt-dlp オプション完全リスト
            </a>
          </li>
          <li>
            <a
              href="https://github.com/yt-dlp/yt-dlp#output-template"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              出力テンプレート構文
            </a>
          </li>
        </ul>
      </div>
    </div>
  )
}
