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

type Page = 'download' | 'history' | 'scheduler' | 'settings'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('download')
  const [isHealthy, setIsHealthy] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const dispatch = useDispatch()

  // ヘルスチェック
  useEffect(() => {
    healthCheck()
      .then(() => {
        setIsHealthy(true)
        setErrorMsg(null)
      })
      .catch((err) => {
        setIsHealthy(false)
        setErrorMsg('バックエンドに接続できません。サーバーが起動しているか確認してください。')
        console.error('Health check failed:', err)
      })
  }, [])

  const navigationItems = [
    {
      label: 'ダウンロード',
      icon: Download,
      page: 'download' as Page,
    },
    {
      label: '履歴',
      icon: History,
      page: 'history' as Page,
    },
    {
      label: 'スケジューラー',
      icon: Calendar,
      page: 'scheduler' as Page,
    },
    {
      label: '設定',
      icon: Settings,
      page: 'settings' as Page,
    },
  ]

  return (
    <div className="flex h-screen bg-slate-50 dark:bg-slate-950">
      <Sidebar 
        items={navigationItems} 
        currentPage={currentPage}
        onPageChange={setCurrentPage}
      />
      
      <main className="flex-1 overflow-auto">
        <div className="container mx-auto p-6">
          {!isHealthy && (
            <div className="mb-6 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 rounded-lg text-red-800 dark:text-red-100">
              <p className="font-semibold">⚠️ エラー</p>
              <p>{errorMsg}</p>
            </div>
          )}

          {isHealthy && (
            <>
              {currentPage === 'download' && (
                <div className="space-y-6">
                  <div className="card p-6">
                    <h1 className="text-3xl font-bold mb-4">yt-dlp GUI</h1>
                    <DownloadForm />
                  </div>
                  <div className="card p-6">
                    <h2 className="text-2xl font-bold mb-4">ダウンロード待機中 / 実行中</h2>
                    <DownloadQueue />
                  </div>
                </div>
              )}

              {currentPage === 'history' && (
                <div className="card p-6">
                  <h1 className="text-3xl font-bold mb-4">ダウンロード履歴</h1>
                  <HistoryPanel />
                </div>
              )}

              {currentPage === 'scheduler' && (
                <div className="card p-6">
                  <h1 className="text-3xl font-bold mb-4">スケジューラー</h1>
                  <SchedulerPanel />
                </div>
              )}

              {currentPage === 'settings' && (
                <div className="card p-6">
                  <h1 className="text-3xl font-bold mb-4">設定</h1>
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
