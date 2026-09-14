# Prim Family Map

Prim is the category: a file that stores information, and tools that interact with it. Some profiles use OKF as their grammar. They do not have to. Prim can evolve without being OKF.

The live list of **types**, **tools**, and **applets** is [`registry/registry.json`](./registry/registry.json). This map is a sketch. `prim registry` prints the catalog. Applets are compositions (they cite types; they may cite tools). They are not a tool kind.

**Repository naming convention**

| Pattern | Role |
|---------|------|
| `prim` | Category home (this repo) |
| `prim.<profile>` | Domain profile (spec, validator, examples) |
| `prim-web` | Public web host (`as: host`, cites `*`) |
| `prim-mac` | Mac document host — Prim.app. The way a `.prim` opens on a Mac |

Examples: `prim.ocsf`, `prim.brand`, `prim.osf`, `prim.orf`.

---

## Family at a glance

```
prim              Category / product identity
                  https://github.com/eidos-agi/prim

prim-web          Public web host (`as: host`, cites `*`)
                  https://github.com/eidos-agi/prim-web

prim-mac          Mac document host — Prim.app. The way a .prim opens on a Mac.
                  Surface / talk / as host / cites *. The pack stays the file.

Profiles (OKF-shaped unless noted)
│
├── prim.emf      Human intent + durable memory + `emf-editor`
├── prim.orf      Research / investigation packs + `orf-editor`
├── prim.opf      Product graph + `opf-editor`
├── prim.odwf     Spreadsheet → bronze proof packages + `odwf-editor`
├── prim.opff     Personal / household finance packs + `opff-editor` (surface / talk, as ledger)
├── prim.omf      Meeting occurrences + `omf-editor` (surface / talk)
├── prim.ocsf     Corporate structure, ownership, capital, governance + `ocsf-editor`
├── prim.brand    Brand kit (identity, tokens, logos, fonts, running blocks). Not OKF. Retired: prim.obif. `prim-viewer` cites it; no separate editor yet.
├── prim.osf      Open Session Format (movable session packs) + `osf-editor`
├── prim.obf      Open Book Format + `obf-editor`
├── prim.docket   Execution prim + first Prim Tool (`docket-editor`, surface / talk)
├── prim.deck     Slide records + `deck-editor` (emerging, not OKF)
├── prim.invoice  Bill pack + `invoice-editor` (emerging, not OKF)
├── prim.session  Thin transcript + `session-editor` (emerging; not OSF)
├── prim.log      Append-only debug / run log + `log-editor` / `prim-sim` (emerging; the log primitive as a file)
├── prim.scene    One cinematic beat. scene.json is authority. The mp4 is a view. (emerging, not OKF)
├── prim.video    Ordered collection of prim.scene packs. Compose, don't merge. (emerging, not OKF)
├── prim.album    One record. album.json is tracks and metadata. The player is a view. (emerging, not OKF)
├── prim.workbook Workbook — ordered worksheets (Alex expected + SQL actuals). Cites measure/metric. Proof/provenance. `workbook-editor` (emerging, not OKF)
├── prim.worksheet One sheet face; rows cite measure/metric or structure-only (emerging; often embedded)
├── prim.measure  Durable identity / definition for a KPI (emerging; may embed in workbook)
└── prim.metric   Period series + proof receipts for a measure (emerging; may embed in workbook)

First connector: docket-webmcp (WebMCP). Validates a docket; does not feed contents to a model unless exposed. Category connector: prim-viewer-webmcp — the player registers WebMCP tools so a model can operate any open prim.

Prim Arcade (`prim-arcade`) is a surface tool on an `arcade` prim. The cart is the file. JSNES embeds in chat.

`album-player` is a surface tool on an `album` prim. The record is the file. Not slides (`prim.deck`).

Base grammar + render
│
└── okflify       OKF pack → HTML / base knowledge + trust model
                  https://github.com/eidos-agi/okflify
```

Profile short names (EMF, ORF, OCSF, …) remain valid in technical and agent contexts.  
Repo names and everyday speech prefer the `prim` / `prim.<profile>` form.

---

## Roles

| Layer | Responsibility |
|-------|----------------|
| **prim** | Category name, positioning, shared properties, language, packaging |
| **OKF** (via okflify and profile bases) | One pack grammar: face, provenance, trust. Optional. |
| **prim.\*** profiles | Domain store and rules. May be OKF-shaped or not. |
| **prim-web** | Public web host. Views on demand. Never the source of truth |
| **prim-mac** | Mac document host (Prim.app). Double-click, Open, Save. Hosts citing tools; not a pack type |
| **Validators** | Enforce profile rules; fail-closed where specified. Register on the category SDK. |
| **Prim UIs** | View plugins keyed `profile/subtype`. How a Prim *opens*. Never the file. |
| **Prim Tools** | Operators on a Prim. Two kinds: **surface** (human counterpart) and **connector** (system counterpart). Cite a Prim. Not a pack type. The category player is **`prim-viewer`** (`<show-prim filename="yadda.prim">`). The category connector on that player is **`prim-viewer-webmcp`**. |

Category primitives (file, face, authority, constraint, log, validator, ui, compose, trust) live in the TypeScript Prim SDK (`sdk/typescript`). See SPEC §9.

Prim Tools are category language, not a family of repos. Do not mint `prim.surface` or `prim.connector`. See SPEC §10.

---

## Composition rules

1. **OKF-shaped prims stay OKF-compatible.** A renderer that understands only OKF can display those packs and ignore extra keys.
2. **Not every Prim is OKF.** A profile may name another store. `docket-md` stays markdown. `docket-prim` (`prim.docket`) is the new-format execution prim.
3. **Profiles do not merge domains by default.** Corporate structure stays in OCSF. Research stays in ORF. Execution stays in the docket. Cross-references are preferred over forced unification.
4. **Evidence and trust follow the profile.** OKF profiles use the OKF ladder. Other profiles do not inherit it by default.
5. **Human intent stays in EMF** (`prim.emf`) where that distinction matters.

---

## How to talk about them

| Context | Preferred language |
|---------|-------------------|
| Everyday / human | “the prim”, “send me the prim”, “latest prim” |
| Profile precision | “the brand prim”, “the corporate prim”, “prim.brand”, “prim.ocsf” |
| Technical / agent | `profile: brand`, `profile: ocsf`, pack path / repo name |

The goal is that **prim** is the default noun. Profile codes and `prim.*` repo names appear when precision is needed.

---

## In-repository profile packages

[`coding-agent-harness`](./profiles/coding-agent-harness/PROFILE.md) stores the
effective coding-agent environment and its evidence, evaluations, incidents and
recovery records. It is a development JSON profile, not an executable tool or OKF
profile. Its identity is `primfoundation/coding-agent-harness` and its existing
source repository is `primfoundation/prim`.

The newer [profile package contract](./program/PROFILE-PACKAGE.md) and D002 permit
multiple profiles in one repository. The `prim.<shortname>` repository pattern
below remains useful for separately hosted profiles, not a requirement to create
a repository for each package. Existing profile identities remain unchanged.

## Adding a new profile

A new domain becomes part of the Prim family when:

1. It names a store and how tools cite it (kinds, gates, layout — OKF or not).
2. It respects the category split: the file stores; tools interact; no fixed UX required.
3. It has an identified source location. A separate repository may use
   `prim.<shortname>`; an in-repository package follows the profile package contract.
4. It is linked from this family map and from the Prim README.

The Prim category SPEC does not need to change for every new profile. The family map does.

A new renderer, print host, bake job, or warehouse reader is a **Prim Tool**, not a new profile. If it is not surface or connector, it is a script. Do not add it here.

---

## Status

This map reflects the `prim` / `prim.*` repositories in the Eidos org as of the current draft. It will be updated as profiles mature and new ones are added.

---

## License

MIT — Eidos AGI
