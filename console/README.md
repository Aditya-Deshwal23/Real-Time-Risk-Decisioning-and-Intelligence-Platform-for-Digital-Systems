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

- `src/app/` — application page
- `src/styles/tokens.css` — the shared raw scale and semantic token source
- `src/styles/global.css` — font faces and global application primitives
- `src/theme/` — theme provider and `useTheme` hook
- `src/components/ui/` — icon allow-list and Icon wrapper
- `src/test/` — unit tests
- `src/main.tsx` — browser entry point

## Tokens and themes

`src/styles/tokens.css` is the source of truth. Dark values are defined at `:root`; light values override the identical semantic names under `:root[data-theme="light"]`. Components must use semantic custom properties such as `var(--color-text-primary)` and spacing, radius, z-index, motion and breakpoint tokens. Raw values belong only in the token source.

The default theme is dark. The `verdict-theme-preference` storage key accepts `light`, `dark` or `system`. `public/theme-init.js` applies the stored choice or falls back to dark before first paint without an inline script. The React provider updates the choice, follows OS changes for `system`, and falls back safely when storage is blocked.

## Fonts and icons

IBM Plex Sans (400, 500, 600) and IBM Plex Mono (400, 500) are self-hosted Latin WOFF2 files in `public/fonts`. Font licences are in `public/fonts/*-LICENSE.txt` and recorded in `docs/compatibility-matrix.md`.

Lucide icons come only through `src/components/ui/icons.ts`. `src/components/ui/Icon.tsx` applies 14, 16, 20 or 24 px token sizes and the 1.75 token stroke. Decorative icons require `decorative`; meaningful icons require a string `label`.

## Theme and token checks

- `tools/ci/check_tokens.py` rejects raw hex colours and off-scale spacing, radius or z-index values outside `tokens.css`.
- `tools/ci/check_contrast.py` parses the theme token values and verifies the contrast pairs declared in `ui-context.md`.
- Theme fixtures, icon accessibility and the separate theme-initialisation script are covered by Vitest tests.

## Primitives

Public primitives are exported only from `src/components/ui/index.ts`. Product code must import from that index, never from an individual primitive file.

Before adding a primitive:

1. Confirm a named consumer exists in the shell or in a Phase 4 or Phase 5 page.
2. Use Radix primitives for focus traps, roving tabindex, ARIA wiring, portals and complex keyboard behavior.
3. Use semantic tokens only; run `tools/ci/check_tokens.py` before adding a raw value.
4. Cover default, hover, focus-visible, active, disabled, loading, error and empty states where applicable in light and dark.
5. Add a Storybook story with purpose, props, keyboard behavior and do/don't guidance.
6. Add Vitest and Testing Library interaction tests that query by role and accessible name.
7. Preserve status text and icons; never use colour alone.
8. Run `npm run lint`, `npm run typecheck`, `npm run test`, `npm run build` and `npm run storybook:build`.

The documentation build is `npm run storybook:build`. Story files live beside the primitive implementation under `src/components/ui/`.

## Platform connection in development

The planned development arrangement is a same-origin Vite proxy for `/console/v1` to the platform's local origin. The platform architecture also permits direct local CORS from `http://localhost:5173` with credentials and the CSRF header; it forbids wildcard origins with credentials. Neither the proxy nor CORS is configured in this skeleton; Phase 4 implements the selected arrangement.
