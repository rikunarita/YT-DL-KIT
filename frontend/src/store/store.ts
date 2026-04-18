import { configureStore } from '@reduxjs/toolkit'
import downloadSlice from './slices/downloadSlice'
import profileSlice from './slices/profileSlice'
import historySlice from './slices/historySlice'

const store = configureStore({
  reducer: {
    downloads: downloadSlice,
    profiles: profileSlice,
    history: historySlice,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

export default store
