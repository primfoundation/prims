# Prim Foundation organization transformation

Status: execution target, September 6, 2026. This document defines the desired organization and migration gates. It does **not** authorize destructive repository operations, production DNS changes, secret movement, or silent format reinterpretation.

## Outcome

Transform Prim Foundation from a collection of strong experiments into a small, coherent standards-and-products organization with explicit ownership boundaries, one public Cloudflare control plane, durable compatibility, and products that can evolve independently.

The target should be understandable to a new maintainer or capable agent without reconstructing old chats.

The end-state is not “fewest repositories.” It is **one repository per materially independent standards/product/release responsibility**.

Likely durable active set:

```text
primfoundation/
  .github
  prim
  prims-hub
  prims-desktop
  primboard
  prims-browsers
```

Additional products earn a repository only when they have a genuinely independent lifecycle. Historical repositories remain available as archived compatibility/history records rather than being deleted.

## Non-negotiable architectural boundaries

1. **`prim` owns standards and definitions.** It is not the website, hosted registry database, or user cloud store.
2. **`prims-hub` owns discovery and Foundation public infrastructure.** It serves the website, catalog, public API, remote MCP, publisher metadata, ranking, compatibility routes, moderation/audit, and Cloudflare operations.
3. **Profile packages own semantics.** A repository location never becomes semantic identity.
4. **Users own Prim instances.** The Foundation must not require private research, finances, secrets, contacts, or other personal records to transit the public library.
5. **Products own their local workflows.** Desktop, Primboard, and Browsers consume standards/Hub contracts but retain their own release and security boundaries.
6. **Popularity, official status, conformance, security review, and factual truth remain separate dimensions.**
7. **A cosmetic rename never justifies breaking stable operating identities.** Bundle IDs, Keychain services, stores, file formats, URLs, and CLI contracts are changed only through explicit migration.
8. **No archive before replacement proof.** Every retirement needs a successor, compatibility path, tests, rollback window, and real-use evidence.

## Program structure

The transformation runs in nine waves. Several can overlap in implementation, but the gates cannot be skipped.

### Wave 0 — Freeze reality and stop accidental sprawl

Goal: create one trusted inventory before moving anything.

Actions:

- preserve every current Prim Foundation repository, default branch, open PR, deployment domain, release path, secret **name** (never value), and known external consumer;
- record current Eidos AGI `prim.*` incubators and classify each as profile-only, profile+tool hybrid, product, compatibility history, or unrelated;
- stop creating route-specific repositories and one-profile-per-repo repositories by default;
- add a repository lifecycle field: `active`, `migrating`, `compatibility`, `candidate-archive`, `archived`;
- create a machine-readable migration ledger (`program/reorganization.json`);
- reconcile the open stacked Foundation PRs #5–#8 before allowing another competing top-level architecture branch;
- preserve open product PRs in `prims-desktop`, `prim.workbook`, `prim-web`, and `prims-registry`; none may vanish during consolidation.

Completion: a replacement maintainer can identify the intended destination and blockers for every current Foundation repo and every discovered legacy Prim incubator.

### Wave 1 — Make `prim` the definitive standards home

Goal: remove repository topology from the definition model.

Actions:

- finish the repository-independent profile package contract and conformance tooling;
- define permanent publisher/profile/version identity and immutable distribution pins;
- make `profiles/*` the normal home for Foundation-maintained definitions;
- migrate definition semantics, fixtures, validators, migrations, and compatibility notes from profile-only repos into `prim` one at a time;
- split profile+tool hybrids: only normative semantics enter `prim`; substantial executables/services remain independent tools/products when justified;
- preserve original source commit IDs and compatibility tests in every migration;
- keep legacy aliases descriptive until explicit adapters exist;
- never claim a copied schema is a lossless semantic migration merely because it validates.

Priority definition migrations:

1. workbook family after private/customer-history review;
2. Research/ORF through the existing frozen compatibility lane;
3. other small profile-only Eidos incubators after classification;
4. large hybrids such as Docket/video/scene only after separating definition from tool/product behavior.

Completion: Foundation can publish many profiles from `prim` or external sources without requiring one repository per type, and existing legacy files remain readable with honest compatibility status.

### Wave 2 — Build `prims-hub` as the single public Foundation control plane

Goal: replace website/registry/MCP fragmentation with one Cloudflare-native product.

Preferred migration: audit `prim-web`; if safe, preserve its history and rename/rework it into `prims-hub`. If its history is too contaminated by obsolete/private experiments, create a clean Hub repo and import useful history explicitly rather than copying without provenance.

Target responsibilities:

- `prims.sh` website and documentation presentation;
- `/prims` marketplace/catalog and definition detail pages;
- `/api/v1/*` public machine API;
- `/mcp` public read-only remote MCP;
- `/.well-known/prim-library.json` discovery;
- publisher pages and later protected publisher/admin UI;
- Popular/Trending ranking and policy display;
- `registry.prims.sh` compatibility surface;
- audit/moderation and deployment health.

Cloudflare shape:

- Workers + Static Assets as the default full-stack runtime;
- no D1 until mutable publisher/ranking/moderation state needs SQL;
- no R2 until immutable bundles/artifacts outgrow Worker-bundled snapshots;
- no Queues until external indexing or signed popularity events become asynchronous work;
- no Durable Objects unless coordination semantics actually require them;
- public read paths cache aggressively and remain anonymous when possible.

Repository shape:

```text
prims-hub/
  apps/public/
  apps/jobs/             # only when asynchronous jobs exist
  packages/contracts/
  packages/library/
  packages/ranking/
  packages/ui/
  packages/testing/
  migrations/
  docs/architecture/
  docs/operations/
  .cloudflare/manifest.json
  .github/workflows/
  wrangler.jsonc
```

Borrow from AIC Hub: explicit product boundary, app/package separation, machine-readable manifest, shared validated contracts, one deploy model, fail-closed readiness, auditable releases. Do **not** copy its enterprise identity model or absorb user domain data.

Completion: a preview deployment proves website + API + MCP + definition detail from one versioned library, with identical definition digests across all surfaces.

### Wave 3 — Cut over public infrastructure and retire route repos

Goal: make `prims.sh` coherent without a flag day.

Actions:

- run old and new public surfaces in parallel;
- verify redirects, docs, static assets, demos still intentionally supported, API responses, MCP protocol behavior, security headers, accessibility, mobile layout, and cache semantics;
- cut `prims.sh` to the unified Worker only after preview acceptance;
- expose canonical `mcp.prims.sh/mcp` alias if desired while `/mcp` remains valid;
- absorb `prims-registry` behavior into Hub and preserve `registry.prims.sh` as compatibility routing;
- close/supersede the old `prim-web` Pages/Railway migration PR only after the new origin is proven;
- retain old Worker/Pages deployment IDs and rollback instructions through the cutover window.

Completion: production health, API smoke, MCP initialize/search/get-kit, website smoke, rollback, and independent external-client acceptance all pass.

### Wave 4 — Turn Primboard into a first-class product

Goal: preserve the excellent idea while removing prototype-era coupling and security ambiguity.

Product identity:

- user-facing product: **Primboard**;
- planned repository slug after audit: `primfoundation/primboard` (preferred) or `primboard-desktop` if needed for naming consistency;
- preserve current runtime identities until a separately designed migration says otherwise.

Compatibility identities that are **locked for now**:

- bundle identifier `sh.prims.paste`;
- executable `PrimsPaste`;
- CLI `prims-paste`;
- store root `~/.prims-paste/`;
- Keychain service `sh.prims.paste` / existing account;
- existing sticky IDs and serialized notebook compatibility.

Do not rename these merely to make source code aesthetically match the brand. TCC, Keychain, CLI users, existing stores, scripts, and old bundles must keep working.

#### Primboard architecture target

Primboard becomes the **private capture and staging surface** of the Prim ecosystem:

```text
capture -> encrypted sticky -> understand/annotate -> Convert to Prim… -> local durable Prim
```

Anything can land first: prose, secret, screenshot, image, audio, URL, task, question, receipt, person detail. Classification can happen later.

The current hard-coded Docket/Paseo/Note conversion menu becomes a compatibility layer over a generic conversion system:

1. search the Foundation Library MCP/catalog for a definition;
2. pin exact profile version and digest;
3. obtain schema/template/creation rules;
4. populate and validate **locally**;
5. write the resulting Prim locally;
6. leave a durable backlink on the sticky;
7. never copy a secret payload merely because the destination supports text.

Docket/Paseo remain useful explicit shortcuts where appropriate.

#### Primboard security/store refactor

Current strengths to preserve: AES-GCM blobs, local Keychain key, 0700/0600 permissions, no TTL, Touch ID opening UX, screen-share protections, local-only AI intent, payload-safe conversion, native Swift rather than Electron.

Required fixes/audits:

- **encrypt sensitive metadata/index state.** Today payload blobs are encrypted but `index.json` is plaintext and can include captions, key-detection metadata, timestamps, tab names, conversion refs, and layout. Define a v3 envelope with a tiny nonsensitive header around an encrypted index, with backwards migration and rollback;
- **concurrent writer safety.** App and CLI share one store while `NotebookStore` is `@unchecked Sendable` and index updates are read-modify-write. Add interprocess locking/transaction semantics and stale-write tests;
- **crash consistency.** Replace remove-then-move replacement gaps with a proven atomic replacement strategy; test power-loss/interruption scenarios as far as practical;
- **backups/recovery.** Define encrypted backup/export/restore, corruption detection, lost-key behavior, and explicit “cannot recover without key” UX;
- **Touch ID/key boundary.** Document and test that Touch ID is an app-level opening gate while Keychain accessibility enables the CLI design; decide whether optional stronger per-access key protection is needed without breaking automation;
- **migration framework.** Version store/index migrations explicitly; retain originals until migration verification succeeds;
- **secret handling.** Never log, include in crash reports, model prompts, conversion metadata, screenshots, notifications, or analytics; fuzz key detection and clipboard paths;
- **local AI boundary.** Treat local models as separate processes with explicit disclosure of which plaintext is sent; reject remote endpoints by default and test bypasses;
- **TCC regression suite.** Accessibility, screen capture, camera, microphone, app rename/install path, signing, and existing bundle identity must have a real Mac acceptance matrix.

#### Separate product development from user work

`Bugs.swift` and `FeaturesWanted.swift` currently compile Primboard's product backlog into the app and seed it into the user's notebook. Preserve this as historical dogfooding, but remove it from normal production behavior.

Target:

- product bugs/features live in GitHub/roadmap or explicit developer fixtures;
- production user notebooks start with user-owned content only;
- optional demo/developer mode may seed fixtures into an isolated temporary/dev board;
- migrations must not delete existing seeded cards from a real user's notebook without explicit user action.

#### Primboard UX/refactor lane

- clean resize/drag/layout behavior and large-board performance;
- make tabs/views (layout/time/week/month) coherent rather than independent experiments;
- improve attachment model for images/audio/video with bounded lazy decryption;
- accessibility/keyboard/VoiceOver coverage;
- restore/search/filter without decrypting the whole notebook unnecessarily;
- offline local search/index strategy that preserves privacy;
- “Convert to Prim…” powered by the same Library contracts as Hub/Desktop;
- versioned theme packages only after defining trust/sandbox rules; a theme cannot become executable code by accident;
- retain a sparse, calm native UI rather than turning the board into a general dashboard.

#### Primboard repository rename gate

Rename `prims-paste-desktop` to `primboard` only after:

- search all source/docs/CI/external repos for old GitHub URL and clone path;
- confirm no updater, release script, signing/notarization path, automation, package dependency, or deployment assumes the old slug;
- update successor links and preserve GitHub redirect behavior;
- prove build/sign/install from a fresh clone of the new slug;
- verify existing installed Primboard opens the same store and Keychain item;
- keep runtime IDs unchanged.

Completion: repo/product naming is coherent, old local data opens unchanged, encryption semantics are accurately described, concurrent app/CLI work is safe, and generic local Prim conversion works.

### Wave 5 — Consolidate Prims Browsers

Goal: one browser product, not separate repos for product-specific URLs.

Keep `prims-browsers`; absorb:

- `browsers-prims-sh` as cloud/gateway app;
- `logins-prims-sh` as cloud/login while the identity remains browser-specific.

Preserve `login.prims.sh`, `browsers.prims.sh`, shared cookie behavior, current Cloudflare bindings, and Authentik/machine gateway boundaries during migration.

Do not turn the browser login into Foundation-wide publisher identity accidentally. If Hub later needs authenticated publishers, design that independently.

Refactor targets:

- one shared contracts/config package for tenant/gateway/session shape;
- no duplicated static brand assets/session implementation across Workers;
- explicit machine/container registry contract;
- safe vault boundaries and no secret leakage into agent transcripts;
- product-level test matrix: local jar, cloud gateway, login, takeover, CDP/VNC fallback, recording, vault, multi-tenant isolation;
- Cloudflare deployment config co-located with the product.

Completion: old route repos can be archived without changing live browser behavior.

### Wave 6 — Refactor Prims Desktop around the new platform contracts

Goal: make Desktop the generic offline-first host for real Prims rather than a collection of profile-specific native paths.

Preserve existing open PRs and prove them on macOS before deciding merge/rewrite. Current open work includes Paseo connector registry, in-app Messages/XPC, durable debug logs, and Person name resolution; none should disappear during refactor.

Refactor targets:

- registry/profile list comes from local pinned definitions and optional Hub discovery, not hardcoded type lists;
- profile-specific Swift UI is replaced by generic hosted surfaces where practical, with native integrations only when the OS genuinely requires them;
- authoritative pack stays the file; no hidden second database;
- open/edit/save/export/revision behavior shares conformance fixtures with Hub/CLI;
- connectors have explicit identity, permissions, provenance and failure contracts;
- local private sources remain local unless the user explicitly shares;
- document handling, Quick Look, Finder/Mail/Messages, file associations and signed release continue to have Mac acceptance tests;
- debug/logging gets retention/privacy policy rather than “forever” by default without review.

Completion: a new profile published through the generic contract can be discovered/opened without shipping a bespoke Desktop release unless it requires an OS-native integration.

### Wave 7 — Migrate legacy Eidos `prim.*` incubators

Goal: preserve invention history while moving standards ownership to Prim Foundation.

Discovered incubators include at least:

- `prim.orf`, `prim.opf`, `prim.odwf`, `prim.opff`, `prim.omf`, `prim.ocsf`, `prim.osf`;
- `prim.docket`, `prim.album`, `prim.scene`, `prim.video`, `prim.brand`;
- private `prim.obf`, private `prim.emf`, `prim.cre.opaf`;
- archived `prim.obif`;
- temporary viewer experiments such as `prim.viewer.temp.odwf-viewer-v1`.

Do not batch-copy them into `prim` blindly.

Classification process for each repo:

1. identify normative schema/spec/validator/fixtures;
2. identify runtime/tool/product code;
3. identify private/customer/sample data and git-history exposure risk;
4. identify downstream consumers and package/repo URLs;
5. define semantic profile identity independent of source location;
6. import definition assets with source commit provenance;
7. preserve executable tooling only in an appropriate product/tool repo;
8. run old/new differential fixtures;
9. publish successor notice;
10. archive only after rollback/consumer verification.

Large hybrids (`prim.docket`, `prim.video`, `prim.scene`, private `prim.obf`) get explicit split plans before movement. Existing Eidos applications that merely *use* Prims do not automatically become Foundation-owned products.

Potential incoming product such as `eidos-agi/prims-launchpad-web` remains an Eidos incubation until its product boundary, governance, security model, and Foundation fit are deliberately accepted. Do not create a Foundation repo just because an old README proposed one.

Completion: Eidos is no longer the accidental permanent standards warehouse, yet useful tools/products retain appropriate ownership and history.

### Wave 8 — Organization governance, CI, quality, and archive completion

Goal: make the cleaner organization stay clean.

`primfoundation/.github` should provide:

- organization README explaining standards vs Hub vs products;
- contribution/security/code-of-conduct defaults;
- reusable CI primitives only where truly shared;
- PR template requiring scope, compatibility, evidence and release/deployment distinction;
- repository lifecycle metadata convention;
- archive/successor README template;
- security disclosure contact/process;
- dependency/update policy;
- release provenance expectations.

Each active repo should carry a small machine-readable product manifest with:

- product/repository role;
- owner/maintainers;
- public/private status;
- source-of-truth boundaries;
- production domains;
- runtime/platform;
- release mechanism;
- test command and acceptance matrix;
- data classification;
- MCP/API surfaces if any;
- dependencies on other Prim repos;
- compatibility IDs that must not be casually renamed;
- current lifecycle state.

Bug/quality program for every active product:

1. preserve existing bugs/open PRs;
2. inventory TODO/FIXME/stub paths and known failure fixtures;
3. build deterministic unit/contract tests;
4. add platform-specific acceptance where mocks cannot prove behavior;
5. security/privacy review proportional to the product;
6. accessibility and mobile/low-resource tests for public surfaces;
7. performance/resource budgets;
8. crash/recovery tests for durable local stores;
9. clean-install/build/release verification;
10. real-user acceptance before stable claims.

No generated “100% complete” score. Implementation, tests, review, release, deployment and real-use are independent evidence states.

## Current Foundation repository decisions

| Current repo | Target | Action | Archive gate |
| --- | --- | --- | --- |
| `.github` | `.github` | keep + strengthen | never by this plan |
| `prim` | `prim` | keep; absorb standards/profile definitions | never by this plan |
| `prim-web` | `prims-hub` | audit then rename/rework preferred | new Hub preview + cutover + history/security review |
| `prims-registry` | `prims-hub` | merge behavior/tests; keep compatibility hostname | production route parity + client inventory |
| `prim.workbook` | `prim/profiles/workbook` (+ viewer destination as appropriate) | migrate after privacy/history audit | old consumers + public scrub + successor proven |
| `prims-desktop` | `prims-desktop` | keep + generic-host refactor | never by this plan |
| `prims-browsers` | `prims-browsers` | keep + absorb cloud route apps | never by this plan |
| `browsers-prims-sh` | `prims-browsers` | merge cloud gateway | live domain + session + jar acceptance |
| `logins-prims-sh` | `prims-browsers` | merge browser login unless identity scope changes deliberately | Apple login/session/domain acceptance |
| `prims-paste-desktop` | `primboard` | keep product, stabilize, then repo rename | this repo is successor; old slug redirects, runtime IDs unchanged |

## Open PR preservation

At planning time, Foundation has open work that must be reconciled rather than erased:

- `prim` PRs #5, #6, #7, #8 form the current stacked Foundation program/library/platform path;
- `prims-desktop` PRs #2, #3, #4, #6 contain product work with explicit Mac proof gates;
- `prim.workbook` PR #1 contains public scrub/viewer work and warns about private customer history;
- `prim-web` PR #1 is the older Pages migration plan;
- `prims-registry` PR #1 pins the existing Worker/domain plan.

Every destination migration must decide whether each PR is merged, superseded with preserved commits, or closed with a successor reference. “Old architecture” is not permission to lose useful work.

## Rename policy

There are four different kinds of names; treat them differently:

1. **Brand/display name** — can change when product meaning improves (e.g. Primboard).
2. **Repository slug** — can change after dependency/link/release audit; GitHub redirects help but are not the only acceptance test.
3. **Public domain/API path** — compatibility surface; use redirects/versioning and real-client tests.
4. **Runtime/security identity** — bundle IDs, Keychain services, TCC principals, application identifiers, durable store roots, file format IDs. These are migration-sensitive and do not change for cosmetic consistency.

A rename plan must state which layer it touches.

## Archive policy

A repository becomes `candidate-archive` only when:

- successor location is live and documented;
- old default branch is frozen;
- all open PRs/issues are reconciled;
- consumers/dependencies are inventoried and migrated or intentionally supported;
- historical release/config evidence is preserved;
- README names successor and last supported commit;
- compatibility URLs/packages/files continue as promised;
- rollback period has passed;
- real-use verification exists.

Archive means read-only history, not deletion.

## Definition of done for the organization transformation

The transformation is complete only when:

- the active Prim Foundation organization has a small, explainable repository set based on responsibilities rather than accidents;
- `prims.sh` presents one coherent Hub with website/catalog/API/MCP backed by the same versioned definition library;
- Foundation profiles publish from portable packages and are not tied to a repository-per-type convention;
- historical Eidos profile incubators have explicit successor/compatibility states;
- Primboard safely preserves existing users while becoming the generic private capture-to-Prim surface;
- Desktop can consume new profiles through generic contracts;
- Browsers has one product repository and isolated cloud/runtime boundaries;
- every active product has tests, release evidence, security boundaries, owners and recovery documentation;
- retired repositories remain discoverable with useful history and successor pointers;
- no private user data was centralized merely to make the architecture look simpler.

The success criterion is not aesthetic repository cleanliness. It is **a Foundation whose standards, public platform and products can each improve rapidly without breaking one another or losing people's durable work**.