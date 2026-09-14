# Prim

**A file that stores information, and tools that interact with it.**

There are Prims and Prim Tools.

**Prims** are the store: files both agents and humans can use without scraping a sheet or a deck. Traditional documents (Excel, Word, PDFs, decks) become projections.

**Prim Tools** operate on a Prim. Two kinds: surface (human counterpart) and connector (system counterpart). A tool cites the file. It is not a Prim.

OKF is one grammar some prims use. Prim can evolve without being OKF.

> “Send me the prim.”

That should feel as natural as “send me the link” or “drop the JSON.”

**New here?** Read [WHAT-IS-PRIM.md](./WHAT-IS-PRIM.md) — the complete explanation and how to talk about it.

## Why Prim exists

Most knowledge today lives in application-specific files:

- Spreadsheets for structure
- Documents for narrative
- Decks for presentation
- Notes for memory

None of these were designed for agents. They require constant translation, re-interpretation, and re-derivation.

**Prims invert this.**

The store *is* the file. Interfaces are generated or operated on the fly. OKF is optional. Pure data formats (images, Parquet, etc.) remain specialized. Everything else can become a view of a Prim.

## Core properties

- **Store + interact** — the file stores; a surface or connector cites it
- **AI-native** — agents open the store without scraping a presentation format
- **Durable** — outlives a session
- **Human-inspectable** — still openable by people
- **No fixed UX** — `ui` opens; a Prim Tool operates
- **OKF optional** — evidence, trust, fail-closed are profile rules when the domain is claims

## Packaging

| Form | Role |
|------|------|
| **Directory pack** | Canonical source of truth (git, editing, validation) |
| **`.prim.zip`** | Primary interchange — “send me the prim” |
| **`.prim.tar.gz`** | Allowed, Unix/agent-friendly |
| **`.prim`** | Reserved branded container (zip-compatible) |

A `.prim.zip` or `.prim` is simply a zip whose root is a valid Prim pack.  
See [SPEC.md §5](./SPEC.md) for the full packaging rules.

## Naming

| Pattern | Role |
|---------|------|
| **`prim`** | This repo — category home |
| **`prim.<profile>`** | Domain profile (spec + validator + examples) |
| **`prim-web`** | Public web host (`as: host`) |
| **`prim-mac`** | Mac document host — Prim.app. The way a `.prim` opens on a Mac |
| **Prim Tool** | Operator on a Prim — **surface** (human) or **connector** (system). Not a repo pattern. |

Examples: `prim.ocsf`, `prim.brand`, `prim.osf`, `prim.orf`. There is no `prim.surface` or `prim.connector`.

## The Prim family

| Repo | Domain |
|------|--------|
| [prim](https://github.com/primfoundation/prim) | Category identity (this repo) |
| prim-web | Public web host / views (not yet public) |
| prim-mac | Mac document host — Prim.app (not yet public) |
| prim.emf | Human intent + durable memory (not yet public) |
| [prim.orf](https://github.com/eidos-agi/prim.orf) | Research / investigation |
| [prim.opf](https://github.com/eidos-agi/prim.opf) | Product graph |
| [prim.odwf](https://github.com/eidos-agi/prim.odwf) | Spreadsheet → bronze proof |
| [prim.opff](https://github.com/eidos-agi/prim.opff) | Personal finance + `opff-editor` (surface / talk, as ledger) |
| [prim.omf](https://github.com/eidos-agi/prim.omf) | Meeting occurrences |
| [prim.ocsf](https://github.com/eidos-agi/prim.ocsf) | Corporate structure & capital |
| [prim.brand](https://github.com/eidos-agi/prim.brand) | Brand kit |
| [prim.osf](https://github.com/eidos-agi/prim.osf) | Open Session Format |
| [prim.docket](https://github.com/eidos-agi/prim.docket) | Execution prim + first Prim Tool (`docket-editor`, surface / talk) |
| prim.deck | Slide records + `deck-editor` (emerging) |
| prim.invoice | Bill pack + `invoice-editor` (emerging) |
| prim.session | Thin transcript + `session-editor` (emerging; not OSF) |
| [prim.scene](https://github.com/eidos-agi/prim.scene) | One cinematic beat. `scene.json` is authority (emerging) |
| [prim.video](https://github.com/eidos-agi/prim.video) | Ordered collection of `prim.scene` packs (emerging) |
| [prim.album](https://github.com/eidos-agi/prim.album) | One record. `album.json` is tracks and metadata (emerging) |

OKF provides the grammar ([okflify](https://github.com/eidos-agi/okflify)).  
**Prim** is what people call the thing.

See [FAMILY.md](./FAMILY.md) for composition rules and how to talk about profiles.

## Coding-agent harness profile

[`profiles/coding-agent-harness`](./profiles/coding-agent-harness) defines a
development knowledge pack for coding-agent environments, constraints, evaluations,
operational evidence and recovery records. It is registered as
`coding-agent-harness`; its portable identity is
`primfoundation/coding-agent-harness`. It is a JSON store, not an executable
control plane or an OKF conformance claim.

## Language

- “Send me the prim.”
- “Is that the latest prim?”
- “Don’t send the spreadsheet — just send the prim.”
- “The prim is the source of truth. The deck is just a view.”
- “Brand prim” / `prim.brand` when you need the profile.
- “There are prims and prim tools.”
- “A surface tool on this prim.” / “A connector that cites this prim.” — not a new pack type.

Full communication guide: [WHAT-IS-PRIM.md](./WHAT-IS-PRIM.md).

## Documents in this repo

| File | Purpose |
|------|---------|
| [WHAT-IS-PRIM.md](./WHAT-IS-PRIM.md) | **Start here** — complete public explanation and how to talk about it |
| [WHY-PEOPLE-NEED-PRIMS.md](./WHY-PEOPLE-NEED-PRIMS.md) | Proposed `prim.*` profiles for people — home, vehicle, health, career, trip, estate, lineage |
| [INTENTION.md](./INTENTION.md) | North-star design commitments |
| [SPEC.md](./SPEC.md) | Category specification (what makes a Prim; Prim Tools in §10) |
| [FAMILY.md](./FAMILY.md) | Map of `prim.*` profiles |
| [registry/registry.json](./registry/registry.json) | **Registry** — Prim types, Prim Tools, and applets |
| [tools/prim-viewer/](./tools/prim-viewer/) | Category player — `<show-prim filename="yadda.prim">`. React: `@eidos-agi/prim-viewer/react`. Next: `@eidos-agi/prim-viewer/next`. WebMCP: `prim-viewer-webmcp`. |
| [BRAND.md](./BRAND.md) | Identity, language, and positioning |
| [sdk/typescript/](./sdk/typescript) | Category SDK (open, face, validate, write) |
| [examples/](./examples/) | Illustrative packs and references |

## Status

Early. Types, tools, and applets are listed in [`registry/registry.json`](./registry/registry.json). `prim registry` prints them. Domain profiles live in `prim.<name>` repositories. They do not have to be OKF. Applets are compositions, not a third tool kind.

## License

MIT — Eidos AGI
