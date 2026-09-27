# Foundation task execution system

Created September 12, 2026 under the user's instruction to establish GitHub execution and staged use of Prims. Requirements: PRG-002/003/005, LIFE-002, AUTH-001/002/003/004.

[Start with the execution tracker](https://github.com/primfoundation/prims/issues/9).

## Authority

- `plan.json` remains authoritative for all 79 requirement contracts, statuses and required evidence. Its 26 delivery packages are unchanged.
- GitHub issues own operational task state, claims, blockers and acceptance evidence. A task can finish while its broader requirement remains incomplete.
- `github-execution.json` is an issue mapping and creation-time snapshot. Do not use its initial statuses as a live queue. Read issues before execution.
- Project Prim export is planned, not implemented or certified by this task-system change. One-way snapshots precede any writeback or authority migration.
- The Foundation's goal is free public usefulness, ownership and continuity. Issue closure counts, sales and synthetic popularity are not mission-completion metrics.

## Execution protocol

1. Read issue #9, the selected issue, its package entry gate and current dependencies. Check the owning repository, current branch/PR overlap and applicable instructions.
2. Claim the task in the issue body with executor/session identity, UTC start, branch and exact next action. Re-read the claim before mutation; GitHub body edits are not an atomic distributed lease. If simultaneous claims appear, stop overlapping writes and resolve ownership. Do not build an unattended scheduler until concurrency and authority are enforced.
3. Use one active implementation task per executor. Ready means a bounded next action exists, not that all downstream release gates passed. Waiting means prerequisites remain; Blocked names a concrete external condition. In review means implementation evidence is available and acceptance remains.
4. Work on isolated branches. Cite the execution issue and requirement IDs in PRs. Run targeted regressions plus required repository gates. Test failure and recovery modes; an independent environment or second reader supplies the double check where the task requires it.
5. Update the issue with exact source, test results, artifact/release links, limitations and the next action. Do not close a task solely because a PR merged. Do not count skipped, timed-out, synthetic or self-reviewed results as stronger evidence than they are.
6. At session end, release the claim or mark it paused with a resumable checkpoint. No continuing worker is implied by an open issue. A later executor revalidates source and permissions before resuming.
7. On task acceptance, update requirement evidence through a Foundation PR, then close the issue's bounded scope. Preserve unmet package gates. A subsequent defect reopens or creates a linked regression issue with its own reproduction.

Human operators/reviewers remain unassigned until roles are actually accepted. The implementation-lead role belongs to the authorized execution process; it is not a fictional GitHub account and does not automatically assign Daniel every task. Prepare concrete decision packets before requesting human-only authority.

## Immediate queue

Start with native complete-pack transfer (#50), bounded encrypted snapshot recovery (#51), the Research demonstration (#53), Project representation (#55), and the scored baseline (#49). These are separate executable lanes; do not overlap edits without explicit coordination. Source and metadata work already shipped is retained in the dated evidence and must not be repeated as new progress.

## Project Prim adoption

Stage 1 (#55): define the development Project model, including work-item identity, dependencies, decisions, evidence, source revision and authority. Test ambiguous acceptance, reopened work and missing references.

Stage 2 (#56): export explicitly selected public GitHub work into immutable, versioned Project snapshots. Preserve GitHub identity and source timestamps; record export coverage, omissions and unavailable evidence. Test pagination, changed/deleted records, interruption, deterministic unchanged snapshots and offline second-reader continuation. The export never grants execution permission or silently fetches private attachments.

Stage 3 (#57): prove fresh-executor handoff from the snapshot, then design guarded writeback. Expected revisions, allowlisted mutations, authorization, idempotency and conflict refusal must pass before writes are enabled. A later change of authority requires an explicit migration, not two editable competing records.

## Views and access limitation

The [Prim Foundation Delivery Project](https://github.com/orgs/primfoundation/projects/1) is now populated through authenticated GitHub CLI on the authorized Fleet laptop. It contains the same 26 packages and 16 tasks, with Status, Kind, Delivery package, Priority, Implementation repository and Blocker fields. Repeated import and read-back verified all 42 memberships and field values. The Project is private. The connector still has no Projects operation; Fleet plus CLI supplies the authorized path. Fields are a manually reconciled view of live issues, not automatic synchronization. Read current issue state before acting. See issue #64 for execution receipts and acceptance.

## Estimates and reassessment

Preliminary cumulative ranges from the execution narrative: 4–8 active hours for a verified baseline, 24–48 for the first complete journey, 80–160 for a coherent candidate, and 180–320 for broad release acceptance. These overlap and must not be added together. Calendar ranges depend on sustained sessions and external reviews; no deadline or current 95% score is established. Reforecast after 8–12 observed hours and after native transfer, installed acceptance and outside-user checkpoints.

## Mapping correction

Earlier narrative/evidence references calling native reconciliation D95-05 were incorrect package labels. The authoritative ledger assigns D95-05 to Research, D95-04 to complete transfer, D95-14 to Primboard, D95-15 to Desktop, with security/release cross-links. The issue map follows the ledger; historical evidence remains retained without altering its test facts.

## Delivery package index

| Package | Issue | Wave | Requirements |
| --- | --- | --- | --- |
| D95-01 | [Recover source and reconcile current work](https://github.com/primfoundation/prims/issues/23) | 0 | PRG-001, PRG-004, PRG-006, RELENG-001 |
| D95-02 | [Make delivery and evidence mechanically checkable](https://github.com/primfoundation/prims/issues/24) | 0 | PRG-002, PRG-003, PRG-005 |
| D95-03 | [Finish the small common contract](https://github.com/primfoundation/prims/issues/25) | 1 | CORE-001, CORE-002, CORE-004, REL-004 |
| D95-04 | [Transfer complete packs and preserve attachments](https://github.com/primfoundation/prims/issues/26) | 1 | CORE-003, HUM-001 |
| D95-05 | [Complete the Research lifecycle](https://github.com/primfoundation/prims/issues/27) | 2 | RES-001, RES-002, RES-003 |
| D95-06 | [Prove independent Research exchange](https://github.com/primfoundation/prims/issues/28) | 5 | RES-004, INTEROP-004 |
| D95-07 | [Complete the six reference cases and context map](https://github.com/primfoundation/prims/issues/29) | 1 | LIFE-001, LIFE-002 |
| D95-08 | [Handle identity, composition and concurrent history](https://github.com/primfoundation/prims/issues/30) | 2 | REL-001, REL-002, REL-003 |
| D95-09 | [Make profile authoring self-service](https://github.com/primfoundation/prims/issues/31) | 2 | PUB-001, PUB-004, PUB-005, DEV-002 |
| D95-10 | [Authenticate publishing and remote resolution](https://github.com/primfoundation/prims/issues/32) | 4 | PUB-002, PUB-003, PUB-006, DIR-002 |
| D95-11 | [Finish one Hub discovery and authoring surface](https://github.com/primfoundation/prims/issues/33) | 2 | DIR-001, DIR-003, DIR-005, DEV-005 |
| D95-12 | [Operate moderation and honest adoption signals](https://github.com/primfoundation/prims/issues/34) | 4 | DIR-004, DIR-006, DIR-007 |
| D95-13 | [Release supported packages and clients](https://github.com/primfoundation/prims/issues/35) | 2 | DEV-001, DEV-004, DEV-006, RELENG-002 |
| D95-14 | [Accept Primboard as a trustworthy daily product](https://github.com/primfoundation/prims/issues/36) | 3 | HUM-004 |
| D95-15 | [Recover and ship the generic Desktop host](https://github.com/primfoundation/prims/issues/37) | 3 | HUM-002 |
| D95-16 | [Prove accessibility and representative environments](https://github.com/primfoundation/prims/issues/38) | 3 | HUM-003, LIFE-004 |
| D95-17 | [Finish trustworthy local and remote ingestion](https://github.com/primfoundation/prims/issues/39) | 5 | ING-001, ING-002, ING-003, ING-004 |
| D95-18 | [Enforce bounded agent operations](https://github.com/primfoundation/prims/issues/40) | 2 | DEV-003, AUTH-001, AUTH-002, AUTH-003, AUTH-004 |
| D95-19 | [Close security and private-data failure modes](https://github.com/primfoundation/prims/issues/41) | 1 | SEC-001, SEC-002, SEC-003, SEC-004 |
| D95-20 | [Migrate incubators and prove compatibility](https://github.com/primfoundation/prims/issues/42) | 5 | INTEROP-001, INTEROP-002, INTEROP-003, RELENG-003 |
| D95-21 | [Cut the public Hub over with verified ownership](https://github.com/primfoundation/prims/issues/43) | 4 | OPS-001, OPS-005 |
| D95-22 | [Prove Browsers and consolidate its live services](https://github.com/primfoundation/prims/issues/44) | 4 | OPS-002 |
| D95-23 | [Make recovery, maintenance and free operation sustainable](https://github.com/primfoundation/prims/issues/45) | 1 | OPS-003, OPS-004, RELENG-004 |
| D95-24 | [Establish actual stewardship and policy ownership](https://github.com/primfoundation/prims/issues/46) | 1 | GOV-001, GOV-002, GOV-003, GOV-004 |
| D95-25 | [Deliver useful diagnostics, onboarding and support](https://github.com/primfoundation/prims/issues/47) | 5 | LIFE-003, COMM-001, COMM-002, COMM-005 |
| D95-26 | [Run independent acceptance and close the release](https://github.com/primfoundation/prims/issues/48) | 6 | COMM-003, COMM-004 |

## Executable task index

This is the initial ordering, not live state. Follow the issue for current status.

| Task | Issue | Dependencies | Implementation repository |
| --- | --- | --- | --- |
| EXEC-01 | [Establish the scored release baseline and repair stale summaries](https://github.com/primfoundation/prims/issues/49) | Package entry gate | primfoundation/prims |
| EXEC-02 | [Implement native complete-pack import, edit and export](https://github.com/primfoundation/prims/issues/50) | Package entry gate | primfoundation/prims-paste-desktop |
| EXEC-03 | [Diagnose and complete existing-key encrypted snapshot restore](https://github.com/primfoundation/prims/issues/51) | Package entry gate | primfoundation/prims-paste-desktop |
| EXEC-04 | [Reconcile richer Primboard UI and prove a safe installed upgrade](https://github.com/primfoundation/prims/issues/52) | EXEC-02, EXEC-03 | primfoundation/prims-paste-desktop |
| EXEC-05 | [Build the Research capture, challenge and revision demonstration](https://github.com/primfoundation/prims/issues/53) | Package entry gate | primfoundation/prims |
| EXEC-06 | [Prove the complete investigation across web, native and offline readers](https://github.com/primfoundation/prims/issues/54) | EXEC-02, EXEC-04, EXEC-05 | primfoundation/prims |
| EXEC-07 | [Specify Project work items using Foundation delivery as the reference case](https://github.com/primfoundation/prims/issues/55) | Package entry gate | primfoundation/prims |
| EXEC-08 | [Export GitHub execution records into a versioned Project Prim](https://github.com/primfoundation/prims/issues/56) | EXEC-07 | primfoundation/prims |
| EXEC-09 | [Prove agent handoff and specify conflict-safe Project writeback](https://github.com/primfoundation/prims/issues/57) | EXEC-08 | primfoundation/prims |
| EXEC-10 | [Resolve Desktop source lineage and the 27 legacy host assertions](https://github.com/primfoundation/prims/issues/58) | Package entry gate | primfoundation/prims-desktop |
| EXEC-11 | [Audit and repair the self-service Hub entry journey](https://github.com/primfoundation/prims/issues/59) | Package entry gate | primfoundation/prims-web |
| EXEC-12 | [Implement and test authenticated publisher and namespace lifecycle](https://github.com/primfoundation/prims/issues/60) | Package entry gate | primfoundation/prims |
| EXEC-13 | [Prepare and execute real Browsers login and isolation acceptance](https://github.com/primfoundation/prims/issues/61) | Package entry gate | primfoundation/prims-browsers |
| EXEC-14 | [Prepare the operator and replacement-maintainer recovery rehearsal](https://github.com/primfoundation/prims/issues/62) | Package entry gate | primfoundation/prims |
| EXEC-15 | [Prepare independent usability and release evidence package](https://github.com/primfoundation/prims/issues/63) | EXEC-06, EXEC-11, EXEC-14 | primfoundation/prims |
| EXEC-16 | [Add a GitHub Projects board when project-scoped access is available](https://github.com/primfoundation/prims/issues/64) | Package entry gate | primfoundation/prims |

The Project has All work, Execution board, Ready now, Blocked and waiting, and Packages views. Field updates were tested and restored. [Execution evidence](evidence/2026-09-12-github-project.json) records exact receipts and test limits.