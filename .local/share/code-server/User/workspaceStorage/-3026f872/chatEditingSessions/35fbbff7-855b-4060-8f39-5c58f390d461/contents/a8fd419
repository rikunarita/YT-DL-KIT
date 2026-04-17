import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export interface Profile {
  id?: number
  name: string
  description?: string
  parameters: Record<string, any>
  created_at?: string
  updated_at?: string
}

interface ProfileState {
  profiles: Profile[]
  selectedProfileId?: number
  loading: boolean
  error?: string
}

const initialState: ProfileState = {
  profiles: [],
  loading: false,
}

const profileSlice = createSlice({
  name: 'profiles',
  initialState,
  reducers: {
    setProfiles: (state, action: PayloadAction<Profile[]>) => {
      state.profiles = action.payload
    },
    addProfile: (state, action: PayloadAction<Profile>) => {
      state.profiles.push(action.payload)
    },
    updateProfile: (state, action: PayloadAction<Profile>) => {
      const index = state.profiles.findIndex(p => p.id === action.payload.id)
      if (index !== -1) {
        state.profiles[index] = action.payload
      }
    },
    removeProfile: (state, action: PayloadAction<number>) => {
      state.profiles = state.profiles.filter(p => p.id !== action.payload)
    },
    selectProfile: (state, action: PayloadAction<number>) => {
      state.selectedProfileId = action.payload
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
  setProfiles, 
  addProfile, 
  updateProfile, 
  removeProfile, 
  selectProfile, 
  setLoading, 
  setError, 
  clearError 
} = profileSlice.actions
export default profileSlice.reducer
