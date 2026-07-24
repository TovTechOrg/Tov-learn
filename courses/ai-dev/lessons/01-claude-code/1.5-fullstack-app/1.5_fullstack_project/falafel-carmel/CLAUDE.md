# falafel-carmel — Project Guidelines

## Stack
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **ORM:** Prisma
- **Database:** PostgreSQL
- **Package manager:** npm

---

## 1. Routing — App Router only
- All routes live under `src/app/`.
- Never use `src/pages/` — the Pages Router is disabled for this project.
- Layouts go in `layout.tsx`, loading states in `loading.tsx`, error boundaries in `error.tsx`.

## 2. React Server Components — default
Use **Server Components** by default for every new file.  
Add `"use client"` **only** when the component requires:
- React hooks (`useState`, `useEffect`, `useRef`, etc.)
- Browser-only APIs (`window`, `document`, `localStorage`)
- Event listeners (`onClick`, `onChange`, etc.)

```tsx
// ✅ Server Component (default — no directive needed)
export default async function MenuPage() {
  const items = await db.menuItem.findMany();
  return <ul>{items.map(i => <li key={i.id}>{i.name}</li>)}</ul>;
}

// ✅ Client Component (interactivity required)
"use client";
export default function AddToCartButton({ id }: { id: string }) {
  const [added, setAdded] = useState(false);
  return <button onClick={() => setAdded(true)}>...</button>;
}
```

## 3. Data mutations — Server Actions only
- All create / update / delete operations must use **Server Actions**.
- Define actions in `src/app/actions/` or co-locate in `actions.ts` next to the relevant page.
- Never expose mutation logic through API Route Handlers for internal use.

```ts
// src/app/actions/order.ts
"use server";
import { db } from "@/lib/db";
import { revalidatePath } from "next/cache";

export async function createOrder(data: OrderInput) {
  await db.order.create({ data });
  revalidatePath("/orders");
}
```

## 4. Styling — Tailwind CSS only
- All styles must use **Tailwind utility classes**.
- No CSS Modules, no `styled-components`, no inline `style={{}}` props (except for dynamic values that Tailwind can't express).
- Use `cn()` (from `clsx` + `tailwind-merge`) for conditional classes.

```tsx
// ✅
<button className="rounded-xl bg-amber-500 px-4 py-2 font-bold text-white hover:bg-amber-600">
  הזמן
</button>

// ❌ No CSS Modules, no inline styles for static values
```

## 5. Prisma + PostgreSQL
- Schema lives in `prisma/schema.prisma`.
- Database client is a **singleton** — import from `src/lib/db.ts`, never instantiate `PrismaClient` directly in components.
- Run migrations with `npx prisma migrate dev`.
- Never query the database from a Client Component — always via a Server Component or Server Action.

```ts
// src/lib/db.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
export const db = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db;
```

---

## Folder structure (after scaffolding)
```
src/
  app/
    layout.tsx          ← root layout (Server Component)
    page.tsx            ← home page (Server Component)
    actions/            ← Server Actions
    (routes)/           ← feature route groups
  components/
    ui/                 ← purely presentational, no data fetching
    (feature)/          ← feature-specific components
  lib/
    db.ts               ← Prisma singleton
prisma/
  schema.prisma
```

---

## Scaffold command (run once, requires Node.js ≥ 18)
```bash
npx create-next-app@latest falafel-carmel \
  --typescript --tailwind --eslint --app --use-npm --src-dir --no-import-alias
```
Then install Prisma:
```bash
npm install prisma @prisma/client
npx prisma init
```
