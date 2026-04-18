import { useEffect, useState } from 'react'
import { useDispatch } from 'react-redux'
import { Download, History, Settings, Calendar } from 'lucide-react'
import Sidebar from './components/Sidebar'
import DownloadForm from './components/DownloadForm'
import DownloadQueue from './components/DownloadQueue'
import HistoryPanel from './components/HistoryPanel'
import SchedulerPanel from './components/SchedulerPanel'
import SettingsPanel from './components/SettingsPanel'
import { healthCheck } from './services/api'
import { useTranslation } from './i18n'

type Page = 'download' | 'history' | 'scheduler' | 'settings'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('download')
  const [isHealthy, setIsHealthy] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const dispatch = useDispatch()
  const { t, language, setLanguage } = useTranslation()

  useEffect(() => {
    healthCheck()
      .then(() => {
        setIsHealthy(true)
        setErrorMsg(null)
      })
      .catch((err) => {
        setIsHealthy(false)
        setErrorMsg(t('app.errorBackend'))
        console.error('Health check failed:', err)
      })
  }, [t])

  const navigationItems = [
    {
      label: t('nav.download'),
      icon: Download,
      page: 'download' as Page,
    },
    {
      label: t('nav.history'),
      icon: History,
      page: 'history' as Page,
    },
    {
      label: t('nav.scheduler'),
      icon: Calendar,
      page: 'scheduler' as Page,
    },
    {
      label: t('nav.settings'),
      icon: Settings,
      page: 'settings' as Page,
    },
  ]

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 dark:bg-slate-950">
      <Sidebar
        items={navigationItems}
        currentPage={currentPage}
        onPageChange={setCurrentPage}
      />

      <main className="flex-1 overflow-auto">
        <div className="sticky top-0 z-20 border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-950/95 backdrop-blur-sm">
          <div className="container mx-auto px-6 py-5 flex flex-col md:flex-row justify-between gap-4 items-start">
            <div className="space-y-2">
              <p className="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">
                {t('app.subTitle')}
              </p>
              <h1 className="text-3xl font-semibold text-slate-900 dark:text-slate-100">
                {t('app.title')}
              </h1>
              <p className="text-sm text-slate-600 dark:text-slate-300 max-w-2xl">
                {t('app.description')}
              </p>
            </div>

            <div className="flex items-center gap-3">
              <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-900 px-3 py-2 text-sm text-slate-700 dark:text-slate-200">
                <label className="block text-[10px] uppercase tracking-[0.4em] mb-1 text-slate-500 dark:text-slate-400">
                  {t('app.languageLabel')}
                </label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value as any)}
                  className="input bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100"
                >
                  <option value="en">English</option>
                  <option value="ja">日本語</option>
                  <option value="zh">中文</option>
                </select>
              </div>
              <div className="text-right text-xs text-slate-500 dark:text-slate-400">
                {t('app.version', { version: '1.0.0' })}
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-6 py-6 space-y-6">
          {!isHealthy && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-800 dark:border-red-700 dark:bg-red-950/70 dark:text-red-200">
              <p className="font-semibold">⚠️ {t('common.error')}</p>
              <p>{errorMsg}</p>
            </div>
          )}

          {isHealthy && (
            <>
              {currentPage === 'download' && (
                <div className="space-y-6">
                  <div className="card p-6">
                    <h2 className="text-2xl font-semibold mb-4">{t('nav.download')}</h2>
                    <DownloadForm />
                  </div>
                  <div className="card p-6">
                    <h2 className="text-2xl font-semibold mb-4">{t('downloadQueue.title')}</h2>
                    <DownloadQueue />
                  </div>
                </div>
              )}

              {currentPage === 'history' && (
                <div className="card p-6">
                  <h2 className="text-2xl font-semibold mb-4">{t('history.title')}</h2>
                  <HistoryPanel />
                </div>
              )}

              {currentPage === 'scheduler' && (
                <div className="card p-6">
                  <h2 className="text-2xl font-semibold mb-4">{t('scheduler.title')}</h2>
                  <SchedulerPanel />
                </div>
              )}

              {currentPage === 'settings' && (
                <div className="card p-6">
                  <h2 className="text-2xl font-semibold mb-4">{t('nav.settings')}</h2>
                  <SettingsPanel />
                </div>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
