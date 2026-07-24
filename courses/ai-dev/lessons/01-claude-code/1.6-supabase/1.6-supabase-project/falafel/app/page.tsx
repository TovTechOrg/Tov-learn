'use client'

import { useEffect, useState, useCallback } from 'react'
import { createClient } from '@/lib/supabase/client'

type Order = {
  id: string
  status: string
  total_price: number
  created_at: string
}

const STATUS_LABEL: Record<string, string> = {
  pending:   'ממתין',
  preparing: 'בהכנה',
  ready:     'מוכן!',
}

const STATUS_COLOR: Record<string, string> = {
  pending:   'border-yellow-400 text-yellow-300',
  preparing: 'border-blue-400 text-blue-300',
  ready:     'border-green-400 text-green-300',
}

let audioCtx: AudioContext | null = null

async function playDing() {
  if (!audioCtx) audioCtx = new AudioContext()
  await audioCtx.resume()
  const osc = audioCtx.createOscillator()
  const gain = audioCtx.createGain()
  osc.connect(gain)
  gain.connect(audioCtx.destination)
  osc.frequency.setValueAtTime(880, audioCtx.currentTime)
  osc.frequency.exponentialRampToValueAtTime(440, audioCtx.currentTime + 0.3)
  gain.gain.setValueAtTime(0.4, audioCtx.currentTime)
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4)
  osc.start(audioCtx.currentTime)
  osc.stop(audioCtx.currentTime + 0.4)
}

export default function OrdersScreen() {
  const [orders, setOrders] = useState<Order[]>([])
  const [flash, setFlash] = useState<string | null>(null)

  const triggerFlash = useCallback((id: string) => {
    setFlash(id)
    setTimeout(() => setFlash(null), 800)
  }, [])

  useEffect(() => {
    const supabase = createClient()

    supabase
      .from('orders')
      .select('*')
      .order('created_at', { ascending: false })
      .then(({ data }: { data: Order[] | null }) => setOrders(data ?? []))

    const channel = supabase
      .channel('orders-realtime')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'orders' },
        (payload: { new: Order }) => {
          playDing()
          triggerFlash(payload.new.id)
          setOrders((prev) => [payload.new, ...prev])
        }
      )
      .on(
        'postgres_changes',
        { event: 'UPDATE', schema: 'public', table: 'orders' },
        (payload: { new: Order }) => {
          playDing()
          triggerFlash(payload.new.id)
          setOrders((prev) =>
            prev.map((o) => (o.id === payload.new.id ? payload.new : o))
          )
        }
      )
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [triggerFlash])

  return (
    <main className="min-h-screen bg-black text-white p-6 font-mono">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-black tracking-widest text-yellow-400 uppercase">
          🧆 פלאפל הקוסם
        </h1>
        <p className="text-gray-500 text-sm mt-1 tracking-widest">LIVE ORDERS</p>
      </header>

      {orders.length === 0 && (
        <p className="text-center text-gray-600 tracking-widest">-- אין הזמנות --</p>
      )}

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 max-w-5xl mx-auto">
        {orders.map((order) => (
          <div
            key={order.id}
            className={`
              border-2 rounded-lg p-4 transition-all duration-300
              ${STATUS_COLOR[order.status] ?? 'border-gray-600 text-gray-400'}
              ${flash === order.id ? 'scale-105 brightness-150' : ''}
            `}
          >
            <p className="text-xs text-gray-500 mb-1">#{order.id.slice(0, 6).toUpperCase()}</p>
            <p className="text-3xl font-black">₪{order.total_price}</p>
            <p className="text-lg font-bold mt-2 tracking-widest">
              {STATUS_LABEL[order.status] ?? order.status}
            </p>
            <p className="text-xs text-gray-600 mt-2">
              {new Date(order.created_at).toLocaleTimeString('he-IL')}
            </p>
          </div>
        ))}
      </div>
    </main>
  )
}
