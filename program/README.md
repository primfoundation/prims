# Prim Foundation delivery program

This is the durable record of the Foundation-wide build authorized on September 6, 2026. Research is the first implementation path, not the boundary of the mission.

**September 11 delivery target:** [DELIVERY-95.md](DELIVERY-95.md) provides the
26-package execution order toward 95%, critical acceptance gates, proposed
outcome rubric and exact next steps. The [Fleet/source audit](evidence/2026-09-11-delivery-audit.json)
confirms Mac access and a local Desktop dependency candidate while preserving
source-rights, dirty-work and installed-release gates. Package assignments live
in `plan.json` and are checked with the existing program command.

**Current publication state:** Foundation bootstrap, ORF compatibility, Library/MCP alpha and sanitized Workbook migration are merged in PRs #5/#6/#7/#10. Verified Hub, Browsers, Primboard, Desktop proof-preflight and organization policy increments are also merged in their owning repositories. `HANDOFF.md` and `evidence/2026-09-07-execution.json` record exact tested commits, CI and unresolved gates. The isolated Cloudflare Hub workbench is deployed; Primboard encrypted-index and recovery changes are merged. See `evidence/2026-09-08-release.json` for exact release evidence. Production cutover, stable/signed releases and independent real-use acceptance remain open.

The later September 8 increments are in `evidence/2026-09-08-portable-delivery.json`: Foundation PR #15 portable hosts, Primboard PR #5 native editing/recovery and Hub PRs #11/#12 actual browser downloads and legacy registry compatibility. `GOAL-STATUS.md` and `REMAINING-GATES.md` describe the remaining scope.

## Execution queue

[GitHub tracker #9](https://github.com/primfoundation/prims/issues/9) now links the 26 delivery packages and a bounded executable queue. [TASK-SYSTEM.md](TASK-SYSTEM.md) defines operational ownership, evidence and Project Prim adoption; `github-execution.json` maps issues to the unchanged canonical requirements. GitHub owns task state; `plan.json` owns requirement state.

## One record, several views

Primboard's subsequent safe Mac candidate tooling and encrypted process-crash
journal are recorded in `evidence/2026-09-08-primboard-journal.json`. They add
software recovery proof; signed installed acceptance and physical power-loss
validation remain open.

| Record | Authority and purpose |
| --- | --- |
| `CHARTER.md` | Mission, outcomes, boundaries, and decisions reserved for human authority. |
| `plan.json` | Canonical workstreams, requirements, milestones, dependencies, status, and evidence references. |
| `../ROADMAP.md` | Generated human view of the plan; never an independently maintained checklist. |
| `DECISIONS.md` | Accepted direction, reversible implementation choices, and unresolved decisions. |
| `BASELINE.md` | Observed repository state, read scope, and migration constraints. |
| `evidence/` | Dated commands/results, tested file hashes, limitations, and release evidence. |
| `HANDOFF.md` | Current bounded work, publication evidence, next step, and overlap warnings. |
| `DELIVERY-95.md` | Detailed execution work orders, critical gates and proposed acceptance rubric; no duplicate requirement status. |

GitHub issues and PRs are coordination surfaces referencing requirement IDs, not another canonical roadmap. Conversations propose changes; reviewed repository changes preserve them. Private source material, credentials, personal records, and sensitive operating details do not belong in this public program record.

## Definition of progress

A requirement is `planned`, `in_progress`, `blocked`, `in_review`, or `complete`. Implementation, testing, review, release, deployment, and real-use verification are separate evidence stages. Each requirement specifies the stages needed before completion. The checker rejects broken references, dependency cycles, unsupported status, and missing required evidence for completed work. It does not independently authenticate an evidence report or establish that its claims are true.

A milestone is complete only when all its requirements and acceptance gates are met. Deferral remains visible with a reason. Scope removal needs a recorded decision; deleted requirements are detectable in Git review, not magically prevented by a single-file validator. There is no equal-weight task percentage presented as mission completion.

## Commands

From the repository or this standalone change-set root:

```bash
python -m pip install -r tools/requirements.txt
python -m unittest discover -s tools/tests -v
python tools/program.py check
python tools/program.py render --check
python tools/profile_catalog.py inspect profiles/research
python tools/orf_conformance.py
python tools/incubator_conformance.py
python tools/profile_catalog.py discover profiles --check registry/profiles.generated.json
```

After changing the source ledger, regenerate with `python tools/program.py render`.
After changing a profile manifest, regenerate with
`python tools/profile_catalog.py discover profiles --output registry/profiles.generated.json`.

The reference publication tooling is local-first and intentionally separate from the existing TypeScript SDK and the pre-existing `sdk-python` branch. It is not a second production SDK or a commitment to Python as the ecosystem's runtime. Cross-language integration and packaged release tests remain ledger obligations.

The program initially uses JSON and Markdown: durable, portable records now, not a fabricated claim of Project Prim conformance. A later reference Project Prim may adopt this record through an explicit migration. A future website can render the same data without owning it.

## Execution policy

Read the charter, baseline, decisions, and handoff before changing the program. Use identifiable branches and bounded changes. Preserve existing formats and consumers. Do not force-push, archive repositories, change production, publish packages, or start paid unattended work as incidental cleanup. Implementation leadership does not confer unlimited governance, spending, or data-access authority.

The first Research acceptance path is: publish a definition; discover and pin it; create an investigation; validate what can actually be checked; open it in another implementation; challenge and revise it; export a view; and preserve legacy ORF data. A manifest parser alone does not complete that path.