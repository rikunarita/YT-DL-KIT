import { useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Pause, Play, X } from 'lucide-react'
import { downloadAPI } from '../services/api'
import { RootState } from '../store/store'
import { removeTask, updateTask } from '../store/slices/downloadSlice'

export default function DownloadQueue() {
  const tasks = useSelector((state: RootState) => state.downloads.tasks)
  const dispatch = useDispatch()

  useEffect(() => {
    // 定期的にキューを更新
    const interval = setInterval(async () => {
      try {
        const response = await downloadAPI.getQueue()
        if (response.data.success) {
          // ここでタスクを更新
        }
      } catch (error) {
        console.error('Failed to fetch queue:', error)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  const handlePause = async (taskId: number) => {
    try {
      await downloadAPI.pause(taskId)
      const status = await downloadAPI.getStatus(taskId)
      if (status.data.success) {
        dispatch(updateTask(status.data.task))
      }
    } catch (error) {
      console.error('Failed to pause download:', error)
    }
  }

  const handleResume = async (taskId: number) => {
    try {
      await downloadAPI.resume(taskId)
      const status = await downloadAPI.getStatus(taskId)
      if (status.data.success) {
        dispatch(updateTask(status.data.task))
      }
    } catch (error) {
      console.error('Failed to resume download:', error)
    }
  }

  const handleCancel = async (taskId: number) => {
    try {
      await downloadAPI.cancel(taskId)
      dispatch(removeTask(taskId))
    } catch (error) {
      console.error('Failed to cancel download:', error)
    }
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8 text-slate-500">
        <p>ダウンロードタスクはありません</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <div key={task.id} className="bg-slate-100 dark:bg-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex-1">
              <p className="font-medium text-sm truncate">{task.url}</p>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                {task.current_filename || 'ダウンロード中...'}
              </p>
            </div>
            <span className="px-3 py-1 text-xs font-semibold bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100 rounded-full">
              {task.status}
            </span>
          </div>

          {/* プログレスバー */}
          <div className="mb-2">
            <div className="h-2 bg-slate-300 dark:bg-slate-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-600 transition-all duration-300"
                style={{ width: `${task.progress_percent}%` }}
              />
            </div>
            <div className="flex justify-between items-center text-xs text-slate-500 dark:text-slate-400 mt-1">
              <span>{task.progress_percent.toFixed(1)}%</span>
              <div className="flex gap-2">
                <span>{task.speed || '---'}</span>
                <span>ETA: {task.eta || '---'}</span>
              </div>
            </div>
          </div>

          {/* エラーメッセージ */}
          {task.error_message && (
            <div className="text-xs text-red-600 dark:text-red-400 mb-2">
              {task.error_message}
            </div>
          )}

          {/* アクションボタン */}
          <div className="flex gap-2 justify-end">
            {task.status === 'downloading' && (
              <button
                onClick={() => handlePause(task.id!)}
                className="btn btn-secondary text-sm"
              >
                <Pause size={14} />
              </button>
            )}

            {task.status === 'paused' && (
              <button
                onClick={() => handleResume(task.id!)}
                className="btn btn-secondary text-sm"
              >
                <Play size={14} />
              </button>
            )}

            {task.status !== 'completed' && (
              <button
                onClick={() => handleCancel(task.id!)}
                className="btn btn-danger text-sm"
              >
                <X size={14} />
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
