'use server'

import { createClient } from '@/lib/supabase/server'

export type Shift = {
  id: string
  employee: string
  start_time: string
  end_time: string
  is_morning: boolean
  created_at: string
  updated_at: string
}

export async function getShifts(): Promise<{ data: Shift[] | null; error: string | null }> {
  const supabase = await createClient()

  const { data, error } = await supabase
    .from('shifts')
    .select('*')
    .order('start_time', { ascending: false })

  if (error) {
    return { data: null, error: error.message }
  }

  return { data, error: null }
}
