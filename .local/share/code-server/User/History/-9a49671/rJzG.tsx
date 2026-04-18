import { useEffect, useState } from 'react'
import { Clock, Plus, Trash2 } from 'lucide-react'
import { schedulerAPI, profileAPI } from '../services/api'
import { useTranslation } from '../i18n'

interface Schedule {
  id?: number
  name: string
  cron_expression: string
  urls: string[]
  profile_id: number
  is_enabled: boolean
}

interface Profile {
  id: number
  name: string
}

export default function SchedulerPanel() {
  const [schedules, setSchedules] = useState<Schedule[]>([])
  const [profiles, setProfiles] = useState<Profile[]>([])
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)

  const [formData, setFormData] = useState<Schedule>({
    name: '',
    cron_expression: '0 22 * * *',
    urls: [''],
    profile_id: 0,
    is_enabled: true,
  })

  const { t } = useTranslation()

  useEffect(() => {
    fetchSchedules()
    fetchProfiles()
  }, [])

  const fetchSchedules = async () => {
    try {
      const response = await schedulerAPI.getTasks()
      if (response.data.success) {
        setSchedules(response.data.tasks)
      }
    } catch (error) {
      console.error('Failed to fetch schedules:', error)
    }
  }

  const fetchProfiles = async () => {
    try {
      const response = await profileAPI.getAll()
      if (response.data.success) {
        setProfiles(response.data.profiles)
      }
    } catch (error) {
      console.error('Failed to fetch profiles:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await schedulerAPI.create(formData)
      fetchSchedules()
      setFormData({
        name: '',
        cron_expression: '0 22 * * *',
        urls: [''],
        profile_id: 0,
        is_enabled: true,
      })
      setShowForm(false)
    } catch (error) {
      console.error('Failed to create schedule:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (scheduleId: number) => {
    try {
      await schedulerAPI.delete(scheduleId)
      fetchSchedules()
    } catch (error) {
      console.error('Failed to delete schedule:', error)
    }
  }

  const addUrlField = () => {
    setFormData({
      ...formData,
      urls: [...formData.urls, ''],
    })
  }

  const removeUrlField = (index: number) => {
    setFormData({
      ...formData,
      urls: formData.urls.filter((_, i) => i !== index),
    })
  }

  const updateUrl = (index: number, value: string) => {
    const newUrls = [...formData.urls]
    newUrls[index] = value
    setFormData({
      ...formData,
      urls: newUrls,
    })
  }

  return (
    <div className="space-y-6">
      <button
        onClick={() => setShowForm(!showForm)}
        className="btn-primary flex items-center gap-2"
      >
        <Plus size={18} />
        {t('schedulerPanel.newSchedule')}
      </button>

      {showForm && (
        <form onSubmit={handleSubmit} className="card p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">{t('schedulerPanel.scheduleName')}</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="input"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">{t('schedulerPanel.cronExpression')}</label>
            <input
              type="text"
              value={formData.cron_expression}
              onChange={(e) => setFormData({ ...formData, cron_expression: e.target.value })}
              placeholder={t('schedulerPanel.cronPlaceholder')}
              className="input text-xs"
              required
            />
            <p className="text-xs text-slate-500 mt-1">
              {t('schedulerPanel.cronExample')}
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">{t('schedulerPanel.profile')}</label>
            <select
              value={formData.profile_id}
              onChange={(e) => setFormData({ ...formData, profile_id: parseInt(e.target.value) })}
              className="input"
              required
            >
              <option value={0}>{t('schedulerPanel.profileSelect')}</option>
              {profiles.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">{t('schedulerPanel.urls')}</label>
            <div className="space-y-2">
              {formData.urls.map((url, index) => (
                <div key={index} className="flex gap-2">
                  <input
                    type="text"
                    value={url}
                    onChange={(e) => updateUrl(index, e.target.value)}
                    placeholder={t('schedulerPanel.urlPlaceholder')}
                    className="input flex-1"
                    required
                  />
                  {formData.urls.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeUrlField(index)}
                      className="btn btn-danger"
                      aria-label={t('schedulerPanel.removeUrl')}
                    >
                      <Trash2 size={14} />
                    </button>
                  )}
                </div>
              ))}
            </div>
            <button
              type="button"
              onClick={addUrlField}
              className="btn btn-secondary text-sm mt-2"
            >
              + {t('schedulerPanel.addUrl')}
            </button>
          </div>

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={formData.is_enabled}
              onChange={(e) => setFormData({ ...formData, is_enabled: e.target.checked })}
              className="mr-2"
            />
            <span className="text-sm">{t('common.enabled')}</span>
          </label>

          <div className="flex gap-2 flex-wrap">
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? t('common.creating') : t('common.create')}
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="btn btn-secondary"
            >
              {t('common.cancel')}
            </button>
          </div>
        </form>
      )}

      <div className="space-y-2">
        {schedules.length === 0 ? (
          <p className="text-slate-500 text-center py-4">{t('schedulerPanel.noSchedules')}</p>
        ) : (
          schedules.map((schedule) => (
            <div key={schedule.id} className="card p-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  <Clock size={16} className="text-blue-600" />
                  <h3 className="font-medium">{schedule.name}</h3>
                  <span className={`px-2 py-1 text-xs rounded ${
                    schedule.is_enabled
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                      : 'bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-300'
                  }`}>
                    {schedule.is_enabled ? t('common.enabled') : t('common.disabled')}
                  </span>
                </div>
                <p className="text-sm text-slate-500 dark:text-slate-400">{t('schedulerPanel.cronLabel')}: {schedule.cron_expression}</p>
                <p className="text-sm text-slate-500 dark:text-slate-400">{schedule.urls.length} {t('schedulerPanel.urlCount')}</p>
              </div>
              <button
                onClick={() => handleDelete(schedule.id!)}
                className="text-red-600 hover:text-red-800"
                aria-label={t('schedulerPanel.delete')}
              >
                <Trash2 size={18} />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
