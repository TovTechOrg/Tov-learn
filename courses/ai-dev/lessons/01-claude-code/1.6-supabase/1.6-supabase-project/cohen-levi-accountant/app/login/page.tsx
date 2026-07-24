'use client'

import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { createClient } from '@/lib/supabase/client'

export default function LoginPage() {
  const supabase = createClient()

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6">כהן-לוי | כניסה</h1>
        <Auth
          supabaseClient={supabase}
          appearance={{ theme: ThemeSupa }}
          providers={[]}
          localization={{
            variables: {
              sign_in: {
                email_label: 'אימייל',
                password_label: 'סיסמה',
                button_label: 'כניסה',
              },
              sign_up: {
                email_label: 'אימייל',
                password_label: 'סיסמה',
                button_label: 'הרשמה',
              },
            },
          }}
        />
      </div>
    </main>
  )
}
