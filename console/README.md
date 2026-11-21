# console/

**Responsibility:** React and TypeScript developer console and analyst workbench.

**Must never contain:** Secrets, direct machine-API credentials, or server-side decision logic.

**First implementation phase:** Phase 1 — console toolchain skeleton; product UI foundations start in Phase 3.

## Toolchain

The project uses the Node.js version in `.nvmrc`, npm, and the versions pinned in `package-lock.json`. Install with `npm ci`.

| Command                | Purpose                                |
| ---------------------- | -------------------------------------- |
| `npm run dev`          | Start the Vite development server      |
| `npm run lint`         | Run ESLint with zero warnings allowed  |
| `npm run format:check` | Check formatting with Prettier         |
| `npm run typecheck`    | Run strict TypeScript checking         |
| `npm run test`         | Run Vitest and Testing Library tests   |
| `npm run build`        | Type-check and create the static build |

## Structure

- `src/app/` — placeholder application page
- `src/styles/` — CSS reset only
- `src/test/` — unit tests
- `src/main.tsx` — browser entry point

No product feature folders, design tokens, routes, or component libraries are included yet.

## Platform connection in development

The planned development arrangement is a same-origin Vite proxy for `/console/v1` to the platform's local origin. The platform architecture also permits direct local CORS from `http://localhost:5173` with credentials and the CSRF header; it forbids wildcard origins with credentials. Neither the proxy nor CORS is configured in this skeleton; Phase 4 implements the selected arrangement.
