import { createClient } from '@/lib/supabase/server'

function deriveInitials(email: string): string {
  const local = email.split('@')[0]
  const parts = local.split(/[._-]/)
  return parts
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase() ?? '')
    .join('')
}

export default async function ClientsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const {
    data: { user },
  } = await supabase.auth.getUser()

  const email = user?.email ?? ''
  const initials = email ? deriveInitials(email) : '?'
  const displayName = email.split('@')[0]

  return (
    <>
      <nav className="navbar" role="navigation" aria-label="ניווט ראשי">
        <div className="navbar-brand">
          <div className="brand-stamp" aria-hidden="true">כ״ל</div>
          <div className="brand-text">
            <span className="brand-name">כהן לוי</span>
            <span className="brand-sub">רואי חשבון</span>
          </div>
        </div>
        <ul className="navbar-nav" role="list">
          <li><a className="nav-link active" href="/clients" aria-current="page">לקוחות</a></li>
          <li><a className="nav-link" href="#">דוחות</a></li>
          <li><a className="nav-link" href="#">מסמכים</a></li>
        </ul>
        <div className="profile-chip" aria-label={`מחובר כ-${displayName}`}>
          <div className="profile-avatar" aria-hidden="true">{initials}</div>
          {displayName}
        </div>
      </nav>
      {children}
    </>
  )
}
