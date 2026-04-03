# validate-fast / validate-full Command Catalog

> Per workspace and repo. All commands reference wrappers that exist on disk.
> validate-fast: correctness gate before closing any lane. Fast — no test execution.
> validate-full: full gate at consolidation. Includes tests and build artifacts.
> Commands assume CWD is the repo root unless a CWD note overrides this.

---

## Partner ecosystem

### Hub (projetos/ — non-git)

| Gate          | Command                                                              | Expectation |
|---------------|----------------------------------------------------------------------|-------------|
| validate-fast | `python tools/governance/verify-precedence.py`                       | exit 0      |
| validate-fast | `python tools/governance/audit-workspace-baseline.py --strict`       | exit 0      |
| validate-fast | `python tools/governance/audit-checkstyle-consistency.py --strict`   | exit 0      |
| validate-full | all validate-fast above                                              | all pass    |
| validate-full | `python tools/governance/audit-compliance.py`                        | = 100       |
| validate-full | `./tools/governance/scan-secrets.ps1`                                | no findings |

### Java child repos — Java 21 / Gradle
*Applies to: boleto-api, core-api-2.0, central-dados-api, conta-digital-api, dda-api,
external-logger-api, integrador, listener, notificador, orquestrador, relatorios-api,
webhook-api*

CWD: `projetos/<repo>/`

| Gate          | Command                                                                                        | Expectation      |
|---------------|------------------------------------------------------------------------------------------------|------------------|
| validate-fast | `../scripts/jdk-env.ps1`                                                                       | Java 21 selected |
| validate-fast | `../scripts/gradlew-jdk.ps1 . checkstyleMain checkstyleTest --no-daemon --console plain`       | exit 0           |
| validate-full | validate-fast + `../scripts/gradlew-jdk.ps1 . test --no-daemon --console plain`               | exit 0           |

Note: `gradlew-jdk.ps1` accepts `$ProjectPath` as first arg (`.` = current dir).

### core-api — Java 11 / Gradle (legacy)

CWD: `projetos/core-api/`

| Gate          | Command                                                                                        | Expectation      |
|---------------|------------------------------------------------------------------------------------------------|------------------|
| validate-fast | `../scripts/jdk-env.ps1`                                                                       | Java 11 selected |
| validate-fast | `../scripts/gradlew-jdk.ps1 . checkstyleMain checkstyleTest --no-daemon --console plain`       | exit 0           |
| validate-full | validate-fast + `../scripts/gradlew-jdk.ps1 . test --no-daemon --console plain`               | exit 0           |

### hash-api — Java 25 / Gradle

CWD: `projetos/hash-api/`

| Gate          | Command                                                                                        | Expectation      |
|---------------|------------------------------------------------------------------------------------------------|------------------|
| validate-fast | `../scripts/jdk-env.ps1`                                                                       | Java 25 selected |
| validate-fast | `../scripts/gradlew-jdk.ps1 . checkstyleMain checkstyleTest --no-daemon --console plain`       | exit 0           |
| validate-full | validate-fast + `../scripts/gradlew-jdk.ps1 . test --no-daemon --console plain`               | exit 0           |

### backoffice — React (Vite + vitest)

CWD: `projetos/backoffice/`

| Gate          | Command            | Expectation |
|---------------|--------------------|-------------|
| validate-fast | `npm run lint`     | exit 0      |
| validate-full | validate-fast + `npm test` | exit 0 |

Note: `npm test` runs `vitest --run` (non-watching by default). Do NOT pass `--watchAll=false` — that is a Jest flag incompatible with vitest.

---

## MeuAgendamento ecosystem

### Root (workspace root repo)

| Gate          | Command                                          | Expectation |
|---------------|--------------------------------------------------|-------------|
| validate-fast | `python tools/governance/verify-precedence.py`   | exit 0      |
| validate-fast | `./scripts/smoke-workspace.ps1`                  | no errors   |
| validate-full | validate-fast + each nested repo validate-full   | all pass    |
| validate-full | `python tools/governance/audit-compliance.py`    | = 100       |

### backend — Java 25 / Maven

CWD: `meuagendamento/backend/`

| Gate          | Command                                              | Expectation      |
|---------------|------------------------------------------------------|------------------|
| validate-fast | `../scripts/jdk-env.ps1`                             | Java 25 selected |
| validate-fast | `../scripts/mvn-jdk.ps1 . validate -q`              | exit 0           |
| validate-full | validate-fast + `../scripts/mvn-jdk.ps1 . test -q`  | exit 0           |

Note: `mvn-jdk.ps1` accepts `$ProjectPath` as first arg (`.` = current dir). It resolves `pom.xml` from this path and calls `jdk-env.ps1` internally.

### frontend — Angular 21 (ESLint + Karma/Jasmine)

CWD: `meuagendamento/frontend/`

| Gate          | Command                                                                | Expectation |
|---------------|------------------------------------------------------------------------|-------------|
| validate-fast | `npm run lint`                                                         | exit 0      |
| validate-full | validate-fast + `npm test -- --watch=false --browsers=ChromeHeadless`  | exit 0      |

Note: `npm run lint` runs `eslint "src/**/*.{ts,js}" --max-warnings=0 --cache --cache-location .eslintcache`.

### landingPage — Static HTML/CSS/JS (vitest)

CWD: `meuagendamento/landingPage/`

| Gate          | Command      | Expectation |
|---------------|--------------|-------------|
| validate-fast | —            | skip (no lint script available) |
| validate-full | `npm test`   | exit 0      |

Note: `npm test` runs `vitest run`. No lint script exists in this project — do not attempt `npm run lint`.

---

## Caradhras ecosystem

### Root (caradhras-poc/ — single repo with backend/ and frontend/ subfolders)

| Gate          | Command                                          | Expectation |
|---------------|--------------------------------------------------|-------------|
| validate-fast | `python tools/governance/verify-precedence.py`   | exit 0      |
| validate-full | validate-fast + backend validate-full + frontend validate-full | all pass |
| validate-full | `python tools/governance/audit-compliance.py`    | = 100       |

### backend — Java 25 / Maven

**CWD: `caradhras-poc/backend/`** (not repo root — required because `mvn-jdk.ps1` has no `$ProjectPath` param)

| Gate          | Command                                            | Expectation      |
|---------------|----------------------------------------------------|------------------|
| validate-fast | `../scripts/jdk-env.ps1`                           | Java 25 selected |
| validate-fast | `../scripts/mvn-jdk.ps1 validate -q`              | exit 0           |
| validate-full | validate-fast + `../scripts/mvn-jdk.ps1 test -q`  | exit 0           |

Note: Caradhras `mvn-jdk.ps1` does NOT accept `$ProjectPath` — it forwards all arguments directly to `mvn`. CWD must be the directory containing `pom.xml`.

### frontend — Angular 21

**CWD: `caradhras-poc/frontend/`**

| Gate          | Command                           | Expectation |
|---------------|-----------------------------------|-------------|
| validate-fast | —                                 | skip (no lint script available) |
| validate-full | `npm test -- --watch=false`       | exit 0      |

Note: No lint script exists. `npm test` runs `ng test`.

---

## Portfolio ecosystem

### Portfolio/

| Gate          | Command                                         | Expectation |
|---------------|-------------------------------------------------|-------------|
| validate-fast | `python tools/governance/verify-precedence.py`  | exit 0      |
| validate-fast | `node scripts/verify-metadata-sync.mjs`         | exit 0      |
| validate-full | validate-fast + `npm run build`                 | exit 0      |

Note: No `lint` or `test` scripts exist. `npm run build` includes `verify:metadata` internally (redundant but harmless).

---

## HelenSantosPortfolio ecosystem

### HelenSantosPortfolio/

| Gate          | Command                                         | Expectation |
|---------------|-------------------------------------------------|-------------|
| validate-fast | `python tools/governance/verify-precedence.py`  | exit 0      |
| validate-fast | `node scripts/verify-metadata-sync.mjs`         | exit 0      |
| validate-full | validate-fast + `npm run build`                 | exit 0      |

Note: No `lint` or `test` scripts exist. Same build pipeline as Portfolio.

---

## preflight-prompt

| Gate          | Command                                          | Expectation |
|---------------|--------------------------------------------------|-------------|
| validate-fast | `python tools/governance/verify-precedence.py`   | exit 0      |
| validate-fast | `python tools/governance/audit-compliance.py`    | = 100       |
| validate-full | same as validate-fast (no build artifact)        | —           |
