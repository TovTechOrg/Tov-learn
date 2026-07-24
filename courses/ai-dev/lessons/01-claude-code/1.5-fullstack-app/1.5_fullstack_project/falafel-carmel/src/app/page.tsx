import { getMenuItems } from '@/actions/menuActions'
import AddMenuItemForm from '@/components/AddMenuItemForm'

type MenuItem = {
  id: string
  name: string
  description: string
  price: number
  isSpicy: boolean
  createdAt: Date
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatPrice(price: number): string {
  return price % 1 === 0 ? price.toFixed(0) : price.toFixed(2)
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function SpicyBadge() {
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-bold text-red-600">
      🌶️ חריף
    </span>
  )
}

function MenuItemCard({ item }: { item: MenuItem }) {
  return (
    <article className="group flex flex-col gap-4 rounded-2xl border border-amber-100 bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md">

      {/* Title row */}
      <div className="flex items-start justify-between gap-3">
        <h2 className="text-lg font-bold leading-snug text-stone-800">
          {item.name}
        </h2>
        {item.isSpicy && <SpicyBadge />}
      </div>

      {/* Description */}
      <p className="flex-1 text-sm leading-relaxed text-stone-500">
        {item.description}
      </p>

      {/* Price row */}
      <div className="flex items-center justify-between border-t border-amber-50 pt-4">
        <span className="text-2xl font-black tracking-tight text-amber-600">
          ₪{formatPrice(item.price)}
        </span>
        <span className="text-xs text-stone-400">כולל מע&quot;מ</span>
      </div>

    </article>
  )
}

function EmptyState() {
  return (
    <div className="col-span-full flex flex-col items-center gap-4 py-24 text-center">
      <span className="text-6xl">🧆</span>
      <p className="text-xl font-bold text-stone-600">התפריט עדיין ריק</p>
      <p className="text-sm text-stone-400">הוסף מנות דרך לוח הניהול כדי להתחיל</p>
    </div>
  )
}

// ─── Page (Server Component) ───────────────────────────────────────────────────

export default async function HomePage() {
  const items = await getMenuItems()

  return (
    <div className="min-h-screen bg-stone-50">

      {/* ── Header ── */}
      <header className="bg-stone-900 px-6 pb-12 pt-10 text-center">
        <p className="mb-2 text-xs font-bold uppercase tracking-[0.2em] text-amber-400">
          מסעדת רחוב · ישראל
        </p>
        <h1 className="text-5xl font-black text-white">
          פלאפל{' '}
          <span className="text-amber-400">כרמל</span>
        </h1>
        <p className="mt-3 text-sm text-stone-400">
          טרי מהמחבת — בישול אמיתי כל יום מחדש
        </p>
        <div className="mx-auto mt-8 flex items-center justify-center gap-3 text-stone-600">
          <div className="h-px w-16 bg-stone-700" />
          <span className="text-xs text-stone-500">☀ פתוח ב-10:00</span>
          <div className="h-px w-16 bg-stone-700" />
        </div>
      </header>

      {/* ── Decorative edge ── */}
      <div className="h-2 bg-gradient-to-r from-amber-400 via-orange-400 to-amber-500" />

      {/* ── Menu section ── */}
      <main className="mx-auto max-w-5xl px-4 py-10">

        <AddMenuItemForm />

        {/* Section header */}
        <div className="mb-8 flex items-center gap-3">
          <h2 className="text-2xl font-black text-stone-800">התפריט שלנו</h2>
          <span className="rounded-full bg-amber-100 px-3 py-0.5 text-sm font-bold text-amber-700">
            {items.length} מנות
          </span>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {items.length === 0 ? (
            <EmptyState />
          ) : (
            items.map((item) => (
              <MenuItemCard key={item.id} item={item} />
            ))
          )}
        </div>

      </main>

      {/* ── Footer ── */}
      <footer className="mt-16 border-t border-stone-200 py-8 text-center text-xs text-stone-400">
        <p>פלאפל כרמל · נסגר כשנגמר הפלאפל</p>
      </footer>

    </div>
  )
}
