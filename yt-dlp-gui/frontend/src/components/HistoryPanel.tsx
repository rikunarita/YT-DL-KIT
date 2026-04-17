import { useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Download, Trash2 } from 'lucide-react'
import { historyAPI } from '../services/api'
import { RootState } from '../store/store'
import { setRecords, removeRecord } from '../store/slices/historySlice'

export default function HistoryPanel() {
  const { records, total } = useSelector((state: RootState) => state.history)
  const dispatch = useDispatch()
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const response = await historyAPI.getAll(50, 0)
      if (response.data.success) {
        dispatch(setRecords({
          records: response.data.records,
          total: response.data.total,
        }))
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
    return <div className="text-center py-4">読み込み中...</div>
  }

  if (records.length === 0) {
    return (
      <div className="text-center py-8 text-slate-500">
        <p>履歴がありません</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <p className="text-sm text-slate-600 dark:text-slate-400">
          全 {total} 件 (表示: {records.length} 件)
        </p>
        <button
          onClick={handleExport}
          className="btn btn-primary text-sm flex items-center gap-2"
        >
          <Download size={14} />
          CSVエクスポート
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="text-left py-2 px-3">URL</th>
              <th className="text-left py-2 px-3">ファイル名</th>
              <th className="text-left py-2 px-3">サイズ</th>
              <th className="text-left py-2 px-3">ステータス</th>
              <th className="text-left py-2 px-3">完了日時</th>
              <th className="text-center py-2 px-3">アクション</th>
            </tr>
          </thead>
          <tbody>
            {records.map((record) => (
              <tr key={record.id} className="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900">
                <td className="py-2 px-3 truncate text-xs">{record.url}</td>
                <td className="py-2 px-3 truncate text-xs">{record.output_filename || '---'}</td>
                <td className="py-2 px-3 text-xs">
                  {record.file_size ? (record.file_size / (1024 * 1024)).toFixed(2) + ' MB' : '---'}
                </td>
                <td className="py-2 px-3">
                  <span className={`px-2 py-1 text-xs rounded font-semibold ${
                    record.status === 'completed'
                      ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100'
                      : 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-100'
                  }`}>
                    {record.status}
                  </span>
                </td>
                <td className="py-2 px-3 text-xs">
                  {new Date(record.completed_at).toLocaleString()}
                </td>
                <td className="py-2 px-3 text-center">
                  <button
                    onClick={() => handleDelete(record.id)}
                    className="text-red-600 hover:text-red-800"
                  >
                    <Trash2 size={14} />
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
