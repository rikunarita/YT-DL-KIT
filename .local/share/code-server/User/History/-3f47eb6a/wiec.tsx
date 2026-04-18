import { useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Download, Trash2 } from 'lucide-react'
import { historyAPI } from '../services/api'
import { RootState } from '../store/store'
import { setRecords, removeRecord } from '../store/slices/historySlice'
import { useTranslation } from '../i18n'

export default function HistoryPanel() {
  const { records, total } = useSelector((state: RootState) => state.history)
  const dispatch = useDispatch()
  const [loading, setLoading] = useState(false)
  const { t } = useTranslation()

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const response = await historyAPI.getAll(50, 0)
      if (response.data.success) {
        dispatch(
          setRecords({
            records: response.data.records,
            total: response.data.total,
          }),
        )
      }
    } catch (error) {
      console.error('Failed to fetch history:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (historyId: number) => {
    try {
      await historyAPI.delete(historyId)
      dispatch(removeRecord(historyId))
    } catch (error) {
      console.error('Failed to delete history:', error)
    }
  }

  const handleExport = async () => {
    try {
      const response = await historyAPI.export()
      const blob = new Blob([response.data.csv_data], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `yt-dlp-history-${new Date().toISOString().split('T')[0]}.csv`
      link.click()
    } catch (error) {
      console.error('Failed to export history:', error)
    }
  }

  if (loading) {
    return <div className="text-center py-4">{t('common.loading')}</div>
  }

  if (records.length === 0) {
    return (
      <div className="text-center py-8 text-slate-500 dark:text-slate-400">
        <p>{t('historyPanel.noHistory')}</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-slate-600 dark:text-slate-400">
          {t('historyPanel.totalCount', { count: total })} ({t('historyPanel.displaying', { count: records.length })})
        </p>
        <button
          onClick={handleExport}
          className="btn btn-primary text-sm flex items-center gap-2"
        >
          <Download size={14} />
          {t('historyPanel.exportCsv')}
        </button>
      </div>

      <div className="overflow-x-auto rounded-3xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/70 shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-950">
            <tr>
              <th className="text-left py-3 px-4">{t('historyPanel.url')}</th>
              <th className="text-left py-3 px-4">{t('historyPanel.filename')}</th>
              <th className="text-left py-3 px-4">{t('historyPanel.size')}</th>
              <th className="text-left py-3 px-4">{t('historyPanel.status')}</th>
              <th className="text-left py-3 px-4">{t('historyPanel.completedAt')}</th>
              <th className="text-center py-3 px-4">{t('historyPanel.actions')}</th>
            </tr>
          </thead>
          <tbody>
            {records.map((record) => (
              <tr key={record.id} className="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900">
                <td className="py-3 px-4 truncate text-xs">{record.url}</td>
                <td className="py-3 px-4 truncate text-xs">{record.output_filename || '---'}</td>
                <td className="py-3 px-4 text-xs">
                  {record.file_size ? `${(record.file_size / (1024 * 1024)).toFixed(2)} MB` : '---'}
                </td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 text-xs rounded font-semibold ${
                    record.status === 'completed'
                      ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100'
                      : 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-100'
                  }`}>
                    {t(`status.${record.status}`)}
                  </span>
                </td>
                <td className="py-3 px-4 text-xs">
                  {new Date(record.completed_at).toLocaleString()}
                </td>
                <td className="py-3 px-4 text-center">
                  <button
                    onClick={() => handleDelete(record.id)}
                    className="text-red-600 hover:text-red-800"
                    aria-label={t('historyPanel.delete')}
                  >
                    <Trash2 size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
