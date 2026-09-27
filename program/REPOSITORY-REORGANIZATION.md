# Prim Foundation repository reorganization

Status: proposed migration map, September 6, 2026. No repository is archived, renamed, deleted, or force-moved by this document.

**Canonical execution target:** [ORGANIZATION-TRANSFORMATION.md](ORGANIZATION-TRANSFORMATION.md).  
**Machine-readable inventory:** [reorganization.json](reorganization.json).  
**Observed quality/refactor work:** [QUALITY-REFACTOR-BACKLOG.md](QUALITY-REFACTOR-BACKLOG.md).

This file is the narrower repository-topology view. If it conflicts with the master transformation plan, the master plan wins.

## Goal

Organize repositories by **independent product/release responsibility**, not by Prim type, route, or temporary implementation experiment.

Target active top-level repositories should be few, durable, and understandable to a new maintainer without chat history.

## Current observed organization

Active repositories currently include:

- `primfoundation/prims`
- `primfoundation/prims-web`
- `primfoundation/prims-registry`
- `primfoundation/prim.workbook`
- `primfoundation/prims-desktop`
- `primfoundation/prims-browsers`
- `primfoundation/browsers-prims-sh`
- `primfoundation/prims-sso (archived: logins-prims-sh)`
- `primfoundation/prims-paste-desktop` — user-facing product is now **Primboard**
- `primfoundation/.github`

The current shape mixes five different concepts:

1. category/standards work;
2. individual profile experiments;
3. Foundation public cloud infrastructure;
4. end-user products;
5. route-specific deployment repositories.

That makes repo names leak historical implementation decisions into the architecture.

## Target model

### 1. `primfoundation/prims` — standards and definition source

Keep.

Owns:

- category specification and vocabulary;
- Foundation-maintained profile packages under `profiles/*`;
- conformance fixtures and compatibility baselines;
- profile publication contract;
- portable SDK/contracts/reference tooling that must remain useful without the hosted Foundation;
- Foundation program/roadmap and normative architectural decisions until governance chooses another home.

Does **not** own production website deployment, public runtime state, user accounts, popularity database, user Prim instances, or a repository per profile.

Migrate profile semantics from `prim.workbook` and suitable legacy Eidos `prim.*` incubators only after privacy/consumer/compatibility classification. Large profile+tool hybrids are split rather than copied wholesale.

### 2. `primfoundation/prims-hub` — public Foundation platform at `prims.sh`

Preferred target: preserve `prim-web` history by renaming/reworking it into `prims-hub` if history/security audit makes that safe. Otherwise create a clean Hub and explicitly import provenance.

Owns:

- `prims.sh` website and docs presentation;
- profile catalog/index projection;
- public API and remote MCP;
- publisher pages and later publisher/admin UI;
- popularity/ranking service;
- Cloudflare Worker/Static Assets config;
- D1 migrations and R2/Queue bindings only when needed;
- Hub-level audit/moderation;
- compatibility routes such as `registry.prims.sh`.

Does **not** own normative profile semantics, end-user Prim data, or desktop/browser product internals.

Suggested monorepo shape:

```text
prims-hub/
  apps/
    public/
    jobs/              # only when queues/schedules justify it
  packages/
    contracts/
    library/
    ranking/
    ui/
    testing/
  migrations/
  docs/architecture/
  docs/operations/
  .cloudflare/manifest.json
  .github/workflows/
  wrangler.jsonc
```

Migration sources:

- `prim-web` → website/history/base repository;
- `prims-registry` → registry compatibility/API behavior;
- hosted Library/MCP runtime pieces from `prim/services/library` → Hub runtime, while portable contracts/fixtures remain standards-owned;
- ranking implementation from the current Library alpha.

### 3. `primfoundation/prims-desktop` — desktop host product

Keep independent.

Its build/signing/TCC/release lifecycle is materially different from a Cloudflare service. It consumes `prim` standards and Hub discovery but remains offline-capable. Existing open PRs must be reconciled with actual Mac proof rather than discarded during refactor.

### 4. `primfoundation/prims-browsers` — browser sandbox product

Keep, and absorb product-specific cloud door infrastructure.

Move/merge:

- `browsers-prims-sh` → `prims-browsers/cloud/gateway` (or equivalent app boundary);
- `prims-sso` (ex `logins-prims-sh`) → `prims-browsers/cloud/login` while the login remains browser-specific.

Reason: those Workers exist to operate Prims Browsers; route-specific repositories create deployment sprawl and duplicate assets/session code.

Do not reuse Browsers identity as Foundation publisher/admin identity without a separate explicit decision.

### 5. `primfoundation/primboard` — private encrypted capture/staging product

Current source repo: `primfoundation/prims-paste-desktop`. User-facing display name at observed commit `25d2641` is **Primboard**.

Keep as an independent signed macOS product and stabilize before repository rename.

Planned repository rename: `prims-paste-desktop` → `primboard` after clone/link/release/CI dependency audit.

**Do not cosmetically rename compatibility-sensitive runtime identities.** Preserve for now:

- bundle ID `sh.prims.paste`;
- executable `PrimsPaste`;
- CLI `prims-paste`;
- store root `~/.prims-paste/`;
- Keychain service `sh.prims.paste`;
- serialized notebook/sticky IDs and old-store compatibility.

Primboard's target role is the private front porch of the ecosystem: arbitrary material lands as an encrypted sticky; later **Convert to Prim…** discovers a pinned definition from Hub/Library and creates the durable Prim locally without uploading the private payload.

Before repo rename, complete the security/store/refactor gates in the master plan: encrypted sensitive index metadata, interprocess app/CLI locking, crash consistency, migrations/backup/recovery, Touch ID/Keychain threat model, removal of product-backlog seeding from normal user notebooks, generic Prim conversion, and signed-Mac acceptance.

### 6. `primfoundation/.github` — organization defaults

Keep and expand carefully:

- organization README;
- contribution/security/code-of-conduct defaults;
- issue/PR templates;
- shared reusable workflows where behavior is truly organization-wide;
- repository lifecycle/successor conventions.

Do not hide product-specific deployment logic here.

## Repositories to consolidate/archive after cutover

### `prims-registry`

Merge runtime contract/tests into `prims-hub`. Preserve `registry.prims.sh` as compatibility route if useful. Archive only after client inventory, parity, release evidence, rollback, and successor notice.

### `prim.workbook`

Move normative workbook/worksheet/measure/metric profile assets under `prim/profiles/workbook` after history/privacy review. Assign viewer code to the product surface whose lifecycle actually owns it. Open PR #1 explicitly warns about customer/private history; removing current files is not proof git history is safe.

### `browsers-prims-sh`

Merge gateway into `prims-browsers`, preserve live domain/session/container behavior, then archive with successor notice.

### `prims-sso` (ex `logins-prims-sh`)

Merge into `prims-browsers` unless its identity role is deliberately broadened later. Preserve Apple callback and shared-cookie behavior before archive.

### legacy Eidos `prim.*` repositories

Treat as incubators to classify, not as permanent one-profile-per-repo architecture. Profile-only definitions migrate into `prim`; profile+tool hybrids split responsibilities; private/customer-derived repos get history/privacy review before any public move. Archived historical repos remain archived.

## `prim-web` decision

Preferred approach:

1. audit repository for secrets/private-only assets/obsolete demos/deployment assumptions;
2. preserve useful public history;
3. rename `prim-web` to `prims-hub` if operationally safe;
4. replace Railway/Pages ambiguity with Cloudflare Workers + Static Assets;
5. add Hub apps/packages incrementally;
6. supersede old Pages PR only after the new preview/cutover is proven.

Alternative: if history is too contaminated, create a clean `prims-hub`, import useful history with explicit provenance, and archive `prim-web`. Never copy files without lineage.

## Why not one giant Foundation monorepo?

The standards library and public Hub should not share a deployment lifecycle with signed macOS apps and browser containers.

The consolidation unit is **independent product responsibility**, not minimum repository count.

Therefore:

- many profiles in one standards repo: yes;
- multiple routes of one cloud Hub in one platform repo: yes;
- browser-specific login/gateway with the browser product: yes;
- Primboard as its own signed/private local product: yes;
- Desktop + cloud Hub combined merely to reduce count: no.

## Target organization after migration

Likely active set:

```text
primfoundation/
  .github
  prim
  prims-hub
  prims-desktop
  primboard
  prims-browsers
```

Potential future products earn repositories by independent lifecycle, not by being a Prim type. Archived compatibility/history repos remain discoverable with successor notices rather than being deleted.

## Migration rules

Every repository consolidation follows these rules:

1. inventory consumers, deployments, domains, secret **names**, branches, open PRs and release evidence;
2. preserve source history or document exact imported commit lineage;
3. distinguish brand/repo/public-route/runtime-security identity changes;
4. move tests before moving production traffic;
5. add successor compatibility paths;
6. verify real production behavior;
7. update docs/links;
8. freeze old repo;
9. archive only after rollback window and real-use verification;
10. never force-push or delete history as cleanup.

Repo movement does not change profile identity.

## Relationship to AIC Hub

Borrow:

- monorepo around one control-plane product;
- explicit app/package boundaries;
- shared validated contracts;
- machine-readable Hub manifest;
- architecture docs that state ownership boundaries;
- one deploy model for related services;
- catalog + MCP as two surfaces over one control plane;
- fail-closed readiness and auditable deployment evidence.

Do not copy AIC Hub's enterprise identity/data model: Prim Foundation is anonymous-read-first, decentralized, and should not absorb user records.

## Immediate execution order

The list below is the original September 6 sequence. Its early implementation
steps have since shipped. Use [DELIVERY-95.md](DELIVERY-95.md), `plan.json` and
`HANDOFF.md` for the September 11 execution queue and Fleet/source findings;
retain the migration gates and topology in this document.

1. reconcile current stacked `prim` PRs #5–#8 and preserve their evidence;
2. finish inventory of current Foundation + Eidos incubators and open PRs;
3. audit `prim-web` and build `prims-hub` Cloudflare preview without production cutover;
4. stabilize Primboard store/security/concurrency while preserving runtime identities;
5. move Library/MCP into the Hub adapter behind identical conformance tests;
6. migrate website/catalog/registry compatibility and cut over only after preview acceptance;
7. consolidate Browsers route repos;
8. refactor Desktop against generic profile contracts while preserving Mac proof gates;
9. migrate profile incubators one by one;
10. archive only after each successor is demonstrably better and reversible.