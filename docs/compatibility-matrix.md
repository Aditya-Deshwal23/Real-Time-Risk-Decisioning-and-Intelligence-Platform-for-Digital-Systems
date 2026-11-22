# Compatibility Matrix

**Last reviewed:** 2026-11-21

| Ecosystem | Package or tool | Version | Verification source | Compatibility notes | Status |
|---|---|---|---|---|---|
| JVM | OpenJDK / Java toolchain | 25 | [OpenJDK 25](https://openjdk.org/projects/jdk/25/), verified 2026-11-21 | Gradle toolchain in `build-logic` | verified |
| JVM | Gradle | 9.6.0 | [Gradle 9.6.0 release](https://gradle.org/releases/), verified 2026-11-21 | Wrapper distribution SHA-256 in `gradle/wrapper/gradle-wrapper.properties` | verified |
| JVM | Spring Boot | 4.1.3 | [Gradle Plugin Portal: Spring Boot](https://plugins.gradle.org/plugin/org.springframework.boot), verified 2026-11-21 | Gradle plugin and dependency BOM | verified |
| JVM | Spotless | 8.12.0 | [Gradle Plugin Portal: Spotless](https://plugins.gradle.org/plugin/com.diffplug.spotless), verified 2026-11-21 | Google Java Format integration | verified |
| JVM | google-java-format | 2.0.0 | [Maven Central: google-java-format](https://central.sonatype.com/artifact/com.google.googlejavaformat/google-java-format/2.0.0), verified 2026-11-21 | Formatting engine | verified |
| JVM | SpotBugs plugin / engine | 6.5.13 / 4.10.5 | [Gradle Plugin Portal: SpotBugs](https://plugins.gradle.org/plugin/com.github.spotbugs), [Maven Central: SpotBugs 4.10.5](https://central.sonatype.com/artifact/com.github.spotbugs/spotbugs/4.10.5), verified 2026-11-21 | Static-analysis plugin and engine | verified |
| JVM | Error Prone plugin / core | 5.2.0 / 2.53.0 | [Gradle Plugin Portal: Error Prone](https://plugins.gradle.org/plugin/net.ltgt.errorprone), [Maven Central: error_prone_core 2.53.0](https://central.sonatype.com/artifact/com.google.errorprone/error_prone_core/2.53.0), verified 2026-11-21 | Compile-time static analysis | verified |
| JVM | NullAway | 0.14.4 | [Maven Central: NullAway 0.14.4](https://central.sonatype.com/artifact/com.uber.nullaway/nullaway/0.14.4), verified 2026-11-21 | Nullability analysis | verified |
| JVM | JSpecify | 1.0.1 | [Maven Central: JSpecify 1.0.1](https://central.sonatype.com/artifact/org.jspecify/jspecify/1.0.1), verified 2026-11-21 | Nullability annotations | verified |
| JVM | Checkstyle | 14.4.0 | [Maven Central: Checkstyle 14.4.0](https://central.sonatype.com/artifact/com.puppycrawl.tools/checkstyle/14.4.0), verified 2026-11-21 | Style and complexity checks | verified |
| JVM | Forbidden APIs | 3.11 | [Gradle Plugin Portal: Forbidden APIs](https://plugins.gradle.org/plugin/de.thetaphi.forbiddenapis), verified 2026-11-21 | Forbidden API signatures | verified |
| JVM | JUnit Jupiter | 6.0.2 | [Maven Central: JUnit Jupiter 6.0.2](https://central.sonatype.com/artifact/org.junit.jupiter/junit-jupiter/6.0.2), verified 2026-11-21 | JVM test platform | verified |
| JVM | ArchUnit | 1.5.1 | [Maven Central: ArchUnit JUnit 5 1.5.1](https://central.sonatype.com/artifact/com.tngtech.archunit/archunit-junit5/1.5.1), verified 2026-11-21 | Module and dependency boundary tests | verified |
| Python | Python | 3.13 | [Python 3.13 release](https://www.python.org/downloads/release/python-3130/), verified 2026-11-21 | Workspace pin in `.python-version`; uv-managed interpreter | verified |
| Python | uv | 0.13.9 | [uv 0.13.9 release](https://github.com/astral-sh/uv/releases/tag/0.13.9), verified 2026-11-21 | One committed workspace lockfile | verified |
| Python | Ruff | 0.17.6 | [PyPI: Ruff 0.17.6](https://pypi.org/project/ruff/0.17.6/), verified 2026-11-21 | Lint and format | verified |
| Python | mypy | 2.4.1 | [PyPI: mypy 2.4.1](https://pypi.org/project/mypy/2.4.1/), verified 2026-11-21 | Strict type check | verified |
| Python | pytest | 9.2.0 | [PyPI: pytest 9.2.0](https://pypi.org/project/pytest/9.2.0/), verified 2026-11-21 | Test runner | verified |
| Python | Hypothesis | 6.170.17 | [PyPI: Hypothesis 6.170.17](https://pypi.org/project/hypothesis/6.170.17/), verified 2026-11-21 | Property test dependency | verified |
| Python | Hatchling | 1.33.0 | [PyPI: Hatchling 1.33.0](https://pypi.org/project/hatchling/1.33.0/), verified 2026-11-21 | Python build backend | verified |
| Repository | pre-commit | 4.7.0 | [PyPI: pre-commit 4.7.0](https://pypi.org/project/pre-commit/4.7.0/), verified 2026-11-21 | Pre-commit hook framework | verified |
| Repository | detect-secrets | 1.5.0 | [PyPI: detect-secrets 1.5.0](https://pypi.org/project/detect-secrets/1.5.0/), verified 2026-11-21 | Local staged-file secret scanning | verified |
| Repository | pre-commit-hooks | 6.0.0 | [GitHub release: pre-commit-hooks v6.0.0](https://github.com/pre-commit/pre-commit-hooks/releases/tag/v6.0.0), verified 2026-11-21 | File hygiene hooks | verified |
| Infrastructure | PostgreSQL official image | 17.12 | [Docker Official Image: postgres 17.12](https://hub.docker.com/_/postgres), verified 2026-11-21 | Exact tag; architecture pins PostgreSQL 17 | verified |
| Infrastructure | Redis official image | 8.10.3 | [Docker Official Image: redis 8.10.3](https://hub.docker.com/_/redis), verified 2026-11-21 | Exact tag; architecture requires a rebuildable Redis materialization | verified |
| Infrastructure | Apache Kafka official image | 4.1.2 | [Docker | Apache Kafka](https://kafka.apache.org/41/getting-started/docker/), [Docker image manifest](https://hub.docker.com/r/apache/kafka), verified 2026-11-21 | Combined KRaft broker/controller; plaintext local listeners; replication factor 1 | verified |
| Infrastructure | MinIO source | RELEASE.2025-10-15T17-29-55Z | [MinIO source release](https://github.com/minio/minio/releases/tag/RELEASE.2025-10-15T17-29-55Z), [GNU AGPLv3 license](https://github.com/minio/minio/blob/master/LICENSE), verified 2026-11-21 | Vendor repository archived 2026-04-25; owner approved source build because Docker Hub tags are unavailable | verified |
| Infrastructure | MinIO MC source | RELEASE.2025-08-13T08-35-41Z | [MC source release](https://github.com/minio/mc/releases/tag/RELEASE.2025-08-13T08-35-41Z), verified 2026-11-21 | Source-built helper for idempotent bucket bootstrap and object round trips | verified |
| Infrastructure | Source-build Go base | 1.24-alpine3.23 | [Docker Official Image: golang](https://hub.docker.com/_/golang), verified 2026-11-21 | Exact tag used to compile the pinned MinIO and MC source releases | verified |
| Infrastructure | Source-build Alpine runtime | 3.23 | [Docker Official Image: alpine](https://hub.docker.com/_/alpine), verified 2026-11-21 | Exact runtime base for source-built MinIO and MC binaries | verified |
| Repository | GitHub Actions checkout | 7.0.1 (SHA `3d3c42e5aac5ba805825da76410c181273ba90b1`) | [GitHub release: actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1), verified 2026-11-21 | Workflow source checkout | verified |
| Repository | GitHub Actions setup-java | 6.3.0 (SHA `d1374f8ac74474200d16ef8ecee22c7ae7a51880`) | [GitHub release: actions/setup-java v6.3.0](https://github.com/actions/setup-java/releases/tag/v6.3.0), verified 2026-11-21 | Temurin 25 setup and Gradle cache | verified |
| Repository | GitHub Actions setup-python | 7.1.0 (SHA `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`) | [GitHub release: actions/setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0), verified 2026-11-21 | Python 3.13 setup | verified |
| Repository | GitHub Actions setup-node | 7.1.0 (SHA `949feb2413d6458794dcd2491c4babbbce0c15c1`) | [GitHub release: actions/setup-node v7.1.0](https://github.com/actions/setup-node/releases/tag/v7.1.0), verified 2026-11-21 | Node 26 setup and npm lockfile cache | verified |
| Repository | astral-sh/setup-uv | 9.0.0 (SHA `c771a70e6277c0a99b617c7a806ffedaca235ff9`) | [GitHub release: astral-sh/setup-uv v9.0.0](https://github.com/astral-sh/setup-uv/releases/tag/v9.0.0), verified 2026-11-21 | uv 0.13.9 setup and `uv.lock` cache | verified |
| Repository | gradle/actions setup-gradle | 6.4.1 (SHA `7296c772c13d12d9871528814b51fb2143c138ef`) | [GitHub release: gradle/actions v6.4.1](https://github.com/gradle/actions/releases/tag/v6.4.1), verified 2026-11-21 | Gradle wrapper validation and build cache | verified |
| Web | Node.js | 26.13.0 | [Node.js v26.13.0 release](https://nodejs.org/en/blog/release/v26.13.0), verified 2026-11-21 | Installed version; satisfies Vite, Vitest, jsdom and ESLint engine ranges | verified |
| Web | npm | 11.20.0 | [npm CLI documentation](https://docs.npmjs.com/cli/v11), official npm CLI release metadata, verified 2026-11-21 | Lockfile generated with npm; frozen installs use `npm ci` | verified |
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
| Web | Tailwind CSS / Vite integration | 4.3.5 | [npm tailwindcss 4.3.5](https://www.npmjs.com/package/tailwindcss/v/4.3.5), [npm @tailwindcss/vite 4.3.5](https://www.npmjs.com/package/@tailwindcss/vite/v/4.3.5), verified 2026-11-22 | CSS-variable token source; MIT licence | verified |
| Web | Lucide | 1.72.0 | [npm lucide-react 1.72.0](https://www.npmjs.com/package/lucide-react/v/1.72.0), [Lucide repository](https://github.com/lucide-icons/lucide), verified 2026-11-22 | Individual imports through the icon allow-list; ISC licence | verified |
| Web | IBM Plex Sans / IBM Plex Mono | 5.3.0 fontsource packages | [Fontsource IBM Plex Sans](https://fontsource.org/fonts/ibm-plex-sans), [Fontsource IBM Plex Mono](https://fontsource.org/fonts/ibm-plex-mono), verified 2026-11-22 | Latin WOFF2 assets served from `console/public/fonts`; SIL Open Font Licence 1.1 | verified |

## Licences

- IBM Plex Sans 400, 500, 600 Latin WOFF2 - Publisher: IBM / Fontsource - Licence: SIL Open Font Licence 1.1 - Source: [Fontsource package 5.3.0](https://www.npmjs.com/package/@fontsource/ibm-plex-sans/v/5.3.0) - Recorded: 2026-11-22
- IBM Plex Mono 400, 500 Latin WOFF2 - Publisher: IBM / Fontsource - Licence: SIL Open Font Licence 1.1 - Source: [Fontsource package 5.3.0](https://www.npmjs.com/package/@fontsource/ibm-plex-mono/v/5.3.0) - Recorded: 2026-11-22
- Lucide icons - Publisher: Lucide Contributors - Licence: ISC - Source: [lucide-react 1.72.0](https://www.npmjs.com/package/lucide-react/v/1.72.0) - Recorded: 2026-11-22
