import { useEffect, useState } from 'react'
import { Download, Save } from 'lucide-react'
import { settingsAPI } from '../services/api'

interface GlobalSettings {
  id?: number
  default_output_directory: string
  max_concurrent_downloads: number
  default_proxy?: string
  proxy_username?: string
  proxy_password?: string
  ffmpeg_path?: string
  yt_dlp_path?: string
  theme: string
  auto_update_yt_dlp: boolean
}

export default function SettingsPanel() {
  const [settings, setSettings] = useState<GlobalSettings | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const response = await settingsAPI.get()
      if (response.data.success) {
        setSettings(response.data.settings)
      }
    } catch (error) {
      console.error('Failed to fetch settings:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!settings) return

    setSaving(true)
    try {
      await settingsAPI.update(settings)
      alert('設定が保存されました')
    } catch (error) {
      console.error('Failed to save settings:', error)
      alert('設定の保存に失敗しました')
    } finally {
      setSaving(false)
    }
  }

  const handleExport = async () => {
    try {
      const response = await settingsAPI.exportConfig()
      const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `yt-dlp-config-${new Date().toISOString().split('T')[0]}.json`
      link.click()
    } catch (error) {
      console.error('Failed to export config:', error)
    }
  }

  if (loading) {
    return <div className="text-center py-4">読み込み中...</div>
  }

  if (!settings) {
    return <div className="text-center py-4 text-red-600">設定の読み込みに失敗しました</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold mb-4">一般設定</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">デフォルト出力フォルダ</label>
            <input
              type="text"
              value={settings.default_output_directory}
              onChange={(e) => setSettings({ ...settings, default_output_directory: e.target.value })}
              className="input"
            />
            <p className="text-xs text-slate-500 mt-1">ダウンロードファイルの保存先</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">最大並列ダウンロード数</label>
            <input
              type="number"
              min="1"
              max="10"
              value={settings.max_concurrent_downloads}
              onChange={(e) => setSettings({ ...settings, max_concurrent_downloads: parseInt(e.target.value) })}
              className="input"
            />
          </div>

          <label className="flex items-center">
            <input
              type="checkbox"
              checked={settings.auto_update_yt_dlp}
              onChange={(e) => setSettings({ ...settings, auto_update_yt_dlp: e.target.checked })}
              className="mr-2"
            />
            <span className="text-sm">起動時にyt-dlpを自動更新</span>
          </label>
        </div>
      </div>

      <div className="border-t border-slate-200 dark:border-slate-700 pt-6">
        <h2 className="text-xl font-bold mb-4">ネットワーク設定</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">プロキシURL</label>
            <input
              type="text"
              value={settings.default_proxy || ''}
              onChange={(e) => setSettings({ ...settings, default_proxy: e.target.value })}
              placeholder="http://proxy.example.com:8080"
              className="input"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">プロキシユーザー</label>
              <input
                type="text"
                value={settings.proxy_username || ''}
                onChange={(e) => setSettings({ ...settings, proxy_username: e.target.value })}
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">プロキシパスワード</label>
              <input
                type="password"
                value={settings.proxy_password || ''}
                onChange={(e) => setSettings({ ...settings, proxy_password: e.target.value })}
                className="input"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-200 dark:border-slate-700 pt-6">
        <h2 className="text-xl font-bold mb-4">パス設定</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">FFmpeg パス</label>
            <input
              type="text"
              value={settings.ffmpeg_path || ''}
              onChange={(e) => setSettings({ ...settings, ffmpeg_path: e.target.value })}
              placeholder="自動検出"
              className="input text-xs"
            />
            <p className="text-xs text-slate-500 mt-1">空欄で自動検出</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">yt-dlp パス</label>
            <input
              type="text"
              value={settings.yt_dlp_path || ''}
              onChange={(e) => setSettings({ ...settings, yt_dlp_path: e.target.value })}
              placeholder="自動ダウンロード"
              className="input text-xs"
              disabled
            />
            <p className="text-xs text-slate-500 mt-1">動的ダウンロード - 自動管理</p>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-200 dark:border-slate-700 pt-6">
        <h2 className="text-xl font-bold mb-4">UI設定</h2>
        <div>
          <label className="block text-sm font-medium mb-2">テーマ</label>
          <select
            value={settings.theme}
            onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
            className="input"
          >
            <option value="light">ライト</option>
            <option value="dark">ダーク</option>
          </select>
        </div>
      </div>

      <div className="border-t border-slate-200 dark:border-slate-700 pt-6 space-y-3">
        <div className="flex gap-2">
          <button
            onClick={handleSave}
            disabled={saving}
            className="btn-primary flex items-center gap-2 flex-1"
          >
            <Save size={18} />
            {saving ? '保存中...' : '保存'}
          </button>

          <button
            onClick={handleExport}
            className="btn btn-secondary flex items-center gap-2"
          >
            <Download size={18} />
            エクスポート
          </button>
        </div>
      </div>
    </div>
  )
}
