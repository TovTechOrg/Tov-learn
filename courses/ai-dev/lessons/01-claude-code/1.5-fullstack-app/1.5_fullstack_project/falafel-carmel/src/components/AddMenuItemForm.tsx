'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { createMenuItem } from '@/actions/menuActions'

export default function AddMenuItemForm() {
  const [pending, setPending] = useState(false)

  async function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>) {
    e.preventDefault()
    const form = e.currentTarget
    setPending(true)

    const result = await createMenuItem(new FormData(form))

    if (result.success) {
      toast.success(result.message)
      form.reset()
    } else {
      toast.error(result.message)
    }

    setPending(false)
  }

  return (
    <section className="mx-auto mb-10 max-w-xl rounded-2xl border border-amber-100 bg-white p-6 shadow-sm">
      <h3 className="mb-5 text-lg font-black text-stone-800">הוספת מנה חדשה</h3>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-stone-500">שם המנה</label>
          <input
            name="name"
            required
            placeholder="פלאפל, סביח, שקשוקה..."
            className="rounded-lg border border-stone-200 px-3 py-2 text-sm text-stone-800 outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-100"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-stone-500">תיאור</label>
          <input
            name="description"
            required
            placeholder="חומוס ביתי, עגבניות טריות..."
            className="rounded-lg border border-stone-200 px-3 py-2 text-sm text-stone-800 outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-100"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-stone-500">מחיר (₪)</label>
          <input
            name="price"
            type="number"
            required
            min="0"
            step="0.5"
            placeholder="25"
            className="rounded-lg border border-stone-200 px-3 py-2 text-sm text-stone-800 outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-100"
          />
        </div>

        <label className="flex cursor-pointer items-center gap-3 rounded-lg border border-stone-200 px-3 py-2.5">
          <input
            name="isSpicy"
            type="checkbox"
            className="h-4 w-4 rounded accent-red-500"
          />
          <span className="text-sm text-stone-700">🌶️ מנה חריפה</span>
        </label>

        <button
          type="submit"
          disabled={pending}
          className="w-full rounded-xl bg-amber-500 py-3 text-sm font-bold text-white transition-colors hover:bg-amber-600 disabled:opacity-60"
        >
          {pending ? 'מוסיף מנה...' : '+ הוסף מנה'}
        </button>

      </form>
    </section>
  )
}
