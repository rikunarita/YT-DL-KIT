import { useEffect, useState } from 'react'
import { Download, Save } from 'lucide-react'
import { settingsAPI } from '../services/api'
import { useTranslation } from '../i18n'

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
  const { t } = useTranslation()

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
      alert(t('settingsPanel.saved'))
    } catch (error) {
      console.error('Failed to save settings:', error)
      alert(t('settingsPanel.saveFailed'))
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
    return <div className="text-center py-4">{t('common.loading')}</div>
  }

  if (!settings) {
    return <div className="text-center py-4 text-red-600">{t('settingsPanel.loadFailed')}</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold mb-4">{t('settingsPanel.generalSettings')}</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">{t('settingsPanel.defaultOutputFolder')}</label>
            <input
              type="text"
              value={settings.default_output_directory}
              onChange={(e) => setSettings({ ...settings, default_output_directory: e.target.value })}
              className="input"
            />
            <p className="text-xs text-slate-500 mt-1">{t('settingsPanel.outputFolderDescription')}</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">{t('settingsPanel.maxConcurrentDownloads')}</label>
            <input
              type="number"
              min="1"
              max="10"
              value={settings.max_concurrent_downloads}
              onChange={(e) => setSettings({ ...settings, max_concurrent_downloads: parseInt(e.target.value) })}
              className="input"
            />
          </div>

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={settings.auto_update_yt_dlp}
              onChange={(e) => setSettings({ ...settings, auto_update_yt_dlp: e.target.checked })}
              className="mr-2"
            />
            <span className="text-sm">{t('settingsPanel.autoUpdateYtDlp')}</span>
          </label>
        </div>
      </div>

      <div className="border-t border-slate-200 dark:border-slate-700 pt-6">
        <h2 className="text-xl font-bold mb-4">{t('settingsPanel.networkSettings')}</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">{t('settingsPanel.proxyUrl')}</label>
            <input
              type="text"
              value={settings.default_proxy || ''}
              onChange={(e) => setSettings({ ...settings, default_proxy: e.target.value })}
              placeholder={t('settingsPanel.proxyPlaceholder')}
              className="input"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">{t('settingsPanel.proxyUsername')}</label>
              <input
                type="text"
                value={settings.proxy_username || ''}
                onChange={(e) => setSettings({ ...settings, proxy_username: e.target.value })}
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">{t('settingsPanel.proxyPassword')}</label>
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
        <h2 className="text-xl font-bold mb-4">{t('settingsPanel.pathSettings')}</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">{t('settingsPanel.ffmpegPath')}</label>
            <input
              type="text"
              value={settings.ffmpeg_path || ''}
              onChange={(e) => setSettings({ ...settings, ffmpeg_path: e.target.value })}
              placeholder={t('settingsPanel.autoDetect')}
              className="input text-xs"
            />
            <p className="text-xs text-slate-500 mt-1">{t('settingsPanel.autoDetectMessage')}</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">{t('settingsPanel.ytDlpPath')}</label>
            <input
              type="text"
              value={settings.yt_dlp_path || ''}
              onChange={(e) => setSettings({ ...settings, yt_dlp_path: e.target.value })}
              placeholder={t('settingsPanel.autoDownload')}
              className="input text-xs"
              disabled
            />
            <p className="text-xs text-slate-500 mt-1">{t('settingsPanel.dynamicDownload')}</p>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-200 dark:border-slate-700 pt-6">
        <h2 className="text-xl font-bold mb-4">{t('settingsPanel.uiSettings')}</h2>
        <div>
          <label className="block text-sm font-medium mb-2">{t('settingsPanel.theme')}</label>
          <select
            value={settings.theme}
            onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
            className="input"
          >
            <option value="light">{t('settingsPanel.themeLight')}</option>
            <option value="dark">{t('settingsPanel.themeDark')}</option>
          </select>
        </div>
      </div>

      <div className="border-t border-slate-200 dark:border-slate-700 pt-6 space-y-3">
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={handleSave}
            disabled={saving}
            className="btn-primary flex items-center gap-2 flex-1"
          >
            <Save size={18} />
            {saving ? t('settingsPanel.saving') : t('settingsPanel.save')}
          </button>

          <button
            onClick={handleExport}
            className="btn btn-secondary flex items-center gap-2"
          >
            <Download size={18} />
            {t('settingsPanel.export')}
          </button>
        </div>
      </div>
    </div>
  )
}
