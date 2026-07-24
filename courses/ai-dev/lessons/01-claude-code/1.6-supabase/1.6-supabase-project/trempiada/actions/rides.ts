'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'

export async function offerRide(formData: FormData) {
  const supabase = await createClient()

  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) return { error: 'יש להתחבר כדי להציע טרמפ' }

  const { error } = await supabase.from('rides').insert({
    driver_id:       user.id,
    origin:          formData.get('origin') as string,
    destination:     formData.get('destination') as string,
    departure_time:  formData.get('departure_time') as string,
    seats_available: Number(formData.get('seats_available')),
  })

  if (error) return { error: error.message }

  revalidatePath('/')
  return { success: true }
}
