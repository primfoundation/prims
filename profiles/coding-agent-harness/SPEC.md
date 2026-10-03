# Coding Agent Harness Prim — 0.1.0-dev.1

Development proposal. Related Foundation requirements: PUB-001 (publishable
profiles), DEV-001 (developer access). This addition claims neither requirement
complete. It follows program/PROFILE-PACKAGE.md and decision D002.

## Purpose and store

Preserve a bounded, evidence-aware description of the environment through which a
coding agent receives context and acts: runtime/provider/version, host/workspace,
capabilities, tools/MCPs, skills, instruction sources, hooks, constraints, measured
health, evaluations, incidents, recovery recommendations and change verification.
Only `coding-agent-harness` is registered. Its components are not new Prim types.

`harness.json` is the authoritative JSON record. A native host exports it with
`prim-definition.lock.json`, `index.md` and `log.md` through the existing creation
kit. The example JSON is a worked record, not by itself a complete exported pack.
The definition lock pins the exact definition; `profile_version` pins record
interpretation. This is not an OKF profile. No claims of OKF conformance, trust
ladder implementation or a required fixed UI are made.

## Identity and unknowns

`profile`, `profile_version`, and `kind` must match the schema constants. `id`
identifies one harness record; authors must replace the template's `harness.new`
with their own identity before saving a distinct record. IDs within each collection
are unique, case-sensitive strings. They are scoped to that collection, not a
universal registry. Cross-pack uniqueness is not checked.

The template is a structurally valid `draft`: unknown runtime, host, workspace and
observation time are null. `observed` requires a runtime name and observation time,
not a claim that the environment is complete or independently verified.
`superseded` retains historical interpretation. Empty collections mean nothing
recorded, never proof that a capability, issue, or risk is absent.

Times should use RFC 3339 with an explicit UTC offset. The shared schema vocabulary
checks bounded nonempty strings, not timestamp syntax, timezone arithmetic or
freshness. Readers must treat unparseable dates as unknown, never fresh. Unknown
optional information may be omitted; nullable fields distinguish unknown from a
measured zero. Unknown JSON properties are preserved for additive evolution but
have no profile-defined reference or executable semantics.

## Collections and references

The schema defines structure; `creation.json` defines relational checks. Both are
required for a profile validation result. Plain JSON Schema validation alone does
not reject duplicate IDs or dangling references.

| Collection | Meaning and checked references |
| --- | --- |
| `capabilities` | Declared capability kind, access and availability; not permission. |
| `components` | Runtime, tool/provider, MCP server, skill, instruction source, hook or process; version/locator and estimated context cost are optional. |
| `capability_links` | One component-to-capability association per row. |
| `evidence` | Bounded claim, source, time, verification state, and optional method/limitations. |
| `evaluations` | Component subject, evaluator/task/environment scope, time, method and 0–100 ratings. |
| `evaluation_evidence` | Links an evaluation to supporting, contradicting or qualifying evidence. |
| `observations` | Component subject (null means whole harness), typed scalar measurements, units, time and evidence. |
| `incidents` | Component subject (or whole harness), summary, time, state and evidence. |
| `procedures` | Recovery recommendations, preconditions, recorded authority, rollback and verification plan; never executable instructions on open. |
| `changes` | Proposed/applied/reverted/failed/unknown change, nullable incident/procedure references and evidence. |
| `verifications` | Change reference, test time, result, exact scope and evidence. |

All non-null declared internal references must resolve. Every collection checks
ID uniqueness. Component-capability membership and evaluation evidence use explicit
link collections so the existing Python and TypeScript validators can check them.
Recovery collections are top-level rather than nested under `recovery` for the same
reason; no runtime-specific validation engine is needed.

## Evaluations, evidence and health

Ratings are optional integers from 0 to 100. Popularity describes recorded adoption
or exposure within a stated population; importance describes the evaluator's
priority; liking and disliking are separate positive/negative personal affinities;
task_fitness is suitability for the scoped task; confidence is confidence in that
evaluation. None is a probability, security certification or permission. A missing
rating is unknown, not zero. Do not average these into a universal quality score.
Use the method and limitations to document population, scale and collection method.
The synthetic example's scores are fabricated illustration, not real popularity.

Every evaluation identifies its primary evidence; additional links can preserve
counterevidence or qualifications. Evidence sources are bounded opaque locators or
attribution text, not internal IDs and never automatically fetched. A source may be
unavailable; its citation alone does not establish support. Do not put signed URLs,
credentials or private user details in public examples. Refer to authorized external
artifacts instead of embedding unbounded tool outputs or transcripts.

Verification vocabulary records `unverified`, `observed`, `reproduced`,
`contradicted` or `inconclusive`. These are producer assertions, not certifications.
A recorded assertion can be wrong. A test passing for configuration syntax says
nothing about loaded runtime, production deployment or cause of an incident.

Observations can represent token estimates, tool counts, latency, failure/loop
counts, drift or owned-process state using bounded scalar `values` and explicit
`units`. Context cost must state its estimation basis. Mixed units should use
separate observations. Define nonstandard measurement names and units in evidence
method text. Keep host/workspace scope explicit; compare compatible observations,
not snapshots from unrelated machines or task populations. A process component is
an observation of a process, not ownership or permission to terminate it.

## Authority, privacy and safety

`constraints` records context/execution limits and `policy_as_recorded`.
`authority_as_recorded` on changes and procedures describes provenance only.
Capabilities and policies do not grant execution authority. Opening, validating or
rating this file must not execute a hook, load code, call an MCP, fetch an artifact,
terminate a process, disable a component or apply a repair. Operators obtain
separate authorization on the exact live host/workspace/action surface.

Do not store secret values, tokens, OTPs or ephemeral credentials. Sensitive paths
should use sanitized hints. Consumers still need appropriate access controls;
structural validation does not detect all secrets or authorize publication.
Corrections retain provenance; retention/redaction follow the owner's policy.
This version specifies no automatic merge, locking, execution or recovery service.

## Validation and worked example

Reject wrong profile/version/kind, missing required fields, malformed typed rows,
unknown enum values, out-of-range scores/budgets, duplicate collection IDs and
dangling declared references. Arrays have 1,000-row limits. Shared hosts also bound
record size, nesting and JSON containers; this is a knowledge pack, not a log sink.
Additional properties are preserved without interpreting new reference fields.

`template.json` is a valid empty draft. `examples/minimal/harness.json` is wholly
synthetic and exercises capability linkage, evaluation evidence, context estimates,
a hook incident, a proposed recovery procedure, a recorded change and narrowly
scoped verification. Its assertions are deliberately not real-machine evidence.

Run profile discovery, Library/host catalog regeneration and both Python Library
and TypeScript profile tests. Manifest inspection checks metadata and paths only.
Full record validation checks structure and declared relations, not timestamp
validity, truth, source availability, authorization, causal attribution, completeness,
publisher identity or independent operational acceptance. Keep those limits visible.
