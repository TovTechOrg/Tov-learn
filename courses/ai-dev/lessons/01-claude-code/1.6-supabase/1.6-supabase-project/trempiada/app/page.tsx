import { createClient } from '@/lib/supabase/server'
import OfferRideForm from '@/components/OfferRideForm'
import RidesFeed from '@/components/RidesFeed'

export default async function Home() {
  const supabase = await createClient()

  const { data: rides } = await supabase
    .from('rides')
    .select('*')
    .order('departure_time', { ascending: true })

  const { data: { user } } = await supabase.auth.getUser()

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-lg mx-auto space-y-6">
        <header className="text-center">
          <h1 className="text-3xl font-black">🚐 טרמפיאדה</h1>
          <p className="text-gray-500 text-sm mt-1">טרמפים לחיילים בסוף שבוע</p>
        </header>

        {user ? (
          <OfferRideForm />
        ) : (
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-center text-sm text-blue-700">
            <a href="/login" className="font-bold underline">התחברו עם Google</a> כדי להציע טרמפ
          </div>
        )}

        <RidesFeed initial={rides ?? []} />
      </div>
    </main>
  )
}
