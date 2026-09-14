import assert from "node:assert/strict";

import {
  getApplet,
  getTool,
  getType,
  listApplets,
  listTools,
  listTypes,
  registerApplet,
  registerTool,
  registerType,
  registry,
  resetRegistry,
} from "../src/registry.ts";

resetRegistry();
assert.equal(getType("coding-agent-harness")?.repo, "primfoundation/prim");
assert.equal(getType("coding-agent-harness")?.okf, false);
assert.equal(getType("coding-agent-harness")?.status, "emerging");

assert.ok(listTypes().length >= 1);
assert.ok(getType("docket"));
assert.equal(getType("docket")?.okf, false);
assert.ok(getType("deck"));
assert.equal(getType("deck")?.okf, false);
assert.ok(getType("invoice"));
assert.ok(getType("session"));
assert.equal(getType("session")?.okf, false);
assert.ok(getType("osf"));
assert.equal(getType("osf")?.okf, true);
assert.ok(getTool("deck-editor"));
assert.equal(getTool("deck-editor")?.cites, "deck");
assert.ok(getTool("invoice-editor"));
assert.ok(getTool("session-editor"));
assert.ok(getType("arcade"));
assert.equal(getType("arcade")?.okf, false);
assert.ok(getType("log"));
assert.equal(getType("log")?.okf, false);
const sim = getTool("prim-sim");
assert.ok(sim);
assert.equal(sim.kind, "surface");
assert.equal(sim.cites, "log");
assert.equal(sim.as, "sim");
const arcade = getTool("prim-arcade");
assert.ok(arcade);
assert.equal(arcade.kind, "surface");
assert.equal(arcade.cites, "arcade");
assert.equal(arcade.as, "arcade");
const viewer = getTool("prim-viewer");
assert.ok(viewer);
assert.equal(viewer.kind, "surface");
assert.equal(viewer.direction, "talk");
assert.equal(viewer.counterpart, "human");
assert.equal(viewer.cites, "*");
assert.equal(viewer.as, "viewer");
assert.equal(viewer.repo, "eidos-agi/prim");
assert.equal(listTools({ cites: "*" }).length, 4);
const listed = getTool("docket-editor");
assert.ok(listed);
assert.equal(listed.kind, "surface");
assert.equal(listed.direction, "talk");
assert.equal(listed.counterpart, "human");
assert.equal(listed.cites, "docket");
assert.equal(listed.as, "editor");
assert.equal(listTools({ kind: "surface", cites: "docket" }).length, 1);
const ledger = getTool("opff-editor");
assert.ok(ledger);
assert.equal(ledger.kind, "surface");
assert.equal(ledger.direction, "talk");
assert.equal(ledger.counterpart, "human");
assert.equal(ledger.cites, "opff");
assert.equal(ledger.as, "ledger");
assert.equal(listTools({ kind: "surface", cites: "opff" }).length, 1);
assert.equal(listTools({ as: "ledger" })[0]?.name, "opff-editor");
assert.ok(getType("opff")?.okf);
const meeting = getTool("omf-editor");
assert.ok(meeting);
assert.equal(meeting.kind, "surface");
assert.equal(meeting.direction, "talk");
assert.equal(meeting.cites, "omf");
assert.equal(meeting.as, "editor");
assert.equal(listTools({ kind: "surface", cites: "omf" }).length, 1);
for (const [name, cites] of [
  ["emf-editor", "emf"],
  ["orf-editor", "orf"],
  ["opf-editor", "opf"],
  ["odwf-editor", "odwf"],
  ["ocsf-editor", "ocsf"],
  ["osf-editor", "osf"],
  ["obf-editor", "obf"],
  ["log-editor", "log"],
]) {
  const tool = getTool(name);
  assert.ok(tool, name);
  assert.equal(tool.cites, cites);
  assert.equal(tool.as, "editor");
}
const mcp = getTool("docket-webmcp");
assert.ok(mcp);
assert.equal(mcp.kind, "connector");
assert.equal(mcp.direction, "talk");
assert.equal(mcp.counterpart, "system");
assert.equal(mcp.cites, "docket");
assert.equal(mcp.as, "webmcp");
assert.equal(listTools({ kind: "connector", cites: "docket" }).length, 1);
const viewerMcp = getTool("prim-viewer-webmcp");
assert.ok(viewerMcp);
assert.equal(viewerMcp.kind, "connector");
assert.equal(viewerMcp.direction, "talk");
assert.equal(viewerMcp.counterpart, "system");
assert.equal(viewerMcp.cites, "*");
assert.equal(viewerMcp.as, "webmcp");
assert.equal(listTools({ kind: "connector", cites: "*" }).length, 1);

assert.equal(registry().version, 2);
assert.ok(Array.isArray(registry().applets));
assert.ok(listApplets().length >= 1);
const pavo = getApplet("pavo");
assert.ok(pavo);
assert.equal(pavo.name, "Pavo");
assert.equal(pavo.repo, "eidos-agi/pavo");
assert.equal(pavo.status, "active");
assert.deepEqual([...pavo.prims], ["opf"]);
assert.deepEqual([...pavo.tools], []);
assert.equal(listApplets().some((a) => a.id === "pavo"), true);
assert.equal(getApplet("bindings-only"), undefined);

const extra = registerType({
  name: "demo",
  repo: "eidos-agi/prim.demo",
  description: "test only",
  okf: false,
  status: "emerging",
});
assert.equal(extra.name, "demo");
assert.throws(() =>
  registerType({
    name: "demo",
    repo: "eidos-agi/prim.demo",
    description: "dup",
    okf: false,
    status: "emerging",
  }),
);
assert.throws(() =>
  registerTool({
    name: "orphan",
    kind: "surface",
    direction: "talk",
    cites: "missing",
  }),
);
const tool = registerTool({
  name: "demo-talk",
  kind: "surface",
  direction: "talk",
  cites: "demo",
});
assert.equal(tool.counterpart, "human");
assert.throws(() =>
  registerTool({
    name: "demo-talk",
    kind: "surface",
    direction: "talk",
    cites: "demo",
  }),
);
const applet = registerApplet({
  id: "demo-app",
  name: "Demo applet",
  summary: "test only",
  repo: "eidos-agi/prim.demo",
  status: "emerging",
  prims: ["demo"],
  tools: ["demo-talk"],
});
assert.equal(applet.id, "demo-app");
assert.deepEqual([...applet.prims], ["demo"]);
assert.throws(() =>
  registerApplet({
    id: "demo-app",
    name: "dup",
    summary: "dup",
    repo: "eidos-agi/prim.demo",
    status: "emerging",
    prims: ["demo"],
    tools: [],
  }),
);
assert.throws(() =>
  registerApplet({
    id: "orphan-app",
    name: "Orphan",
    summary: "missing prim",
    repo: "eidos-agi/prim.demo",
    status: "emerging",
    prims: ["missing"],
    tools: [],
  }),
);
resetRegistry();
assert.equal(getType("demo"), undefined);
assert.equal(getApplet("demo-app"), undefined);
assert.ok(getTool("docket-editor"));
assert.ok(getApplet("pavo"));
console.log("registry.test.ts ok");
