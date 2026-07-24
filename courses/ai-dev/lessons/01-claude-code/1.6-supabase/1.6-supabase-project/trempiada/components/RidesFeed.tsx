'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type Ride = {
  id: string
  origin: string
  destination: string
  departure_time: string
  seats_available: number
  driver_id: string
}

export default function RidesFeed({ initial }: { initial: Ride[] }) {
  const [rides, setRides] = useState<Ride[]>(initial)
  const [newRideId, setNewRideId] = useState<string | null>(null)

  useEffect(() => {
    const supabase = createClient()

    const channel = supabase
      .channel('rides-feed')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'rides' },
        (payload: { new: Ride }) => {
          setRides((prev) => [payload.new, ...prev])
          setNewRideId(payload.new.id)
          setTimeout(() => setNewRideId(null), 2000)
        }
      )
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [])

  return (
    <div className="space-y-3">
      <h2 className="text-lg font-bold">🗺️ טרמפים זמינים</h2>
      {rides.length === 0 && (
        <p className="text-gray-400 text-sm text-center py-8">אין טרמפים כרגע — היה הראשון!</p>
      )}
      {rides.map((ride) => (
        <div key={ride.id}
          className={`bg-white rounded-xl shadow p-4 flex justify-between items-center transition-all duration-500
            ${newRideId === ride.id ? 'ring-2 ring-green-400 scale-[1.02]' : ''}`}>
          <div>
            <p className="font-bold text-base">
              מ-{ride.origin} ל-{ride.destination}
            </p>
            <p className="text-sm text-gray-500 mt-1">
              {new Date(ride.departure_time).toLocaleString('he-IL', {
                weekday: 'short', day: 'numeric', month: 'numeric',
                hour: '2-digit', minute: '2-digit'
              })}
            </p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-black text-green-600">{ride.seats_available}</p>
            <p className="text-xs text-gray-400">מקומות</p>
          </div>
        </div>
      ))}
    </div>
  )
}
