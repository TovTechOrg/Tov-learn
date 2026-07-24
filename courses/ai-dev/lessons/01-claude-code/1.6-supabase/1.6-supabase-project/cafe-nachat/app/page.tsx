import { getShifts } from '@/actions/shifts'

export default async function Home() {
  const { data: shifts, error } = await getShifts()

  return (
    <main className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">משמרות קפה נחת</h1>

      {error && (
        <p className="text-red-500 mb-4">שגיאה: {error}</p>
      )}

      {shifts && shifts.length === 0 && (
        <p className="text-gray-500">אין משמרות להצגה</p>
      )}

      <ul className="space-y-3">
        {shifts?.map((shift) => (
          <li key={shift.id} className="border rounded-lg p-4 flex justify-between items-center">
            <div>
              <p className="font-medium">{shift.employee}</p>
              <p className="text-sm text-gray-500">
                {new Date(shift.start_time).toLocaleString('he-IL')} —{' '}
                {new Date(shift.end_time).toLocaleString('he-IL')}
              </p>
            </div>
            <span className={`text-sm px-2 py-1 rounded ${shift.is_morning ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'}`}>
              {shift.is_morning ? 'בוקר' : 'ערב'}
            </span>
          </li>
        ))}
      </ul>
    </main>
  )
}
