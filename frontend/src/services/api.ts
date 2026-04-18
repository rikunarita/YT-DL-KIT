import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Downloads API
export const downloadAPI = {
  startDownload: (url: string, parameters: Record<string, any>, outputPath?: string) =>
    api.post('/downloads/start', {
      url,
      parameters,
      output_path: outputPath,
    }),

  getQueue: () => api.get('/downloads/queue'),

  getStatus: (taskId: number) => api.get(`/downloads/${taskId}/status`),

  pause: (taskId: number) => api.post(`/downloads/${taskId}/pause`),

  resume: (taskId: number) => api.post(`/downloads/${taskId}/resume`),

  cancel: (taskId: number) => api.delete(`/downloads/${taskId}`),
}

// Profiles API
export const profileAPI = {
  getAll: () => api.get('/profiles'),

  create: (profile: { name: string; description?: string; parameters: Record<string, any> }) =>
    api.post('/profiles', profile),

  update: (profileId: number, profile: { name: string; description?: string; parameters: Record<string, any> }) =>
    api.put(`/profiles/${profileId}`, profile),

  delete: (profileId: number) => api.delete(`/profiles/${profileId}`),

  duplicate: (profileId: number, newName: string) =>
    api.post(`/profiles/${profileId}/duplicate?new_name=${encodeURIComponent(newName)}`),
}

// History API
export const historyAPI = {
  getAll: (limit = 50, offset = 0, status?: string, dateFrom?: string, dateTo?: string) => {
    const params = new URLSearchParams({
      limit: String(limit),
      offset: String(offset),
    })
    if (status) params.append('status', status)
    if (dateFrom) params.append('date_from', dateFrom)
    if (dateTo) params.append('date_to', dateTo)
    return api.get(`/history?${params.toString()}`)
  },

  getStats: () => api.get('/history/stats'),

  delete: (historyId: number) => api.delete(`/history/${historyId}`),

  export: () => api.post('/history/export'),
}

// Settings API
export const settingsAPI = {
  get: () => api.get('/settings'),

  update: (settings: Record<string, any>) => api.put('/settings', settings),

  getYtDlpParameters: () => api.get('/settings/yt-dlp/parameters'),

  exportConfig: () => api.post('/settings/config/export'),

  importConfig: (config: Record<string, any>) => api.post('/settings/config/import', config),
}

// Scheduler API
export const schedulerAPI = {
  getTasks: () => api.get('/scheduler/tasks'),

  create: (schedule: { name: string; cron_expression: string; urls: string[]; profile_id: number; is_enabled: boolean }) =>
    api.post('/scheduler/tasks', schedule),

  update: (scheduleId: number, schedule: { name: string; cron_expression: string; urls: string[]; profile_id: number; is_enabled: boolean }) =>
    api.put(`/scheduler/tasks/${scheduleId}`, schedule),

  delete: (scheduleId: number) => api.delete(`/scheduler/tasks/${scheduleId}`),
}

// Health check
export const healthCheck = () => api.get('/health')

export default api
