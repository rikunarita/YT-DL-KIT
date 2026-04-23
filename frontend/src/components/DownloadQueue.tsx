import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Pause, Play, X } from 'lucide-react'
import { downloadAPI } from '../services/api'
import { RootState } from '../store/store'
import { removeTask, setTasks, updateTask } from '../store/slices/downloadSlice'
import { DownloadTask } from '../store/slices/downloadSlice'
import { useTranslation } from '../i18n'

export default function DownloadQueue() {
  const tasks = useSelector((state: RootState) => state.downloads.tasks)
  const dispatch = useDispatch()
  const { t } = useTranslation()

  useEffect(() => {
    const fetchQueue = async () => {
      try {
        const response = await downloadAPI.getQueue()
        if (response.data.success) {
          dispatch(setTasks(response.data.tasks as DownloadTask[]))
        }
      } catch (error) {
        console.error('Failed to fetch queue:', error)
      }
    }

    fetchQueue()
    const interval = setInterval(fetchQueue, 2000)

    return () => clearInterval(interval)
  }, [dispatch])

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
      <div className="text-center py-8 text-slate-500 dark:text-slate-400">
        <p>{t('downloadQueue.noTasks')}</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-4 rounded-3xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div>
          <p className="text-sm font-medium text-slate-900 dark:text-slate-100">{t('downloadQueue.activeTasks')}</p>
          <p className="text-xs text-slate-500 dark:text-slate-400">{tasks.length} {t('downloadQueue.tasksCount')}</p>
        </div>
        {tasks.some((task) => task.status === 'failed') && (
          <div className="inline-flex items-center gap-2 rounded-full bg-red-50 dark:bg-red-900/20 px-3 py-2 text-xs text-red-700 dark:text-red-200">
            {t('downloadQueue.failedTasks')}: {tasks.filter((task) => task.status === 'failed').length}
          </div>
        )}
      </div>
      {tasks.map((task) => {
        const statusText = t(`status.${task.status}`)

        return (
          <div key={task.id} className="bg-slate-100 dark:bg-slate-800 rounded-3xl p-4 shadow-sm">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between mb-3">
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm truncate text-slate-900 dark:text-slate-100">{task.url}</p>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  {task.current_filename || t('downloadQueue.downloading')}
                </p>
              </div>
              <span className={`inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full ${task.status === 'failed' ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-100' : 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100'}`}>
                {statusText}
              </span>
            </div>

            <div className="mb-3">
              <div className="h-2 bg-slate-300 dark:bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-600 transition-all duration-300"
                  style={{ width: `${task.progress_percent}%` }}
                />
              </div>
              <div className="mt-2 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between text-xs text-slate-500 dark:text-slate-400">
                <span>{task.progress_percent.toFixed(1)}%</span>
                <div className="flex flex-wrap gap-3">
                  <span>{task.speed || '---'}</span>
                  <span>{t('downloadQueue.eta')}: {task.eta || '---'}</span>
                </div>
              </div>
            </div>

            {task.error_message && (
              <div className="rounded-xl bg-red-50 dark:bg-red-900/20 p-3 text-sm text-red-700 dark:text-red-200 mb-3">
                {task.error_message}
              </div>
            )}

            <div className="flex flex-wrap gap-2 justify-end">
              {task.status === 'downloading' && (
                <button
                  onClick={() => handlePause(task.id!)}
                  className="btn btn-secondary text-sm"
                  title={t('downloadQueue.pause')}
                >
                  <Pause size={14} />
                </button>
              )}

              {task.status === 'paused' && (
                <button
                  onClick={() => handleResume(task.id!)}
                  className="btn btn-secondary text-sm"
                  title={t('downloadQueue.resume')}
                >
                  <Play size={14} />
                </button>
              )}

              {task.status !== 'completed' && (
                <button
                  onClick={() => handleCancel(task.id!)}
                  className="btn btn-danger text-sm"
                  title={t('downloadQueue.remove')}
                >
                  <X size={14} />
                </button>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
