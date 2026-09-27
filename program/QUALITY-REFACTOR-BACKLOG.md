# Prim Foundation quality and refactor backlog

Status: observed/proposed quality program, September 6, 2026. This is not permission to rewrite working compatibility surfaces without tests. Items are classified so old code is neither preserved merely because it exists nor discarded merely because it is old.


**September 7 resolution checkpoint:** Primboard normal-startup seeding, stale concurrent writes and remove-then-move replacement now have tested fixes merged in PR #1. Browser Worker duplication and legacy unsigned-token/missing-secret authentication defects have fixes merged in PR #1. Hub catalog drift/runtime source fetching are addressed by a verified canonical bundle in PR #5. Desktop's false successful proof after skipped source tests is fixed in PR #7; its authoritative dependency remains unavailable. These are bounded fixes, not closure of the encrypted metadata, multi-file recovery, real-account/device, production and independent-review obligations below. See [execution evidence](evidence/2026-09-07-execution.json).

## Classification

- **DEFECT** — current behavior can violate a stated contract, lose data, leak information, or fail a known workflow.
- **DEBT** — design works but creates unnecessary coupling, duplication, or future migration cost.
- **MIGRATION** — naming/topology/runtime change that needs compatibility proof.
- **PROOF** — implementation may be correct, but current automated/local evidence cannot establish platform behavior.
- **PRODUCT** — intentional capability/UX improvement, not a bug.

Every fix should state which class it addresses and its acceptance evidence.

## `prim` — standards/profile source

### DEBT — profile identity still leaks repository-era assumptions in legacy registry/SDK

Target: profile identity and publisher/version are semantic; source repository is distribution metadata only. Keep old SDK behavior readable during migration and add explicit compatibility rather than deleting fields blindly.

### DEBT — category/type/profile/kind vocabulary has historical overlap

Target: reconcile the small category substrate with profile/kind semantics using Research plus diverse reference cases. Avoid one giant ontology and avoid merely renaming fields without migration semantics.

### DEFECT/DEBT — generated/typed status vocabularies and old registry data can drift

Existing historical registry/SDK states have already shown mismatches (for example retired entries versus narrower typed statuses). Convert this class of drift into generated schemas/conformance fixtures rather than manual parallel lists.

### MIGRATION — one-repo-per-profile documentation conflicts with actual practice

Person already lives in `prim`; workbook represents multiple related kinds; Foundation Library work supports multi-profile sources. Update public architecture only after the portable package contract is reviewable and compatibility documented.

### DEBT — old Eidos URLs/names remain in profile metadata and docs

Systematically inventory stale repository/package/homepage links during each profile migration. Preserve old locations as historical aliases where useful; do not silently make URLs semantic IDs.

### PROOF — independent implementation interoperability

Current reference tools and tests do not equal two independently developed implementations. Stable claims remain gated on cross-implementation fixtures and unknown-field preservation.

## `prims-hub` target / current `prim-web` + `prims-registry` + Library MCP

### DEBT — public Foundation currently fragmented by implementation layer

Website, registry Worker, Library/MCP alpha, login/gateway experiments and Cloudflare migration plans live separately. Consolidate website/catalog/API/MCP/ranking/compat routes into one Hub product while keeping standards and user data out of it.

### MIGRATION — Railway/Pages/Workers deployment intent conflicts

`prim-web` main still contains Railway deployment history while an open PR proposes Pages; the target architecture now favors Workers + Static Assets. Preserve old deployment proof, create preview first, then supersede—not overwrite—the prior migration path.

### DEBT — registry Worker mirrors source-of-truth but exists as a permanent repo boundary

Absorb its HTTP compatibility contract/tests into Hub. Keep `registry.prims.sh` as an endpoint, not a repository architecture requirement.

### PRODUCT — marketplace-quality discovery

Add profile detail pages, versions, publisher, digest, creation availability, examples, compatibility, conformance/security states, Popular/Trending, “Use with AI”, download and local-create guidance. Information density should increase from home → catalog → detail, borrowing the AIC Hub pattern without copying enterprise identity.

### SECURITY — external profile publication

Before accepting arbitrary external definitions: authenticated publisher identity, immutable pins, withdrawal/retraction, bounded resource parsing, no arbitrary validator execution, moderation, abuse reporting, and source/provenance display.

### SECURITY/PRIVACY — popularity

Do not activate telemetry-like adoption counting merely because ranking code exists. Require opt-in/consent, authenticated collector model, deletion, anti-Sybil/anomaly controls, minimum cohorts, policy versioning, and a clear statement that popularity is not quality/truth/security.

### PROOF — Cloudflare runtime adapter

The tested Python MCP package proves protocol behavior, not Cloudflare Worker compatibility. Implement a Worker-native adapter (likely TypeScript unless Python Workers proves cleaner) against the same contracts and conformance fixtures. Two runtimes must not create two definitions.

### PROOF — production readiness

Preview, custom domain, TLS, caching, MCP current/legacy clients, rate limits, error budgets, log privacy, rollback, static assets, redirects, mobile/accessibility, and external user agent tests are distinct gates.

## Primboard / current `prims-paste-desktop`

### DEFECT/SECURITY — sensitive metadata is plaintext

Payload blobs are encrypted, but `index.json` contains captions, timestamps, tabs, key-detection metadata, conversion refs and spatial metadata. Users can reasonably interpret “encrypted sticky board” more broadly than that implementation.

Target: versioned encrypted-index/store envelope with backwards migration, retained original until verification, corruption detection and explicit loss/rollback semantics.

### DEFECT — concurrent app/CLI read-modify-write can lose updates

App and CLI intentionally share one store. `NotebookStore` is `@unchecked Sendable`, reads an index, mutates it and writes it back without an explicit interprocess transaction/lock contract.

Target: proven interprocess locking or transaction journal, stale-write detection, concurrent writer tests, lock timeout/recovery, and no deadlock when a process crashes.

### DEFECT/RECOVERY — replacement has a remove/move gap

The current atomic helper writes a temporary file, removes the old destination, then moves the replacement. Test and replace this with a crash-consistent platform strategy; “temporary write used .atomic” does not by itself prove the final replacement is atomic.

### DEBT — product backlog is embedded in the user's product/store

`Bugs.swift` and `FeaturesWanted.swift` compile the product backlog and seed stickies into the notebook. This was effective dogfooding but violates the mature separation between product development state and user durable work.

Target: move backlog to GitHub/Foundation program; keep fixtures only in isolated developer/demo mode; never delete already-seeded user cards without explicit user choice.

### MIGRATION — Primboard brand vs compatibility identities

User-facing Primboard is correct. Planned repo rename to `primboard` should happen only after link/CI/release audit. Preserve for now: `sh.prims.paste`, `PrimsPaste`, `prims-paste`, `~/.prims-paste`, Keychain service, serialized IDs/formats.

### SECURITY/PRODUCT — Touch ID versus key access

Touch ID is an app-opening UX gate; Keychain accessibility supports the shared CLI design. Document the threat model explicitly and consider optional stronger key policies without silently breaking CLI automation or existing stores.

### PRODUCT — generic `Convert to Prim…`

Replace the permanently hard-coded destination enum as the extensibility boundary. Search/fetch a pinned creation kit from Hub/MCP, populate/validate locally, create local Prim, leave backlink, and never transfer secret payload by default. Docket/Paseo can remain shortcuts/adapters.

### SECURITY — local AI

Keep remote endpoints rejected by default. Define exactly which decrypted text/images/audio can be sent to a local model process and how long it exists in memory/logs. Test configuration bypass, process errors and output injection.

### PRODUCT/QUALITY — board scale and interaction

Bounded lazy decryption, search/filter, attachment loading, drag/resize performance, z-order, tab/calendar lens consistency, keyboard/VoiceOver, clipboard/drop behavior, theme trust, recovery from huge/corrupt boards.

### PROOF — real Mac acceptance

Signing/notarization, TCC persistence after display/repo rename, accessibility fill, screen capture protections, mic/camera prompts, Touch ID, Keychain continuity, same-store CLI, clean install/update and existing-store migration require actual signed Mac tests.

## `prims-desktop`

### DEBT — generic host versus profile-specific implementation

Existing Person/iMessage work and other native paths prove useful integrations but risk reintroducing one native face per profile. Keep OS-native connectors where needed while making profile discovery/view/edit generic through portable definitions and hosted surfaces.

### MIGRATION/PROOF — open PR reconciliation

PRs #2, #3, #4 and #6 have explicit constraints and Mac proof gaps. Inventory and run required host tests before merge/supersession. Never discard their working lessons because a larger refactor exists.

### SECURITY/PRIVACY — “forever” debug logs

Open PR #4 proposes never-rotated day logs. Treat this as a policy decision, not a default quality win: define sensitive-field redaction, retention, disk quota/export/delete, and whether logs can contain filenames/people/connectors. Debug durability and privacy need separate requirements.

### DEBT — path/profile assumptions

Person resolution currently searches specific filesystem layouts. Evolve toward a local Prim index/query abstraction driven by pinned profiles, while retaining explicit compatibility for current on-disk locations.

### PROOF — XPC/FDA/identity boundaries

Existing PR work correctly distinguishes bundle identity, Full Disk Access principal and XPC rendezvous. Keep actual signed-Mac proof as the gate; Linux/static checks cannot certify TCC/FDA behavior.

### PRODUCT — offline-first Hub integration

Hub discovery is optional enrichment/cache. Desktop must open already-pinned/local Prims without network or Foundation availability.

## `prims-browsers` + route repos

### DEBT — duplicate cloud product code/repos

Login and gateway repos duplicate product assets/session concepts and exist solely for Browsers. Consolidate into the product repo with shared contracts while keeping independently deployable Workers if needed.

### SECURITY — session boundary

Preserve Secure/HttpOnly cookie semantics, Apple callback correctness and product-specific scope. Do not reuse Browsers identity as publisher/admin authority for Hub without a deliberate auth design.

### SECURITY — vault and agent isolation

Tests must prove tenant/cookie/vault isolation, no secret echo in agent transcript, safe takeover, CDP/VNC fallback boundaries, recording scope and cleanup. Private fleet config never goes into public examples.

### DEBT — configuration as ad hoc variables/fallbacks

Move tenant/container registry into a validated, versioned config contract with explicit source, owner and safe defaults. Product configuration remains separate from the Prim standards registry.

### PROOF — local versus hosted behavior

Local multi-tenant jars, Paseo plugin shape, cloud gateway, Authentik handoff and headed-window behavior need end-to-end tests. A Worker unit test alone does not prove a browser jar.

## `prim.workbook`

### SECURITY/MIGRATION — private history/public scrub risk

Open PR #1 explicitly warns about historical customer/Greenmark/Cerebro material and repository visibility. Complete git-history/privacy review before public migration or archive. Removing files from current HEAD is not proof history is safe.

### DEBT — profile and viewer are combined by historical convenience

Normative workbook/worksheet/measure/metric definitions should move to `prim`; determine whether viewer belongs in Hub, Desktop, or another generic surface based on lifecycle rather than preserving repo boundaries.

### PROOF — private dropped packs

Browser-local drag/drop behavior must prove nothing uploads unexpectedly; add network-negative tests and malicious archive bounds if kept.

## `prims-registry`

### DEBT — README/runtime reality drift

The repo describes itself as local/no Worker while a Worker source/config exists and an open PR configures domains. Consolidation should preserve observed behavior and rewrite docs from verified reality, not choose whichever description is newer.

### MIGRATION — source URL and compatibility

The Worker points at `primfoundation/prim/main/registry/registry.json`. Hub migration must either preserve that compatibility or version a new endpoint. Never make a mutable `main` URL an immutable distribution pin.

## Legacy Eidos `prim.*` incubators

### MIGRATION — standards ownership

Move semantics only after per-repo classification; preserve source commit lineage. Eidos incubation was where the family was discovered, not necessarily the permanent standards topology.

### SECURITY — private repos and sample data

Private `prim.obf`, `prim.emf`, workbook history and any customer-derived fixtures require content/history audit before Foundation/public migration. Never infer that a schema repo is safe to publish because the schema itself is generic.

### DEBT — profile/tool hybrids

Docket, video, scene and other large repos may contain both normative format and substantial runtime/tooling. Split responsibility rather than dumping full products into `prim`.

### DEBT — stale names/version coupling

ORF already demonstrated stale repository URLs and profile version tied to OKF grammar line. Audit all incubators for repository-based identity, stale links, grammar/profile coupling and workflow-specific rules before declaring Foundation versions.

## Organization-level quality gates

Every active repository eventually needs:

- `AGENTS.md`/maintainer guidance that states product boundary and dangerous identities;
- `SECURITY.md` appropriate to its threat model;
- deterministic test command plus platform acceptance matrix;
- clean build/install proof;
- release/deploy distinction;
- dependency and secret-name inventory;
- logging/privacy/retention policy;
- backup/recovery when durable state exists;
- accessibility requirements for human surfaces;
- resource/performance budgets;
- machine-readable product manifest;
- successor/archive metadata if migrating.

## Refactor rule

Newer models and agents should feel free to replace poor code. They should **not** feel free to replace contracts they have not understood.

For each old subsystem:

1. state the user/product behavior worth preserving;
2. state accidental implementation details;
3. identify compatibility/security identities;
4. write tests around behavior and known failures;
5. build the cleaner implementation beside the old one;
6. compare outputs/real use;
7. cut over with rollback;
8. delete/archive only after proof.

The goal is not reverence for old code. It is freedom to rebuild **without losing the accumulated truth hidden inside it**.