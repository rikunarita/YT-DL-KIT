import { useEffect, useState } from 'react'

export interface ProgressUpdate {
  percent: number
  speed?: string
  eta?: string
}

export const useWebSocket = (taskId: number) => {
  const [progress, setProgress] = useState<ProgressUpdate>({
    percent: 0,
  })
  const [connected, setConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/downloads/${taskId}`)

    ws.onopen = () => {
      console.log(`WebSocket connected for task ${taskId}`)
      setConnected(true)
      setError(null)
    }

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        if (message.type === 'progress') {
          setProgress(message.data)
        }
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e)
      }
    }

    ws.onerror = (event) => {
      console.error('WebSocket error:', event)
      setError('WebSocket connection error')
      setConnected(false)
    }

    ws.onclose = () => {
      console.log(`WebSocket closed for task ${taskId}`)
      setConnected(false)
    }

    return () => {
      ws.close()
    }
  }, [taskId])

  return { progress, connected, error }
}
