'use client'

import { useActionState } from 'react'
import { offerRide } from '@/actions/rides'

const initialState = { error: undefined as string | undefined, success: false }

export default function OfferRideForm() {
  const [state, action, pending] = useActionState(
    async (_prev: typeof initialState, formData: FormData) => {
      const result = await offerRide(formData)
      return { error: result.error, success: result.success ?? false }
    },
    initialState
  )

  return (
    <form action={action} className="bg-white rounded-2xl shadow p-6 space-y-4">
      <h2 className="text-lg font-bold">🚗 הצע טרמפ</h2>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-sm text-gray-600">מוצא</label>
          <input name="origin" required placeholder="תל אביב"
            className="w-full mt-1 border rounded-lg px-3 py-2 text-sm" />
        </div>
        <div>
          <label className="text-sm text-gray-600">יעד</label>
          <input name="destination" required placeholder="חיפה"
            className="w-full mt-1 border rounded-lg px-3 py-2 text-sm" />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-sm text-gray-600">זמן יציאה</label>
          <input name="departure_time" type="datetime-local" required
            className="w-full mt-1 border rounded-lg px-3 py-2 text-sm" />
        </div>
        <div>
          <label className="text-sm text-gray-600">מקומות פנויים</label>
          <input name="seats_available" type="number" min="1" max="8" defaultValue="3" required
            className="w-full mt-1 border rounded-lg px-3 py-2 text-sm" />
        </div>
      </div>

      {state.error && <p className="text-red-500 text-sm">{state.error}</p>}
      {state.success && <p className="text-green-600 text-sm">הטרמפ נוסף בהצלחה!</p>}

      <button type="submit" disabled={pending}
        className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 rounded-lg transition-colors disabled:opacity-50">
        {pending ? 'שולח...' : 'פרסם טרמפ'}
      </button>
    </form>
  )
}
