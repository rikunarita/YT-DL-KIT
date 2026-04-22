import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export interface DownloadTask {
  id?: number
  url: string
  profile_id?: number
  status: string
  progress_percent: number
  speed?: string
  eta?: string
  current_filename?: string
  error_message?: string
}

interface DownloadState {
  tasks: DownloadTask[]
  activeTaskId?: number
  loading: boolean
  error?: string
}

const initialState: DownloadState = {
  tasks: [],
  loading: false,
}

const downloadSlice = createSlice({
  name: 'downloads',
  initialState,
  reducers: {
    setTasks: (state, action: PayloadAction<DownloadTask[]>) => {
      state.tasks = action.payload
    },
    addTask: (state, action: PayloadAction<DownloadTask>) => {
      state.tasks.push(action.payload)
    },
    updateTask: (state, action: PayloadAction<DownloadTask>) => {
      const index = state.tasks.findIndex(t => t.id === action.payload.id)
      if (index !== -1) {
        state.tasks[index] = action.payload
      }
    },
    removeTask: (state, action: PayloadAction<number>) => {
      state.tasks = state.tasks.filter(t => t.id !== action.payload)
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload
    },
    clearError: (state) => {
      state.error = undefined
    },
  },
})

export const { setTasks, addTask, updateTask, removeTask, setLoading, setError, clearError } = downloadSlice.actions
export default downloadSlice.reducer
