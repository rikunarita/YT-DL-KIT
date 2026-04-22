import { useState, useEffect } from 'react'
import { Copy, Download } from 'lucide-react'
import { useTranslation } from '../i18n'

interface RawOptionsProps {
  value?: string
  onChange?: (value: string) => void
}

export default function RawOptions({ value = '', onChange }: RawOptionsProps) {
  const [rawOptions, setRawOptions] = useState(value)
  const [copied, setCopied] = useState(false)
  const { t } = useTranslation()

  useEffect(() => {
    setRawOptions(value)
  }, [value])

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

  const handleChange = (value: string) => {
    setRawOptions(value)
    if (onChange) {
      onChange(value)
    }
  }

  return (
    <div className="space-y-4">
      <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg">
        <h3 className="font-bold text-yellow-900 dark:text-yellow-100 mb-2">⚠️ {t('rawOptions.title')}</h3>
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          {t('rawOptions.description')}
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">{t('rawOptions.label')}</label>
        <textarea
          value={rawOptions}
          onChange={(e) => handleChange(e.target.value)}
          placeholder={t('rawOptions.placeholder')}
          className="w-full h-64 p-3 border border-slate-300 dark:border-slate-600 rounded font-mono text-sm"
          spellCheck="false"
        />
        <p className="text-xs text-slate-500 mt-2">
          {t('rawOptions.helpText')}
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <button
          onClick={copyToClipboard}
          className="btn btn-secondary flex items-center justify-center gap-2"
        >
          <Copy size={18} />
          {copied ? t('rawOptions.copied') : t('rawOptions.copy')}
        </button>
        <button
          onClick={downloadOptions}
          className="btn btn-secondary flex items-center justify-center gap-2"
        >
          <Download size={18} />
          {t('rawOptions.download')}
        </button>
      </div>

      <div className="p-4 bg-slate-50 dark:bg-slate-800 rounded border border-slate-200 dark:border-slate-700">
        <h4 className="font-bold text-sm mb-3">{t('rawOptions.commonOptionsTitle')}</h4>
        <div className="space-y-2">
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">{t('rawOptions.commonOptions.highQuality')}</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --format bestvideo+bestaudio/best
            </code>
          </div>
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">{t('rawOptions.commonOptions.extractAudio')}</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --extract-audio --audio-format mp3 --audio-quality 192
            </code>
          </div>
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">{t('rawOptions.commonOptions.subtitles')}</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --write-subs --sub-langs en,ja --sub-format vtt
            </code>
          </div>
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">{t('rawOptions.commonOptions.playlist')}</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --yes-playlist --playlist-items 1-10
            </code>
          </div>
          <div>
            <p className="text-xs font-medium text-slate-600 dark:text-slate-400">{t('rawOptions.commonOptions.outputTemplate')}</p>
            <code className="text-xs bg-slate-200 dark:bg-slate-900 p-1 rounded block break-all">
              --output "%(uploader)s/%(playlist)s/%(title)s.%(ext)s"
            </code>
          </div>
        </div>
      </div>

      <div className="text-xs text-slate-600 dark:text-slate-400 space-y-1">
        <p>{t('rawOptions.referencesTitle')}</p>
        <ul className="list-disc list-inside space-y-1">
          <li>
            <a
              href="https://github.com/yt-dlp/yt-dlp#usage-and-options"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              {t('rawOptions.referenceUsage')}
            </a>
          </li>
          <li>
            <a
              href="https://github.com/yt-dlp/yt-dlp#output-template"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              {t('rawOptions.referenceOutputTemplate')}
            </a>
          </li>
        </ul>
      </div>
    </div>
  )
}
