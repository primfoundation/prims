# Foundation reality inventory — 2026-09-07

Status: pre-execution point-in-time checkpoint for Wave 0. This records observed GitHub state before repository rename/archive or production cutover. It is not a claim that every deployment, secret binding, release artifact or external consumer has already been discovered.


**Later September 7 execution:** Foundation #5/#6/#7/#10, Hub #5, Browsers #1, Primboard #1, Desktop #7 and governance #1 have since merged. This inventory retains the observed earlier heads/PRs for provenance. Use [GOAL-STATUS.md](GOAL-STATUS.md) and [execution evidence](evidence/2026-09-07-execution.json) for current results and merge commits. Production routes, repository slugs and archive gates remain open.

## Prim Foundation repositories

| Repository | Visibility | Observed default head | Current role | Target direction |
| --- | --- | --- | --- | --- |
| `primfoundation/prims` | public | `08760405325ca3f9c9b63648c7398ffc4c96e831` | category/spec/registry/SDK/profile incubation | keep as standards/profile/conformance source |
| `primfoundation/prims-web` | private | `02add4e6c739d9152ade1696e3103492e62e097f` | current website/history | audit; preferred evolution/rename into `prims-hub` |
| `primfoundation/prims-registry` | private | `7dd77093d789f0f6317e21e9104a5d346353d3e2` | Cloudflare registry mirror | fold runtime into Hub; preserve compatibility route |
| `primfoundation/prim.workbook` | public | `b4376fcf3332eaadf1d51c5396e924c41f17d6e7` | workbook/worksheet/measure/metric profile experiment | import sanitized profile semantics into `prim`; archive only after privacy/consumer proof |
| `primfoundation/prims-desktop` | public | `956233b38bf9fdc4565c86b76a95965fe69c356d` | signed desktop host/connectors | keep; refactor toward generic profile hosting |
| `primfoundation/prims-browsers` | public | `2fd507bc0619c6bc0da0098bbe9334c951668a91` | browser sandbox product | keep; absorb login/gateway cloud surfaces |
| `primfoundation/browsers-prims-sh` | private | `4046cff490f13766dda8a33367f0ea1ac04397c5` | Browsers gateway Worker | migrate to `prims-browsers/cloud/apps/gateway`, then compatibility/archive |
| `primfoundation/logins-prims-sh` | private | `15abc2716afddc8c127d25cd84630146442bd299` | Apple login Worker for Browsers | migrate to `prims-browsers/cloud/apps/login`, then compatibility/archive |
| `primfoundation/prims-paste-desktop` | public | `25d2641443c1e9d4b55b2651c18188a378a3b166` | Primboard product under historical repo slug | stabilize, then rename repo to `primboard`; preserve runtime identities |
| `primfoundation/.github` | public | `6e9911abe205b4c8b8e89751bc916b23954f3801` | organization profile only | keep; add defaults/lifecycle/governance carefully |

Observed branch metadata for sampled main branches (`prim`, `prims-desktop`, `prim-web`, `prims-registry`, `prim.workbook`, `prims-browsers`, `.github`) reported branch protection disabled. This is an operational/governance gap to address through a reviewed organization policy; it is not changed by the transformation planning branch.

## Open pull requests observed

Existing work is migration input, not disposable legacy.

### `primfoundation/prims`

- #5 — Foundation program bootstrap and repository-independent profile discovery.
- #6 — ORF compatibility baseline and loss-aware Research inspection.
- #7 — Foundation Library MCP, definition-driven creation, Popular/Trending.
- #8 — organization transformation target / Cloudflare and repository reorganization (this branch).

### `primfoundation/prims-web`

- #1 — older Cloudflare Pages migration proposal; preserve its route/header discoveries while superseding deployment architecture only after the Worker preview proves better.
- #5 — G2 Cloudflare-native Prims Hub preview. CI run `34074018249` passed typecheck/tests and a Wrangler Worker + Static Assets dry build. No Cloudflare deployment is inferred.

### `primfoundation/prims-paste-desktop` / Primboard

- #1 — G3 stabilization lane: Mac CI, compatibility locks, portable local-tool paths and hermetic conversion tests. Initial CI exposed real Swift 6 calendar layout typing and developer-machine tool-path assumptions; both are being fixed on the branch. Product/user data are untouched.

### `primfoundation/prims-browsers`

- #1 — G4 cloud consolidation: shared session contract and exact route-repo migration record. Production login/gateway Workers remain in their current repositories until imported-preview and real Apple/container acceptance.

### `primfoundation/.github`

- #1 — G7 security/contribution/repository-lifecycle defaults and updated organization profile. It does not activate organization administration settings by itself.

### `primfoundation/prims-desktop`

- #2 — Paseo connector tenant registry; preserve its bounded connector model and Mac proof requirements.
- #3 — Messages/FDA plus XPC rendezvous; explicitly requires real-Mac proof and says not to treat XPC as the FDA acceptance.
- #4 — detached Debug/day-log work; requires Mac HostTests before merge.
- #6 — Person Prim names in iMessage rows; requires installed-Mac acceptance.

### `primfoundation/prim.workbook`

- #1 — sanitizes Greenmark/Cerebro references and replaces them with fictional Acme data. Head `8e997f0e349d788c56722ea8bd0c3d0afbdb99e5`. The PR itself warns that repository history must be reviewed before visibility/archive decisions. Any standards import must use sanitized semantics/fixtures with explicit provenance rather than copying sensitive history.

### `primfoundation/prims-registry`

- #1 — Cloudflare account/custom-domain configuration. Preserve the intended `registry.prims.sh` compatibility surface while moving runtime responsibility into Hub.

## Current public/cloud boundaries observed

- `prims.sh` — Foundation website; current repository contains older Railway and Cloudflare Pages migration assumptions. Target is one Workers + Static Assets Hub after preview/acceptance.
- `registry.prims.sh` — registry compatibility Worker route in the legacy registry repository.
- `login.prims.sh` — Sign in with Apple door for Prims Browsers.
- `browsers.prims.sh` — authenticated Prims Browsers gateway.
- Public Foundation Library/MCP alpha is built/installable in `prim` but is not yet a Foundation-hosted endpoint.

At this initial checkpoint no Cloudflare administration connector was available, so exact live origin bindings, project/version inventory, current traffic, secret binding presence, rollback history and external consumers were unresolved. On September 7 Clawdflare connected successfully: account/zone and the three existing Prim Worker names/timestamps were verified. The isolated Hub preview was created disabled; asset upload then failed scoped-token verification. See [the follow-up evidence](evidence/2026-09-07-cloudflare-preview.json). This bounded read does not complete the wider operational inventory.

## Legacy Eidos Prim incubators

The migration ledger already includes discovered `eidos-agi/prim.*` work such as ORF, OPF, ODWF, OPFF, OMF, OCSF, OSF, Docket, Album, Scene, Video, Brand, private OBF/EMF, OPAF, archived OBIF and temporary viewer work. These are inventions to classify, not a permanent one-repository-per-profile mandate.

Rules:

- small profile-only source → import as a portable profile package with source commit provenance;
- profile + substantial runtime/tool → split normative definition from justified product/tool responsibility;
- private source → privacy/history audit before any public import;
- already archived source → preserve compatibility provenance, do not resurrect by default;
- no repo movement changes semantic profile identity.

## Wave 0 remaining gates

This checkpoint materially advances repository/open-work reconciliation, but W0 is not fully closed until we also have:

1. Cloudflare live-resource/domain/version/binding inventory from the owning account;
2. package/release/download consumers and external source references for repos slated to rename/archive;
3. current deployment/release ownership and cost responsibility;
4. explicit reconciliation of every Eidos incubator's active consumers/private-data risk;
5. organization administration baseline (branch rules/private vulnerability reporting/release controls) from an admin-capable inspection.

Those are real evidence gates, not reasons to stop implementation in independent lanes.

## Deployed preview follow-up — September 7, 17:05 UTC

The initial upload failure is resolved and the isolated Hub preview is deployed. The exact module, five-file asset manifest, Worker version/deployment, browser observation and client checks are recorded in [deployment evidence](evidence/2026-09-07-cloudflare-deployed.json). Existing login, gateway and registry Worker timestamps remain unchanged; this does not claim a production route migration or complete operational inventory.


## Shipped workbench and recovery follow-up — September 8

The Hub now serves 36 assets, searchable/readable discovery, local authoring for
four profiles and an offline workbench. Primboard encrypted-index and backup
recovery changes are merged with Mac verification. The actual preview
rollback/return drill, current artifacts and all remaining acceptance limitations
are recorded in [release evidence](evidence/2026-09-08-release.json). The legacy
Railway workflow separately returned `Service not found`; production service
mapping remains unresolved. Historical observations above remain dated evidence.