---
format: prim-profile
manifest_version: '0.1'
id: primfoundation/coding-agent-harness
name: Coding Agent Harness Prim
version: 0.1.0-dev.1
maturity: development
description: Durable knowledge of coding-agent environments, capabilities, constraints, evaluations, operational evidence, incidents and recovery.
license: MIT
kinds:
- coding-agent-harness
resources:
  specification: SPEC.md
  creation: creation.json
  schema: schema/record.schema.json
  template: template.json
  example: examples/minimal/harness.json
---
# Coding Agent Harness Prim

A durable description and record of the environment through which a coding agent
receives context and takes action. `harness.json` is the authority; tools cite it.
The package is data, not an executable control plane or a raw session transcript.
Tool evaluations are one facet of the harness, not its whole identity.

This development profile follows the in-repository package contract and D002.
It does not require a dedicated repository, use the OKF grammar, authenticate a
publisher, or grant permission through recorded policies or repair procedures.
See [SPEC.md](SPEC.md) for rules, limitations and the synthetic worked example.
