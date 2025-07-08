# OpenAPI Testing Cheat Sheet

## Schemathesis Commands

Up-to-date CLI commands for testing OpenAPI (YAML or JSON) files with Schemathesis.

| Scenario | Command | Why / what it does |
|----------|---------|-------------------|
| Smoke-test a public URL | `st run https://example.schemathesis.io/openapi.json` | Downloads the schema from the given URL and immediately starts all test phases (examples + coverage + fuzzing + stateful). |
| Local spec + live server | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1` | When the schema is on disk you must tell Schemathesis where the running API lives via --url. |
| Only run the quick "examples" phase | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 --phases=examples` | Skips coverage / fuzzing / stateful tests—handy for very fast CI smoke checks. |
| Throw more CPU at it | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 -w auto` | -w / --workers sets concurrency; auto picks an optimal value for your machine. |
| Target just one operation | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 --include-path=/search --include-method=GET` | Limits test generation to GET /search; combines well with --exclude-deprecated. |
| Add auth / custom headers | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 -H "Cookie: AL_BALANCE-S=$TOKEN" -H "User-Agent: schemathesis"` | Any curl-style header becomes part of every request. |
| Fail fast after 3 problems | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 --max-failures 3` | Stops the run early and exits non-zero—perfect for CI. |
| Save a nice HTML report | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 --report html --report-dir reports/` | Generates index.html plus static assets under reports/ for later inspection. |
| JUnit output for Jenkins / GitLab | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 --report-junit-path schemathesis.xml` | Produces a CI-friendly JUnit-style XML file. |
| Deterministic re-runs | `st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 --seed 1234` | Fixes the Hypothesis seed so identical cases are generated every time. |

### CLI aliases & install notes
- `st` is the standard entry-point (installed via `pip install schemathesis`)
- You'll also see docs use `schemathesis run` (fully-qualified) or `uvx schemathesis run` when running via the UV package manager
- All three invocations are identical

## Dredd Commands

Day-to-day Dredd commands for the most common testing tasks.

> **Heads-up on OpenAPI 3**: Dredd's OAS 3 adapter is still branded experimental — it works for most "happy-path" cases but can miss edge-case validations. If you hit parser errors, convert the spec first (`npx swagger2openapi -y zer_search_openapi.yaml > zer_search_oas2.yaml`) or stay with Schemathesis for fuzzing.

### 1. One-liner smoke test
```bash
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1
```
Runs every transaction in the file against the live server and prints a green/red summary.

### 2. Generate (and reuse) a dredd.yml
```bash
dredd init      # interactive wizard
dredd           # afterwards you can just run this in CI
```
The wizard scaffolds a config file, so future runs need no long CLI flags.

### 3. Add auth or any custom headers
```bash
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1 \
      -h "Cookie: AL_BALANCE-S=$TOKEN" \
      -h "User-Agent: dredd"
```
`-h/--header` may be repeated for each header you need.

### 4. Limit the scope (faster local runs)
```bash
# Only the GET /search operation
dredd zer_search_openapi.yaml https://zer.search_openapi.yaml \
      --path=/search --method=GET
```
`--path` filters by URI template, `--method` by verb. You can stack them or use `--only "<transaction name>"` for pinpoint tests.

### 5. Run with hooks (fixtures, auth tokens, DB cleanup)
```bash
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1 \
      --hookfiles=hooks/*.js --language=nodejs
```
Any glob is allowed; multiple `--hookfiles` are executed alphabetically. Supported hook languages include Node.js, Python, Ruby, Go, Rust and more.

### 6. Dry-run / lint only (compile transactions, don't hit the API)
```bash
dredd zer_search_openapi.yaml --dry-run
```
Great for catching spec typos quickly.

### 7. Produce machine-readable reports
```bash
# JUnit-style XML (works with Jenkins, GitLab, etc.)
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1 \
      --reporter xunit --output dredd-report.xml

# Pretty self-contained HTML
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1 \
      --reporter html --output reports/index.html
```
`--reporter` can be repeated (xunit, markdown, html, dot, nyan, apiary) and each needs its own `--output`.

### 8. Spin up and tear down the server automatically
```bash
dredd zer_search_openapi.yaml http://127.0.0.1:3000 \
      --server "npm run dev" --server-wait 5
```
Dredd launches the command, waits the given seconds, runs all tests, then kills the process.

### 9. Run Dredd from a Docker image (zero local install)
```bash
docker run --rm -it -v $(pwd):/data \
  dredd/dredd:latest \
  dredd /data/zer_search_openapi.yaml https://zer.bzst.de/api/v1
```

These commands cover 95% of real-world workflows: quick local checks, CI regression gates, and rich reports you can archive or publish. Use them as templates and mix flags as needed—the CLI options can be combined freely.

## Quick Comparison

| Tool | Best For | Testing Approach |
|------|----------|------------------|
| **Schemathesis** | Finding bugs, security issues, edge cases | Property-based fuzzing, generates random test data |
| **Dredd** | Contract validation, API compliance | Example-based testing, validates against spec |

## Example ZER API Test Commands

```bash
# Quick Schemathesis fuzzing
st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 --max-failures 3

# Thorough Schemathesis test with report
st run zer_search_openapi.yaml --url https://zer.bzst.de/api/v1 \
  --checks all --workers auto \
  --report html --report-dir test-results/

# Quick Dredd contract test
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1

# Install Dredd if needed
npm install -g dredd
```

## Swagger UI Documentation Preview

Preview your OpenAPI documentation with the classic Swagger UI:

```bash
# Using Docker (recommended)
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/api/zer_search_openapi.yaml \
  -v $(pwd)/zer_search_openapi.yaml:/api/zer_search_openapi.yaml \
  swaggerapi/swagger-ui

# Or use the convenience script
./swagger-ui.sh

# Stop Swagger UI
docker stop swagger-ui

# Alternative: Using Python HTTP server with swagger-ui-dist
npm install -g swagger-ui-dist
# Then serve with Python
python -m http.server 8080
```

### Key Features:
- Interactive API testing with "Try it out" button
- Classic three-panel layout
- Industry standard for API documentation
- No auto-reload (restart container for changes)

## Redocly API Documentation Preview (Alternative)

Preview with Redocly's modern UI:

```bash
# Preview documentation (runs on http://127.0.0.1:8080)
npx @redocly/cli@latest preview-docs zer_search_openapi.yaml

# With custom port
npx @redocly/cli@latest preview-docs zer_search_openapi.yaml --port 3000
```

### Key Features:
- Live reload on file changes
- Clean two-pane documentation UI
- Modern design focused on readability