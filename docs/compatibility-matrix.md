# Compatibility Matrix

| Ecosystem | Package or tool | Version | Verification source | Compatibility notes | Status |
|---|---|---|---|---|---|
| Web | Node.js | 26.13.0 | [Node.js v26.13.0 release](https://nodejs.org/en/blog/release/v26.13.0), verified 2026-11-21 | Installed version; satisfies Vite, Vitest, jsdom and ESLint engine ranges | verified |
| Web | npm | 11.20.0 | `npm --version`, official npm CLI release metadata, verified 2026-11-21 | Lockfile generated with npm; frozen installs use `npm ci` | verified |
| Web | React / React DOM | 19.3.1 | [npm React 19.3.1](https://www.npmjs.com/package/react/v/19.3.1), [npm React DOM 19.3.1](https://www.npmjs.com/package/react-dom/v/19.3.1), verified 2026-11-21 | React DOM peer requires React `^19.3.1` | verified |
| Web | Vite | 8.3.8 | [npm Vite 8.3.8](https://www.npmjs.com/package/vite/v/8.3.8), verified 2026-11-21 | Node engine `^20.19.0 || >=22.12.0` | verified |
| Web | `@vitejs/plugin-react` | 6.3.0 | [npm @vitejs/plugin-react 6.3.0](https://www.npmjs.com/package/@vitejs/plugin-react/v/6.3.0), verified 2026-11-21 | Vite peer `^8.0.0` | verified |
| Web | TypeScript | 6.0.3 | [npm TypeScript 6.0.3](https://www.npmjs.com/package/typescript/v/6.0.3), verified 2026-11-21 | Selected to satisfy `typescript-eslint` peer `<6.1.0` | verified |
| Web | ESLint / `@eslint/js` | 9.39.5 | [npm ESLint 9.39.5](https://www.npmjs.com/package/eslint/v/9.39.5), [npm @eslint/js 9.39.5](https://www.npmjs.com/package/@eslint/js/v/9.39.5), verified 2026-11-21 | ESLint 9 is supported by required jsx-a11y and typescript-eslint versions | verified |
| Web | `typescript-eslint` | 8.73.0 | [npm typescript-eslint 8.73.0](https://www.npmjs.com/package/typescript-eslint/v/8.73.0), verified 2026-11-21 | Peer range: TypeScript `>=4.8.4 <6.1.0`; ESLint `^8.57.0 || ^9.0.0 || ^10.0.0` | verified |
| Web | `eslint-plugin-jsx-a11y` | 6.10.2 | [npm eslint-plugin-jsx-a11y 6.10.2](https://www.npmjs.com/package/eslint-plugin-jsx-a11y/v/6.10.2), verified 2026-11-21 | Peer range includes ESLint 9 and excludes ESLint 10 | verified |
| Web | `eslint-plugin-react-hooks` | 7.1.1 | [npm eslint-plugin-react-hooks 7.1.1](https://www.npmjs.com/package/eslint-plugin-react-hooks/v/7.1.1), verified 2026-11-21 | Peer range includes ESLint 9 | verified |
| Web | Vitest | 5.1.1 | [npm Vitest 5.1.1](https://www.npmjs.com/package/vitest/v/5.1.1), verified 2026-11-21 | Vite peer range includes 8; Node engine includes 26 | verified |
| Web | Testing Library | 16.3.3 (`@testing-library/react`), 10.4.2 (`@testing-library/dom`) | [npm @testing-library/react 16.3.3](https://www.npmjs.com/package/@testing-library/react/v/16.3.3), [npm @testing-library/dom 10.4.2](https://www.npmjs.com/package/@testing-library/dom/v/10.4.2), verified 2026-11-21 | DOM package is the required peer of React Testing Library | verified |
| Web | jsdom | 31.0.1 | [npm jsdom 31.0.1](https://www.npmjs.com/package/jsdom/v/31.0.1), verified 2026-11-21 | Test-only environment; Node engine `^22.22.2 || ^24.15.0 || >=26.0.0` | verified |
| Web | React type declarations | 19.3.0 (`@types/react`), 19.3.0 (`@types/react-dom`) | [npm @types/react 19.3.0](https://www.npmjs.com/package/@types/react/v/19.3.0), [npm @types/react-dom 19.3.0](https://www.npmjs.com/package/@types/react-dom/v/19.3.0), verified 2026-11-21 | Type declarations for the pinned React runtime | verified |
| Web | Prettier | 3.10.1 | [npm Prettier 3.10.1](https://www.npmjs.com/package/prettier/v/3.10.1), verified 2026-11-21 | Formatting only; lint remains a separate gate | verified |
