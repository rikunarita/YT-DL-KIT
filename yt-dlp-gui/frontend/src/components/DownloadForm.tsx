import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { Play } from 'lucide-react'
import { downloadAPI } from '../services/api'
import { addTask, setError as setDownloadError } from '../store/slices/downloadSlice'

export default function DownloadForm() {
  const [url, setUrl] = useState('')
  const [format, setFormat] = useState('best')
  const [extractAudio, setExtractAudio] = useState(false)
  const [audioFormat, setAudioFormat] = useState('mp3')
  const [writeSubs, setWriteSubs] = useState(false)
  const [loading, setLoading] = useState(false)

  const dispatch = useDispatch()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!url.trim()) {
      dispatch(setDownloadError('URLを入力してください'))
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
        dispatch(addTask({
          id: response.data.task_id,
          url,
          status: 'pending',
          progress_percent: 0,
        }))
        
        // フォームクリア
        setUrl('')
        setFormat('best')
        setExtractAudio(false)
        setAudioFormat('mp3')
        setWriteSubs(false)
      }
    } catch (error) {
      dispatch(setDownloadError('ダウンロード開始に失敗しました'))
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
          URL
        </label>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://www.youtube.com/watch?v=..."
          className="input"
          disabled={loading}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            形式
          </label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="input"
            disabled={loading || extractAudio}
          >
            <option value="best">最高品質 (best)</option>
            <option value="bestvideo+bestaudio/best">最高ビデオ + オーディオ</option>
            <option value="best[height<=1080]">1080p以下</option>
            <option value="best[height<=720]">720p以下</option>
            <option value="best[height<=480]">480p以下 (モバイル)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            オーディオ抽出
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={extractAudio}
              onChange={(e) => setExtractAudio(e.target.checked)}
              className="mr-2"
              disabled={loading}
            />
            <span className="text-sm">有効</span>
          </label>
        </div>
      </div>

      {extractAudio && (
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              音声形式
            </label>
            <select
              value={audioFormat}
              onChange={(e) => setAudioFormat(e.target.value)}
              className="input"
              disabled={loading}
            >
              <option value="mp3">MP3</option>
              <option value="m4a">M4A</option>
              <option value="wav">WAV</option>
              <option value="opus">Opus</option>
              <option value="vorbis">Vorbis</option>
            </select>
          </div>
        </div>
      )}

      <div>
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={writeSubs}
            onChange={(e) => setWriteSubs(e.target.checked)}
            className="mr-2"
            disabled={loading}
          />
          <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
            字幕をダウンロード
          </span>
        </label>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        <Play size={18} />
        {loading ? 'ダウンロード開始中...' : 'ダウンロード開始'}
      </button>
    </form>
  )
}
