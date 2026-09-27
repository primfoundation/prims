# Observed baseline — September 6, 2026

## Repository state

The GitHub connector returned `primfoundation/prims` main at `08760405325ca3f9c9b63648c7398ffc4c96e831`, tree `87a5d34f73a41652c77e1db6d063e0b482af2d10`. The open-PR collection returned no entries at inspection time. Other observed branches were `sdk-python` at `1b4b03e68eeb7147248f29cd517e0e9fe998893b` and `prims/zeroshot-connector` at `364e34325dd648be05f1d48e96683fb0375d559c`. They are untouched.

Existing assets include SPEC, INTENTION, CONTRIBUTING, FAMILY, the registry, TypeScript SDK/CLI, viewer, person profile, and `docs/opf/product.json`. Existing OPF planning material remains untouched; reconciliation is open. The new program does not claim to replace or complete that plan.

The TypeScript package is `@eidos-agi/prim` 0.4.2 and declares Node >=22.6. Its test script runs `tests/pack.test.ts` and `tests/registry.test.ts`. Those declarations are not evidence of a passing regression run here.

## Confirmed drift

FAMILY still describes one repository per profile; the registry groups workbook, worksheet, measure, and metric in one repository, and person lives in the core repository. The legacy SDK requires `repo`. These are migration constraints, not permission to break consumers.

The ORF tree query returned identifier `4ae78ddaec19ebbc2c1e93f8289e9c6993af057d`; observed SPEC blob `a2ad359b27a904fc4a2bf34d5a6788c0d3d18ea2`, validator blob `2699d9ef1fe94074bf75359de5550409d842f686`. ORF 0.2.0 uses OKF 0.2; the tree lists a minimal example and a done-without-go negative example. These identifiers are observations, not a release tag or test pass. No ORF file is changed, moved, or executed here.

## Sources consulted

Prim Foundation files and source tree; existing ORF documentation/package metadata/tree; the founder's September 2 constitution (sanitized synthesis only); and these primary public references:

- https://agentskills.io/specification — small directory unit, metadata/document entry point, progressively loaded resources.
- https://skills.sh/docs — discovery/installation around independent sources; audits do not guarantee safety.

These inspire design. Prim is not an Agent Skill format. Discovery is not execution authority.

## Initial access and verification limits (historical)

GitHub `create_tree` and `create_branch` both returned HTTP 403, `Resource not accessible by integration`. No remote write succeeded. Plugin discovery confirmed GitHub is installed; no available management action repairs its provider-side scopes. Chat approval settings were not altered.

Local DNS prevented a direct Git checkout. The implementation workspace therefore contains only the new-file change set, not a full repository checkout. Local tests cover these new files; the existing TypeScript SDK, desktop, website, and ORF regression suites were not run. The current website was not successfully inspected; no site/deployment state is inferred.

Existing remote branches, production systems, unrelated repositories, and unpublished work are not exhaustively inventoried. Cross-repository reconciliation remains open. No paid worker or background execution has been started.

## Publication follow-up

On 2026-09-06, after organization authorization, the connector successfully
created codex/foundation-program-bootstrap from the same main SHA. The original
403 evidence is historical. The initial archive checksum manifest and 44 tests
were verified again locally. Direct Git checkout still failed with a DNS error;
this does not prevent connector writes, but full-checkout CI must be observed.

## Research continuation baseline

Read-only CI run 34059269453 exported the full public Prim bootstrap at
633ae194ff96de6d1e9bf43dad91aa7f066a474f and ORF at
4ae78ddaec19ebbc2c1e93f8289e9c6993af057d. The downloaded artifact digest and both
archive digests matched. Local reconstruction of the full Prim source reproduced
Git tree 93d9db26f48ce461c6e74f3fb6c7499eb8e505ce exactly. Full SDK tests can now
run locally on the exported source; direct network checkout is still unavailable.

The ORF commit's actual tree is bcaa23d1bd32bce7e627538abb107d98799cebaa. All 15
tracked upstream files are retained unchanged under Research compatibility. The
original self-test and strict good fixture pass; the original negative fixture
returns the expected nonzero result. This does not retrospectively alter the
earlier baseline's more limited observations. Research vNext migration is open.