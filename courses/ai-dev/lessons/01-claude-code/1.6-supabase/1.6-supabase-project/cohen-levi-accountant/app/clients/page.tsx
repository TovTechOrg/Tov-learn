import { createClient } from '@/lib/supabase/server'

type Client = {
  id: string
  name: string
  accountant_id: string | null
}

function getEntityBadge(name: string): string | null {
  if (name.includes('בע"מ')) return 'בע"מ'
  if (name.includes('שותפות')) return 'שותפות'
  if (name.includes('עמותה')) return 'עמותה'
  if (name.includes('עוסק מורשה')) return 'עוסק מורשה'
  return null
}

export default async function ClientsPage() {
  const supabase = await createClient()
  const { data: clients, error } = await supabase
    .from('clients')
    .select('id, name, accountant_id')
    .order('name')

  if (error) {
    return (
      <main className="clients-main">
        <p style={{ color: 'var(--negative)' }}>שגיאה בטעינת לקוחות: {error.message}</p>
      </main>
    )
  }

  const count = clients?.length ?? 0

  return (
    <main className="clients-main">
      <header className="page-header">
        <div className="page-title-group">
          <span className="page-eyebrow">ניהול לקוחות</span>
          <h1 className="page-title">
            לקוחות
            {count > 0 && (
              <span className="client-count" aria-label={`${count} לקוחות`}>
                {count}
              </span>
            )}
          </h1>
        </div>
        <button className="add-btn" type="button">
          + לקוח חדש
        </button>
      </header>

      <div className="search-row">
        <input
          className="search-input"
          type="search"
          placeholder="חיפוש לפי שם..."
          aria-label="חיפוש לקוחות"
        />
      </div>

      {clients && clients.length > 0 ? (
        <div className="clients-grid" role="list">
          {clients.map((client: Client) => {
            const badge = getEntityBadge(client.name)
            return (
              <div key={client.id} className="client-card" role="listitem" tabIndex={0}>
                <div className="card-top">
                  {badge ? (
                    <span className="entity-badge">{badge}</span>
                  ) : (
                    <span />
                  )}
                  <div className="card-status status-active" />
                </div>
                <div className="card-name">{client.name}</div>
                <div className="card-meta">
                  <div className="meta-row">
                    <span className="meta-label">מזהה</span>
                    <span className="meta-value">{client.id.slice(0, 18)}…</span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <p style={{ color: 'var(--text-muted)', marginTop: '3rem' }}>
          אין לקוחות להצגה.
        </p>
      )}
    </main>
  )
}
