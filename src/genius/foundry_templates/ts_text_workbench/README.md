# __PROJECT__

Real, local full-stack TypeScript text workbench: Node HTTP API, Unicode
analysis, and an interactive browser interface. The original objective is
retained in `mission.json`.

## Run and verify

Requires Node >=22.16.0. No runtime npm dependencies.

```sh
npm start
# Open http://127.0.0.1:3000
npm test
npm install --ignore-scripts --no-audit --no-fund
npm run typecheck
npm run build
npm run serve
```

`PORT` selects a local port. The server binds only to `127.0.0.1`: it is
not a public deployment. `GET /health` checks readiness, `POST /api/analyze`
accepts JSON `{ "text": "one one two" }`, and `GET /` is the UI.

Developer dependencies are exact-pinned. The template does not yet include
a committed npm lockfile or production deployment.
`GENERATED_UNVERIFIED` is not a claim of test success or objective completion.
