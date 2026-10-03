import assert from "node:assert/strict";
import { test } from "node:test";
import { existsSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createHash } from "node:crypto";
import { ProfileLibrary, parseProfileJSON } from "../src/index.ts";
import { checkProfileSchema } from "../src/profile-schema.ts";
import { HOST_CATALOG_BASE64 } from "../src/profile-data.ts";
import type { JSONValue } from "../src/profile-schema.ts";

test("all 83 independent Python cases agree with the SDK", () => {
  const library = new ProfileLibrary();
  const corpus = JSON.parse(readFileSync(new URL("./fixtures/prim-host-cases.json", import.meta.url), "utf8"));
  assert.equal(corpus.cases.length, 83);
  for (const c of corpus.cases) {
    const kit = library.list().find(k => k.profile_id === c.profile_id)!;
    assert.equal(kit.definition_sha256, c.definition_sha256);
    assert.equal(library.validate(library.pin(kit), c.record).length === 0, c.valid, c.name);
  }
});

test("versions and checksums are exact and returned kits cannot mutate the library", () => {
  const library = new ProfileLibrary(), kit = library.list()[0], pin = library.pin(kit);
  assert.throws(() => library.get({ ...pin, version: "next" }));
  assert.throws(() => library.get({ ...pin, definition_sha256: "0".repeat(64) }));
  assert.throws(() => new ProfileLibrary(Buffer.from("{}"), "0".repeat(64)));
  kit.template.title = "mutated";
  assert.notEqual(library.get(pin).template.title, "mutated");
});

test("duplicate, oversized, nonfinite and deeply nested JSON is rejected", () => {
  for (const input of ['{"a":1,"a":2}', '{"a":1,"\\u0061":2}', '{"a":{"b":1,"b":2}}', '{"n":1e999}', '{"n":9007199254740993}', "[".repeat(25) + "0" + "]".repeat(25)]) assert.throws(() => parseProfileJSON(input));
  assert.deepEqual(parseProfileJSON('{"a":{"id":"a"},"b":{"id":"b"}}'), { a: { id: "a" }, b: { id: "b" } });
});

test("unsupported schema assertions never become a passing validation", () => {
  const unsupported: JSONValue[] = [{ $ref: "https://example.invalid/schema" }, { pattern: ".*" }, { required: "id" }, { allOf: {} }];
  for (const schema of unsupported) assert.throws(() => checkProfileSchema(schema));
});

test("all profiles round-trip as category-compatible packs with extensions preserved", () => {
  const root = mkdtempSync(join(tmpdir(), "prim-sdk-host-")), library = new ProfileLibrary();
  try {
    for (const kit of library.list()) {
      const pin = library.pin(kit), record = library.create(pin, { extension: { preserved: ["漢字", true, false, null, 42] } });
      const target = join(root, kit.profile_id.split("/").at(-1)!);
      library.writePack(pin, record, target);
      assert.deepEqual(library.readPack(target), { pin, record });
      assert.throws(() => library.writePack(pin, record, target));
      const link = target + "-link"; symlinkSync(target, link);
      assert.throws(() => library.readPack(link));
      writeFileSync(join(target, "prim-definition.lock.json"), JSON.stringify({ ...pin, definition_sha256: "0".repeat(64) }));
      assert.throws(() => library.readPack(target));
    }
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("external publisher and source moves need no repository identity or SDK change", () => {
  const catalog = JSON.parse(Buffer.from(HOST_CATALOG_BASE64, "base64").toString());
  const kit = structuredClone(catalog.kits.find((k: {profile_id: string}) => k.profile_id === "primfoundation/person"));
  kit.profile_id = "example-publisher/contact"; kit.name = "External contact";
  // Synthetic fixture explicitly pinned by its caller; no publisher authentication claim.
  kit.definition_sha256 = "a".repeat(64); catalog.kits = [kit]; catalog.source_commit = "external-fixture";
  const data = Buffer.from(JSON.stringify(catalog));
  const library = new ProfileLibrary(data, createHash("sha256").update(data).digest("hex"));
  const loaded = library.list()[0];
  assert.equal(library.validate(library.pin(loaded), library.create(library.pin(loaded))).length, 0);
  assert.equal(loaded.profile_id, "example-publisher/contact");
});

test("prototype-named extension fields remain ordinary data", () => {
  const library = new ProfileLibrary(), kit = library.list().find(k => k.profile_id === "primfoundation/person")!;
  const record = library.create(library.pin(kit), parseProfileJSON('{"__proto__":{"polluted":true},"constructor":"ordinary"}') as any);
  assert.equal(Object.hasOwn(record, "__proto__"), true);
  assert.equal(({} as any).polluted, undefined);
  assert.equal(library.validate(library.pin(kit), record).length, 0);
});

test("exports reject representations the same reader cannot reopen before creating a folder", () => {
  const root = mkdtempSync(join(tmpdir(), "prim-sdk-export-budget-")), library = new ProfileLibrary();
  try {
    const kit = library.list()[0], pin = library.pin(kit);
    const record = library.create(pin, { extension: Array.from({length: 1800}, () => "x".repeat(284)) });
    assert.ok(Buffer.byteLength(JSON.stringify(record)) < 512 * 1024);
    assert.ok(Buffer.byteLength(JSON.stringify(record, null, 2) + "\n") > 512 * 1024);
    const target = join(root, "too-large-after-formatting");
    assert.throws(() => library.writePack(pin, record, target), /size limit/);
    assert.equal(existsSync(target), false);
  } finally { rmSync(root, {recursive: true, force: true}); }
});

test("coding-agent harness template, evidence and recovery validate without granting authority", () => {
  const library = new ProfileLibrary();
  const kit = library.list().find(k => k.profile_id === "primfoundation/coding-agent-harness")!;
  assert.ok(kit);
  assert.equal(kit.version, "0.1.0-dev.1");
  assert.equal(kit.authority_file, "harness.json");
  const pin = library.pin(kit);
  const source = new URL("../../../profiles/coding-agent-harness/", import.meta.url);
  const template = JSON.parse(readFileSync(new URL("template.json", source), "utf8"));
  const example = JSON.parse(readFileSync(new URL("examples/minimal/harness.json", source), "utf8"));
  const schema = JSON.parse(readFileSync(new URL("schema/record.schema.json", source), "utf8"));
  assert.deepEqual(kit.template, template);
  assert.deepEqual(kit.schema, schema);
  assert.deepEqual(library.validate(pin, template), []);
  assert.deepEqual(library.validate(pin, example), []);
  assert.equal(library.create(pin).status, "draft");
  const draft = structuredClone(template);
  draft.extension = { caller_owned: true };
  assert.deepEqual(library.create(pin, draft).extension, draft.extension);

  for (const [field, bad] of [["profile", "other/harness"], ["profile_version", "1.0.0"], ["kind", "tool-evaluation"]]) {
    assert.ok(library.validate(pin, { ...example, [field as string]: bad }).length, String(field));
  }
  for (const collection of ["capabilities", "components", "capability_links", "evidence", "evaluations", "evaluation_evidence", "observations", "incidents", "procedures", "changes", "verifications"]) {
    const duplicate = structuredClone(example);
    duplicate[collection].push(structuredClone(duplicate[collection][0]));
    assert.ok(library.validate(pin, duplicate).some(p => p.rule === "duplicate_id"), collection);
  }
  for (const [collection, field] of [
    ["capability_links", "component_id"], ["capability_links", "capability_id"],
    ["evaluations", "subject"], ["evaluations", "evidence_id"],
    ["evaluation_evidence", "evaluation_id"], ["evaluation_evidence", "evidence_id"],
    ["observations", "subject"], ["observations", "evidence_id"],
    ["incidents", "subject"], ["incidents", "evidence_id"],
    ["changes", "incident_id"], ["changes", "procedure_id"], ["changes", "evidence_id"],
    ["verifications", "change_id"], ["verifications", "evidence_id"],
  ]) {
    const dangling = structuredClone(example);
    dangling[collection][0][field] = "missing";
    assert.ok(library.validate(pin, dangling).some(p => p.rule === "unresolved_reference"), `${collection}.${field}`);
  }
  for (const score of [-1, 101, 1.5, "70", null]) {
    const bad = structuredClone(example);
    bad.evaluations[0].ratings.confidence = score;
    assert.ok(library.validate(pin, bad).length, `score ${score}`);
  }
  const bad = structuredClone(example);
  bad.constraints.context.max_tokens = -1;
  assert.ok(library.validate(pin, bad).length);
  bad.constraints = {};
  bad.components[0].status = "approved-to-execute";
  assert.ok(library.validate(pin, bad).length);
  const missingEvidence = structuredClone(example);
  delete missingEvidence.evaluations[0].evidence_id;
  assert.ok(library.validate(pin, missingEvidence).length);
  assert.ok(library.validate(pin, { ...template, status: "observed" }).length);
  const malformed = structuredClone(example);
  malformed.observations[0].values = [];
  assert.ok(library.validate(pin, malformed).length);
  // Structural validity can retain an unverified source and narrowly scoped pass.
  assert.equal(example.evidence[0].verification, "unverified");
  assert.equal(example.verifications[0].result, "passed");
});
