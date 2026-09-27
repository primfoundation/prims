# Prim Foundation Cloudflare platform plan

Status: proposed implementation architecture, September 6, 2026. This plan extends the existing Foundation program; it does not mark deployment, migration, governance, or real-user gates complete.

## Objective

Turn `prims.sh` into the Foundation's coherent public control plane for Prim discovery and distribution while keeping actual Prim instances with their owners.

The platform should make this path obvious to humans and agents:

> discover a Prim definition → inspect exact version and publisher → obtain creation kit → create locally → validate locally → keep the work

The Hub owns discovery, routing, public metadata, publisher relationships, popularity, compatibility reports, and operational audit. A Prim definition owns its semantics. A user or organization owns its actual Prim instances. The Hub must not become the universal private data store or agent runtime.

## Why Cloudflare

The existing `prims.sh` domain and several Prim services already target the same Cloudflare account. `prims-registry` is already a Worker with a `registry.prims.sh` custom domain. `logins-prims-sh` and `browsers-prims-sh` are also Workers. A prior `prim-web` PR prepared the website for Cloudflare Pages.

Cloudflare now supports Worker-hosted static assets and full-stack applications in one deployment. For the rebuilt Foundation Hub, prefer Workers + Static Assets over creating a separate Pages project plus separate API Worker unless a later constraint requires separation.

Cloudflare platform components proposed here:

- Workers + Static Assets: public site, catalog, JSON API, remote MCP, well-known metadata.
- D1: derivative public index state, publishers, stars/adoption aggregates, moderation/audit records. D1 is not the canonical definition source.
- R2: immutable definition bundles and downloadable distribution artifacts keyed by digest when repository-bundled assets stop being sufficient.
- Queues: later, for external-source indexing and authenticated adoption-event processing when those jobs need asynchronous isolation.
- Workers Builds + GitHub: previews and deploys from the platform repository.
- Cloudflare Access: maintainer/admin surfaces and preview protection where appropriate.

Do not provision D1/R2/Queues merely because they exist. The first production cut can ship with the compiled public definition snapshot and add durable services only when the corresponding feature activates.

## Target product surface

Information density should increase as users move inward, similar to the useful AIC Hub pattern.

- `/` — quiet Foundation home: what Prims are, why they matter, search entry.
- `/prims` — searchable catalog with Popular / Trending / New / Official filters.
- `/prims/:publisher/:name` — one definition: purpose, maturity, versions, source, creation support, interoperability, popularity, security/conformance status.
- `/prims/:publisher/:name/:version` — exact immutable version and digest.
- `/publishers/:publisher` — publisher identity and verification state.
- `/docs` — category, authoring, publishing, MCP, migration, conformance.
- `/collections` — later: useful compositions of profiles/tools without inventing a new type.
- `/admin/*` — maintainers only; never required for public read-only use.
- `/api/v1/*` — versioned JSON API.
- `/mcp` — Streamable HTTP MCP endpoint on the Hub worker.
- `/.well-known/prim-library.json` — machine discovery.
- `/healthz` — operational health without leaking private data.

Recommended public domains:

- `prims.sh` — canonical human site and API routes.
- `mcp.prims.sh/mcp` — canonical remote MCP alias to the same deployed service or route.
- `registry.prims.sh` — compatibility alias during migration; later a documented API alias/redirect.
- `www.prims.sh` — redirect to apex.
- `prim.eidosagi.com` — legacy redirect after successful cutover.

Avoid creating a subdomain per Prim profile.

## Public MCP contract

Keep the anonymous public MCP read-only. It should distribute definitions, not collect user records.

Initial tools:

- `prim_search`
- `prim_get_definition`
- `prim_list_versions`
- `prim_get_resource`
- `prim_get_creation_kit`
- `prim_rankings`

Requirements:

- Streamable HTTP at `/mcp`.
- Current MCP protocol plus intentional compatibility policy for supported older Streamable HTTP clients.
- Exact version and full definition digest in every creation path.
- No arbitrary URL fetches or execution of profile-provided code.
- No private Prim content parameter on public tools.
- No public anonymous `vote`, `publish`, or `validate_my_private_record` tool.
- Retrieved definition text is data, not host-level instructions.

If authenticated publisher/admin MCP is later useful, expose it as a separate authorization boundary rather than adding mutation tools to the anonymous endpoint.

## Definition publication model

GitHub repository location is not identity. A repository can contain many profiles; independent publishers can host profiles elsewhere.

The Hub indexes publishable profile packages. For each version it stores/serves:

- profile identity (`namespace/name` while the namespace design remains provisional),
- semantic version,
- maturity,
- publisher identity and verification state,
- source location and immutable source revision,
- full definition digest,
- declared resources,
- creation-kit support,
- compatibility/conformance reports,
- moderation/retraction state.

Foundation-official definitions in `primfoundation/prim/profiles/*` are one source, not the architecture's special case.

Initial publication path should remain PR/review based. Later external publishing can add a source record through reviewed registration and automated indexing. The indexer must pin immutable source revisions and retain the original fetched bundle in R2 before promoting a version to the public catalog.

D1 is a query/index projection. The authoritative published package remains the immutable source/bundle plus its digest.

## Popularity model

Popularity is useful discovery, not quality certification.

Expose separate dimensions:

- `Popular`: longer-term active stars + distinct recent adoption.
- `Trending`: recent adoption momentum with a capped growth multiplier.
- `New`: release date.
- `Official`: Foundation stewardship status.
- `Verified publisher`: identity state.
- `Conformance`: version-specific tests.
- `Security review`: independent status.

Never merge those into a single trust score.

The initial catalog may legitimately show no popularity data. Do not seed fake votes.

When activated:

- user stars require authenticated, revocable identity;
- adoption telemetry is explicit opt-in and distinct-user deduplicated;
- raw searches/definition reads do not count as adoption;
- events enter through authenticated collector services, preferably via Queue;
- D1 stores minimal actor pseudonyms/aggregates, not private Prim content;
- small cohorts remain suppressed;
- score policy is versioned and published;
- abuse review and anti-Sybil controls are explicit operations, not assumed solved by OAuth.

## Cloudflare data layout

### D1 — `prims-hub`

Proposed tables, introduced only when needed:

- `publishers`
- `profile_sources`
- `profile_versions`
- `profile_resources`
- `stars`
- `adoption_daily`
- `ranking_snapshots`
- `conformance_results`
- `moderation_actions`
- `audit_events`
- `index_jobs`

No table for users' actual Prim contents.

All schema changes live as ordered migrations in Git. Production migration status is auditable. Roll-forward is primary; destructive migration requires explicit review and backups/restore evidence.

### R2 — `prims-definitions`

Use immutable digest-addressed keys, for example:

`definitions/sha256/<digest>/bundle.zip`

Additional optional prefixes:

- `releases/` — published Hub/client artifacts
- `conformance/` — retained result bundles
- `publisher-assets/` — public icons/screenshots after content review

No secrets or private Prims.

### Queues

Add only when justified:

- `profile-index` — external profile source refresh / verification.
- `popularity-events` — authenticated consented adoption/star ingestion.

Workers consuming these queues must be idempotent and record durable receipts before acknowledging work.

## Cloudflare Worker topology

Prefer one repository and a small number of deployables.

Suggested monorepo deployables:

- `apps/public` — Worker + static assets; serves website, API, public MCP, well-known endpoints, health, and public read-only catalog.
- `apps/jobs` — queue/scheduled worker added only when asynchronous indexing/ranking is activated.

Do not split website, registry, MCP, auth, and rankings into separate repositories merely because they have different routes.

Shared packages:

- `packages/contracts` — validated profile, catalog, MCP, ranking and API contracts.
- `packages/library` — immutable definition resolution/search and creation-kit projection.
- `packages/ranking` — transparent scoring policy.
- `packages/ui` — small Foundation design system and accessible catalog components.
- `packages/testing` — conformance fixtures and Cloudflare contract helpers.

Infrastructure/config:

- `wrangler.jsonc` / per-app Wrangler config in Git.
- `migrations/` for D1.
- `.cloudflare/manifest.json` (or equivalent) describing domains, bindings, Worker names and expected public surfaces without secret values.
- `.github/workflows/verify.yml` for repository verification.
- Workers Builds for preview/prod deploys, or GitHub Actions deployment if we need stronger approval gates. Choose one deploy authority, not both.

## CI/CD and environments

No permanent staging service is required initially. Use:

1. local `wrangler dev` with local bindings,
2. per-PR preview versions/URLs,
3. production from `main` after required checks.

PR checks:

- lint/typecheck/unit tests,
- profile/catalog compilation drift,
- MCP protocol tests,
- API contract tests,
- D1 migration dry-run/local application,
- static build,
- security boundary tests,
- broken-link and redirect checks,
- accessibility smoke tests,
- package build/install test for local MCP client artifact,
- inherited `prim` conformance fixtures where relevant.

Cloudflare preview URLs should be protected with Access if they expose unpublished administrative work.

Production deploy:

- deploy one immutable Worker version,
- smoke `/healthz`, `/`, `/api/v1/prims`, `/.well-known/prim-library.json`, and MCP initialize/search,
- record deployment ID/commit/digests,
- retain rollback instructions and previous known-good version.

## Secrets and identity

The public library does not need user authentication for reads.

Keep secrets entirely in Cloudflare/GitHub secret stores. The repository contains only secret names, purpose, holder, rotation owner, and whether required.

Initial maintainer/admin access can be protected by Cloudflare Access, avoiding another bespoke login system. Publisher self-service and public stars can later use a dedicated identity flow when the requirements justify it.

Do not reuse the `prims_session` browser-product cookie as Foundation publisher identity. Browser-product login and Foundation publishing are different trust domains.

## Website migration

`prim-web` currently contains years of demos/experiments and a Railway deploy workflow; an open PR prepared Pages migration. The rebuilt Hub should not blindly carry every historical demo onto the main information architecture.

Migration steps:

1. inventory every current route and classify: canonical / compatibility / demo / product-specific / obsolete;
2. preserve valuable demos under `/labs` or their owning product repository;
3. move canonical Foundation content into the Hub information architecture;
4. implement explicit redirects for externally linked legacy paths;
5. cut the canonical site to Workers Static Assets + Worker routing;
6. verify TLS, caching, headers, redirects, sitemap, robots, canonical tags and 404 behavior;
7. only then retire Railway/Pages deploy paths.

## Security and privacy

Minimum production controls:

- Host/Origin validation for MCP and admin/browser mutation paths.
- request/response size limits and pagination.
- edge rate limits for MCP/API; per-route abuse policy.
- no execution of profile-supplied code in public Worker.
- no remote schema references in public validation path unless explicitly sandboxed and reviewed.
- CSP, Referrer-Policy, HSTS, X-Content-Type-Options and safe asset handling.
- D1 prepared statements only.
- R2 objects immutable by digest after publication.
- explicit publisher/retraction moderation path.
- audit trail for admin publication changes.
- no private Prim content in logs/analytics.
- separate operational telemetry from popularity metrics.

## Observability and operations

Track only service health/useful aggregate operations initially:

- request/error/latency by route class,
- MCP initialize/tool error counts,
- index freshness,
- D1/R2/Queue failures,
- ranking snapshot age,
- deployment version/commit,
- abuse/rate-limit events.

Do not use raw user search queries as popularity signals. If search analytics are ever retained, create an explicit privacy policy first.

Operational runbooks:

- deploy/rollback,
- D1 migration/recovery,
- R2 integrity verification,
- publisher retraction/emergency hide,
- lost/compromised maintainer credential,
- popularity abuse investigation,
- Cloudflare account/zone transfer,
- GitHub outage / Hub serving from last known-good snapshot.

## Cloudflare account boundary

Today the existing Prim Cloudflare services reference the Eidos AGI account. That is operationally convenient, but Foundation architecture must not depend on the account identifier.

Near-term reasonable choice: continue in Cloudflare under the existing controlled account with a dedicated `prims.sh` zone/resources and narrowly scoped deploy token. Do not hardcode account IDs into portable application logic.

Long-term governance choice: if/when Prim Foundation gets its own Cloudflare account, transfer the zone/resources without changing profile identities, URLs where avoidable, or published definition semantics.

## Execution phases

### P0 — inventory and freeze

- map current Prim Foundation repos, routes, domains, Workers/Pages/Railway deploy paths;
- capture existing Cloudflare bindings/config without secret values;
- classify every repo as standards, platform, product, compatibility, or archive candidate;
- preserve redirects and consumer dependencies.

### P1 — create the Hub monorepo shape

- rename/rework `prim-web` into the Hub repository or create the target repo and preserve history;
- add `apps/public`, `packages/contracts`, `packages/library`, `packages/ui`, `docs/architecture`, `.cloudflare`;
- move public website source and the Library/MCP runtime into this structure without switching production yet;
- compile Foundation definitions from a pinned `prim` commit.

### P2 — preview the unified Worker

- Workers Static Assets + public Worker routes;
- MCP/API/human catalog from one snapshot;
- PR preview deploys and smoke tests;
- legacy route compatibility tests.

### P3 — production cutover

- bind `prims.sh`, `mcp.prims.sh`, `registry.prims.sh` compatibility route;
- production smoke and external MCP connection;
- redirect old Railway/Eidos web origins;
- retain previous deployment for rollback.

### P4 — persistent catalog and popularity

- D1 migrations;
- profile source/version indexing;
- authenticated stars;
- optional adoption signals via Queue;
- ranking pages and policy transparency;
- moderation/audit.

### P5 — decentralized publishing

- external publisher source registration;
- immutable source revision fetch and R2 retention;
- publisher verification;
- automated re-index on approved releases;
- retraction/transfer/abandonment flows.

### P6 — ecosystem hardening

- security review;
- accessibility/user tests;
- recovery drills;
- client compatibility matrix;
- package-index publication where appropriate;
- public governance/maintenance policy.

## Completion criteria for a materially better online Foundation

The platform is not considered "online" merely because `prims.sh` renders.

A meaningful first launch requires:

- canonical website on Cloudflare Worker/static assets,
- searchable catalog with exact versions/digests,
- working remote MCP from an external client,
- local creation kit flow for at least Research/Person/Decision,
- transparent no-data or real popularity state,
- compatibility redirect for the old registry route,
- repository-defined Cloudflare config and deployment checks,
- rollback and health monitoring,
- no private Prim data stored by default,
- clear docs for a human or agent to discover and create a Prim without founder intervention.