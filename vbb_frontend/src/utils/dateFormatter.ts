import { format } from 'date-fns'

export const formatTime = (timestamp: string): string => {
  return format(new Date(timestamp), 'HH:mm')
}
