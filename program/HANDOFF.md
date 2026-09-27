# Foundation execution handoff — September 12, 2026

## GitHub execution is now established

[Issue #9](https://github.com/primfoundation/prims/issues/9) links all 26 package trackers and 16 executable tasks. Read live issues before selecting work; `github-execution.json` is a mapping and initial snapshot, not live state. [TASK-SYSTEM.md](TASK-SYSTEM.md) defines claiming, handoff, evidence, closure and staged Project Prim adoption. Start with #50/#51/#53/#55/#49. Projects access is now verified through Fleet and the laptop GitHub CLI after user authorization. [Project 1](https://github.com/orgs/primfoundation/projects/1) contains all 42 mapped issues; #64 retains receipts. Project fields are manually reconciled, not continuously synchronized. No unattended worker or Project exporter is claimed.

## Current delivery target and recovered Mac access

The user requested a comprehensive autonomous path to 95%. [DELIVERY-95.md](DELIVERY-95.md)
defines 26 work packages over the preserved 79 requirements, seven start waves,
critical release gates, a proposed weighted outcome rubric and exact next actions.
`plan.json` owns the package mapping and requirement status; no current 75% or 95%
claim has been established. The planning change does not complete requirements.

The September 12 execution preserved and reconstructed Desktop, Primboard (both
Macs) and Browsers source snapshots privately. Foundation's current 97 files are
verified separately because its existing Git history has a missing object. Original
working trees remain intact. The recovered private PrimSimCore candidate and clean
Desktop main build successfully; provenance remains unresolved. Desktop's test
compile fix reveals 27 legacy host assertion failures across 20 tests.

Library 0.1.0a4 and SDK 0.5.0-dev.3 complete-pack transport is merged in PR #20 at
`d01805f831f9c9a15ac8458409d3ab929886a026`, after all three CI workflows passed.
Python → TypeScript → Python archives are byte-identical after deleting originals;
110 Library tests, 100 Foundation tests, SDK and installed wheel/tarball checks pass.
See [the contract](COMPLETE-PACK-TRANSFER.md) and
[verification/publication evidence](evidence/2026-09-12-complete-pack.json).

Hub PR #15 is merged at `d14e43c988e2db4ffb9335e7662596b9db43ca7b` and the exact CI
artifact is deployed to the existing isolated preview. Complete packs open, edit,
save and reopen with original attachments, unknown files and capture receipts.
40 unit/DOM/type checks and 15 real browser tests pass; one phone hardware-keyboard
case is intentionally skipped. Post-deployment health verifies all essential routes
and release bytes. [Hub release evidence](evidence/2026-09-12-hub-transfer-release.json)
retains source, artifact, Worker version, rollback and checks. Production domain
cutover and independent user acceptance remain separate gates.

Primboard's clean-main candidate was company-signed, Apple-notarized, stapled and
Gatekeeper-accepted; its freshly extracted selftest passed. After a verified app/store
checkpoint it was temporarily installed with the matching CLI. **Existing-store
acceptance failed before migration:** the installed development notebook uses video
and newer metadata that clean main does not support. The original app and CLI were
restored, and every original notebook file remains byte-identical. Do not retry the
installation by removing metadata or treating this valid newer format as corruption.
[Mac execution evidence](evidence/2026-09-12-mac-execution.json) retains sanitized
receipts; private source, notebooks, keys and diagnostic logs remain on the Macs.

Primboard PR #6 is now merged at `f9161fc8d8a503d9dcf974c78361727f47f29667`
after macOS CI passed. It refuses unsupported notebook formats before lossy
migration, protects missing/concurrently created encryption keys, and refuses
attachment-dropping record-only imports/exports. Eleven new synthetic regressions
cover these boundaries. This source increment is not installed over the restored
app and does not resolve the newer private notebook's feature compatibility.

Primboard PR #7 is merged at `2cc43882795f61c060e7b99ef431665a655eb307`.
It retains file/video kinds, caption provenance, exact board-column strings,
worker records, fill defaults and conversion comments. Existing secret links
remain data-only; unsupported create/revert operations refuse before execution.
CI passed on `2e81de7b38c5a77a65bd7549522d22df013e5c61`; the selected Mac ran
178 scheduled tests with three intentional skips and zero failures. A separate
key-free check against the retained actual notebook passed: every original
metadata field/value survives decode/encode and snapshot bytes are unchanged.
The private encrypted roundtrip started but timed out; its cause is not proven
and it is not a pass. The richer installed app remains untouched. Exact scope,
receipts and limitations are in
[native compatibility evidence](evidence/2026-09-12-native-compatibility.json).

**Next execution:** implement native complete-pack attachment storage and reconcile
video/recording, board-column and worker UI with the preserved newer source.
Resolve the bounded existing-key encrypted snapshot roundtrip before another
signed existing-store upgrade. Do not mistake metadata-only proof for encrypted
restore or complete installed-app compatibility.
Finish Desktop source provenance and legacy host failures without changing old
working trees. Continue remaining reference cases, Research lifecycle, authenticated
distribution, Browsers real-account and production/operator/reviewer work packages.
No overall 75% or 95% acceptance claim is established.

Foundation PR #19 is merged at `eed0e6eae3f08352d587ff33738613bd377d98ac`, the
input main for the complete-pack increment. The original 79 requirement contracts
and all 26 delivery packages remain unchanged.

## Current state

The Foundation bootstrap (#5), ORF compatibility (#6), Library/MCP alpha (#7) and sanitized Workbook import (#10) are merged into `primfoundation/prims`. The reorganization work (#8) is merged at `cc640009089cd8663021fbd6a8211c7a605c68ea`. September 8 Hub and Primboard release work is recorded in `evidence/2026-09-08-release.json`.

Four development profiles are available through generic local creation tooling: Research, Person, Decision and Workbook. Source/workbook provenance is preserved; no customer-history import or stable-standard release is implied. All 17 workstreams, seven milestones and 79 requirement IDs remain. Whole-life contexts, diagnostics, ingestion, authority/privacy, governance, community, sustainability and the remaining diverse reference cases are still obligations.

## September 9 portable distribution increment

Library 0.1.0a2 adds installed `publish`, `resolve` and `restore` commands.
An external folder can become a data-only source without a Foundation checkout;
explicit namespace scopes, immutable source/definition pins, dependency closure,
withdrawals and a portable cache preserve offline installation and rollback.
77 Library and 97 Foundation tests pass locally, as do the SDK checks and actual
clean-wheel installed CLI/MCP smoke. The source is deleted before the restore
proof. PR #17 is merged at `fc4626fe3b597639725feff65c4cac6a3088b129`; all three CI workflows passed on `4f1122bd45cd7b86fd392450b966204d142bbc8a`. Exact source/artifact hashes and test scope are retained in
`evidence/2026-09-09-distribution.json`. See `DEFINITION-DISTRIBUTION.md` for the
runnable example, limits and remaining authenticated-publisher/identity gates.
No requirement is marked complete by these tests; the overall 75% target is
still not established by that increment. The September 11 plan now includes direct Fleet Mac execution.

## September 9 Research capture increment

Library 0.1.0a3 adds `capture-research` and `check-capture`: explicit local files
become a private native Research draft with byte-preserved originals, source
and permission provenance, and an initial capture receipt. Retry verifies the
prior operation without overwriting later edits. Complete-folder checks detect
missing or changed evidence. The current TypeScript reader preserves captured
record metadata, including exact nanosecond strings. Transfer the whole folder:
existing record-only host exporters do not migrate attachments.

96 Library tests (19 capture cases), 97 Foundation tests, existing SDK checks and
an actual installed-wheel capture/retry/folder-transfer smoke pass locally and
in all three CI workflows on PR #18 implementation head
`20ff9e3cab126e6b6af8a0f8ff8a123821184edb`. The PR retains the final ledger head
and merge identity; code evidence belongs to the exact tested source.
`evidence/2026-09-09-capture.json` retains the exact test/publication state and
`ARTIFACT-CAPTURE.md` provides the runnable example and limits. Source authority,
remote extraction, recursive media/archive parsing, revocation and independent
research/user review remain. All 79 requirements are still present.

## Integrated product increments

| Repository / PR | Result | Evidence |
| --- | --- | --- |
| `prim` #10 | Workbook provenance fix, immutable source regression, rebuilt four-profile Library | tested `86e8a58c…`; CI `34085213081` / `34085213070`; 53 Library + 96 Foundation Python tests, both TS suites, clean wheel and installed MCP smoke |
| `prim-web` #5 | canonical bundled Hub catalog, human pages, JSON/MCP and local-authoring kits | tested `dfe683cc…`; CI `34086822519`; six tests, dry build, real local Worker HTTP + external auto/legacy MCP parity for all four kits |
| `prims-paste-desktop` #1 | safe startup, current-version store locking, revision conflict rejection and atomic replacement | tested `d0fae3b9…`; macOS CI `34086141864`; 121 XCTest cases, release build, isolated selftest and compatibility guards |
| `prims-browsers` #1 | imported login/gateway Workers; shared session/assets; verified Apple identity and fail-closed configuration | tested `e542cd69…`; CI `34086860578`; 13 tests and two dry builds; complete synthetic Apple-to-gateway round trip |
| `prims-desktop` #7 | required-source/toolchain preflight prevents false successful proof | tested `075128f3…`; Bash syntax + real missing-dependency failure; no native pass |
| `.github` #1 | contribution, security, repository lifecycle and evidence defaults | document contents inspected; merged `350af7fe…`; no admin enforcement or independent review claimed |

All rows above are merged. Full tested and merge SHAs, scope and limitations are in [execution evidence](evidence/2026-09-07-execution.json). A CI result belongs to its exact tested commit, not arbitrary later work.

## September 8 shipped increment

- **Hub:** searchable discovery, readable specifications, connection onboarding, generic local creation/edit/validate/read/save/open for four pinned profiles and a downloadable offline workbench. Tests preserve unknown fields and declared Research relationships. Focused-field and stale-download-link regressions were found during hosted acceptance and fixed. The release evidence records exact artifacts, module/assets hashes, source commits, deployments and public HTTP/MCP checks.
- **Primboard:** PR #2 merged at `26fa1162c4569f2e2f87c4c4ffabc792f9aa4231`. The `PPI3` encrypted index envelope preserves an encrypted exact-byte legacy backup before migration; referenced legacy payloads authenticate with the existing key first. `prims-paste backup` and `restore … --to …` authenticate all referenced data, refuse replacement and restore to a new directory. CI `34175616470` and merged-main CI `34175780056` pass the 131-case suite, release build, isolated selftest and compatibility guards. No signed binary or private-store migration was performed here.
- **Operations:** the previous Cloudflare catalog was restored at 100%, observed live, then the current workbench version was restored and observed. A six-hour public health workflow is configured. Exact drill versions and deployments are retained; it was limited to the isolated preview.

## Next actionable gates

The subsequent Primboard increment is recorded in
[`evidence/2026-09-08-primboard-journal.json`](evidence/2026-09-08-primboard-journal.json).
PR #3 protects the working installation during candidate preparation and adds
resumable notarization tooling. PR #4 adds an authenticated encrypted multi-file
redo journal, recovery before store reads/writes, precise cleanup, path/size
checks, and deterministic derived-tab metadata. macOS CI exercises 151 scheduled
XCTest cases (including 20 journal cases and a subprocess-only helper), five real
abrupt process-exit scenarios, and 14 release-tool tests. The fixture helper and
absent optional integrations are not counted as ordinary passed tests. Exact
source, merge, CI identifiers and limitations are retained in that evidence file.

1. **Shipped portable hosts:** Foundation PR #15 and Primboard PR #5 are merged. The SDK installs outside the checkout; 83 shared cases exercise Python, TypeScript and Swift. Generic native creation/edit/export/import, operation IDs, recoverable drafts and guided locked recovery are implemented. Exact source and passing CI are in `evidence/2026-09-08-portable-delivery.json`.
2. **Hub acceptance:** PR #11 actual desktop Chromium and phone-size WebKit downloads, offline HTML and pack reopen passed, as did automated accessibility/overflow and desktop keyboard checks. PR #13 also enforces native portable-export budgets and passes real Hub ZIP-to-SDK tests, including the exact 512 KiB boundary. PR #12 adds all pinned category registry routes beside the four profiles; postmerge hosted HTTP/MCP passes. These checks supersede the earlier browser-engine download gap; they do not establish this chat's download bridge or independent real-user/assistive-technology acceptance.
3. **Compatibility follow-up:** five selected public incubator baselines retain 28 exact source blobs and 27 fixed CLI checks, including the original six OPF tests. Five cases deliberately record known unsafe acceptance. No semantic migration or arbitrary user-input safety is claimed. SDK export now checks actual formatted bytes before creating a folder, preventing an export its own reader cannot reopen. The audit retains source selection/privacy/license limits.
4. **Public operations:** current portable-export preview version `2dd0054f-5f19-4a93-9d2b-907b14a99752` has immediate rollback target `1bf1e03e-6899-4c0e-b9b9-e992a3ccc891`. Existing Free defaults remain; custom CPU limits were rejected without paid activation. Apex/www remain on Pages and production registry/login/browsers retain old Workers. Resolve ownership, cost/escalation, old clients and Railway mapping before cutover.
5. **Mac/source gates:** use `MAC-RELEASE.md` in the Primboard repository for signed installed existing-store/Keychain/TCC acceptance. September 11 Fleet execution now works; preserve dirty work and verify the discovered prim-sim candidate's source lineage/reuse authority and actual build. Preserve integration PRs and never substitute a stub. Real Apple/session/container and independent outside-user/stewardship acceptance also remain.
6. **Broader implementation:** `REMAINING-GATES.md` names available publishing, resolution, reference cases, ingestion, composition and migration work. The full project is not merely waiting for the Mac. All 79 requirements remain; no 75% claim follows from these increments.

## Stable boundaries

Private Prim instances stay local/user-owned. The public Hub distributes definitions and public metadata. Popularity has no fabricated launch signals and does not mean truth, safety or official status. Primboard and Desktop bundle/CLI/Keychain/store/signing identities remain fixed. Valid legacy browser session cookies remain compatible; restart old in-flight Apple logins when a future nonce-enforcing cutover occurs.

No production DNS or route change, repository archive/rename, history rewrite, signed release, private data upload or paid unattended worker was performed. No background agent is running. Bounded repository CI and the configured public health workflow are the only unattended checks added. `plan.json` remains the canonical ledger; regenerate `ROADMAP.md` with `python tools/program.py render` after edits.