'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type Branch = {
  id: number
  name: string
  city: string
}

export default function Home() {
  const [branches, setBranches] = useState<Branch[]>([])

  useEffect(() => {
    const supabase = createClient()
    supabase
      .from('branches')
      .select('*')
      .then(({ data }) => setBranches(data ?? []))
  }, [])

  return (
    <main className="max-w-xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">סניפי חומוס אליהו</h1>
      <ul className="space-y-3">
        {branches.map((branch) => (
          <li key={branch.id} className="flex justify-between border rounded-lg p-4">
            <span className="font-medium">{branch.name}</span>
            <span className="text-gray-500">{branch.city}</span>
          </li>
        ))}
      </ul>
    </main>
  )
}
