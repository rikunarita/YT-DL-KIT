import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { Play } from 'lucide-react'
import { downloadAPI } from '../services/api'
import { addTask, setError as setDownloadError } from '../store/slices/downloadSlice'
import { useTranslation } from '../i18n'

export default function DownloadForm() {
  const [url, setUrl] = useState('')
  const [format, setFormat] = useState('best')
  const [extractAudio, setExtractAudio] = useState(false)
  const [audioFormat, setAudioFormat] = useState('mp3')
  const [writeSubs, setWriteSubs] = useState(false)
  const [loading, setLoading] = useState(false)

  const dispatch = useDispatch()
  const { t } = useTranslation()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!url.trim()) {
      dispatch(setDownloadError(t('downloadForm.missingUrl')))
      return
    }

    setLoading(true)

    try {
      const parameters = {
        format,
        extract_audio: extractAudio,
        audio_format: audioFormat,
        write_subs: writeSubs,
      }

      const response = await downloadAPI.startDownload(url, parameters)

      if (response.data.success) {
        dispatch(
          addTask({
            id: response.data.task_id,
            url,
            status: 'pending',
            progress_percent: 0,
          }),
        )

        setUrl('')
        setFormat('best')
        setExtractAudio(false)
        setAudioFormat('mp3')
        setWriteSubs(false)
      }
    } catch (error) {
      dispatch(setDownloadError(t('downloadForm.downloadFailed')))
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
          {t('downloadForm.urlLabel')}
        </label>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder={t('downloadForm.urlPlaceholder')}
          className="input"
          disabled={loading}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            {t('downloadForm.formatLabel')}
          </label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="input"
            disabled={loading || extractAudio}
          >
            <option value="best">{t('downloadForm.formatBest')}</option>
            <option value="bestvideo+bestaudio/best">{t('downloadForm.formatBestVideoAudio')}</option>
            <option value="best[height<=1080]">{t('downloadForm.format1080')}</option>
            <option value="best[height<=720]">{t('downloadForm.format720')}</option>
            <option value="best[height<=480]">{t('downloadForm.format480')}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            {t('downloadForm.audioExtraction')}
          </label>
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={extractAudio}
              onChange={(e) => setExtractAudio(e.target.checked)}
              className="mr-2"
              disabled={loading}
            />
            <span className="text-sm">{t('common.enabled')}</span>
          </label>
        </div>
      </div>

      {extractAudio && (
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            {t('downloadForm.audioFormat')}
          </label>
          <select
            value={audioFormat}
            onChange={(e) => setAudioFormat(e.target.value)}
            className="input"
            disabled={loading}
          >
            <option value="mp3">{t('downloadForm.audioMp3')}</option>
            <option value="m4a">{t('downloadForm.audioM4a')}</option>
            <option value="wav">{t('downloadForm.audioWav')}</option>
            <option value="opus">{t('downloadForm.audioOpus')}</option>
            <option value="vorbis">{t('downloadForm.audioVorbis')}</option>
          </select>
        </div>
      )}

      <div>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={writeSubs}
            onChange={(e) => setWriteSubs(e.target.checked)}
            className="mr-2"
            disabled={loading}
          />
          <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
            {t('downloadForm.subtitles')}
          </span>
        </label>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        <Play size={18} />
        {loading ? t('downloadForm.startingDownload') : t('downloadForm.startDownload')}
      </button>
    </form>
  )
}
