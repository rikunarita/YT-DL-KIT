import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export interface HistoryRecord {
  id: number
  task_id?: number
  url: string
  output_filename?: string
  file_size?: number
  status: string
  duration_seconds?: number
  error_message?: string
  completed_at: string
  profile_name?: string
}

interface HistoryState {
  records: HistoryRecord[]
  total: number
  offset: number
  limit: number
  loading: boolean
  error?: string
}

const initialState: HistoryState = {
  records: [],
  total: 0,
  offset: 0,
  limit: 50,
  loading: false,
}

const historySlice = createSlice({
  name: 'history',
  initialState,
  reducers: {
    setRecords: (state, action: PayloadAction<{ records: HistoryRecord[]; total: number }>) => {
      state.records = action.payload.records
      state.total = action.payload.total
    },
    addRecord: (state, action: PayloadAction<HistoryRecord>) => {
      state.records.unshift(action.payload)
      state.total += 1
    },
    removeRecord: (state, action: PayloadAction<number>) => {
      state.records = state.records.filter(r => r.id !== action.payload)
      state.total -= 1
    },
    setOffset: (state, action: PayloadAction<number>) => {
      state.offset = action.payload
    },
    setLimit: (state, action: PayloadAction<number>) => {
      state.limit = action.payload
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

export const { 
  setRecords, 
  addRecord, 
  removeRecord, 
  setOffset, 
  setLimit,
  setLoading, 
  setError, 
  clearError 
} = historySlice.actions
export default historySlice.reducer
