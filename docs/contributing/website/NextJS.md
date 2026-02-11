# Next.js Frontend (App Router)

## Prerequisites

- **Node.js** 20+ and npm
- **Git** for version control
- Code editor (VS Code recommended)

## Installation & Setup

Clone the repository and navigate to the Next.js app:

```bash
git clone https://github.com/openml/openml.org.git
cd openml.org/app
npm install
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## App Structure

The Next.js App Router uses a file-based routing system with the following structure:

```
src/
├── app/                         # Next.js App Router (Pages)
│   ├── (pages)/                 # Route group
│   │   ├── datasets/            
│   │   │   ├── [id]/page.tsx    # Single dataset page
│   │   │   └── page.tsx         # Datasets list
│   │   ├── tasks/[id]/page.tsx  
│   │   ├── flows/[id]/page.tsx  
│   │   ├── runs/[id]/page.tsx   
│   │   └── layout.tsx
│   ├── layout.tsx               # Root layout
│   └── page.tsx                 # Home page
│
├── components/
│   ├── ui/                      # Reusable UI (shadcn)
│   ├── layout/                  # Header, Footer, Sidebar
│   ├── header/                  # Search, Notifications, Account
│   ├── home/                    # Home page sections
│   ├── dataset/                 # Dataset components
│   └── search/                  # Search & filters
│
├── hooks/                       # Custom React hooks
│
├── types/                       # TypeScript types
│   ├── dataset.ts
│   ├── task.ts
│   ├── flow.ts
│   └── run.ts
│
└── lib/
    ├── api.ts                   # API client
    └── utils.ts                 # Helper functions
```

### Key File Conventions

- `page.tsx` - Defines a route's UI
- `layout.tsx` - Shared UI for route segments
- `loading.tsx` - Loading UI with Suspense
- `error.tsx` - Error boundary UI
- `not-found.tsx` - 404 page

---

## TypeScript

- Use **TypeScript** for all new files
- Define proper types in `src/types/`
- Avoid using `any` - use proper types or `unknown`
- Export types that are used across multiple files

### React Components

- Use **functional components** with hooks
- Follow the component structure:
  ```tsx
  import { ... } from '...'

  interface ComponentProps {
    // Props definition
  }

  export function Component({ prop }: ComponentProps) {
    // Component logic
    return (
      // JSX
    )
  }
  ```

## Styling

- Use **Tailwind CSS** for styling
- Follow existing design patterns
- Use the `cn()` utility from `lib/utils.ts` for conditional classes
  ```tsx
  import { cn } from '@/lib/utils'

  <div className={cn("base-class", condition && "conditional-class")} />
  ```

## File Naming

- Components: **PascalCase** (`DatasetHeader.tsx`)
- Utilities: **kebab-case** (`use-entity.ts`)
- Pages: **lowercase** (`page.tsx`, `layout.tsx`)

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [OpenML API Docs](https://docs.openml.org/APIs/)

---

For questions, open an issue on GitHub or ask in team discussions.
