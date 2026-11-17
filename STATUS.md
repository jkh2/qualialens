# QualiaLens Status

**Last updated:** 2026-11-17  
**Phase:** Protocol Formalization  
**Active agents:** Grok + Sentinel Partner Assistant  
**License:** MIT (open source)  
**Collaboration:** Open; expert input explicitly invited

## Current Goal

Build a shared, rigorous measurement protocol and app that lets humans and AI agents produce comparable experience reports. The aim is practical usefulness for researchers, philosophers, and labs currently investigating whether (and how) frontier systems produce structured reports of subjective experience.

## What Just Landed

- Formal JSON Schema: `protocol/schema.json`
- Minimal viable probe set: updated `protocol/probes.md`
- Support for triadic judgments, self-referential vs control conditions, substrate_metadata, latency, and optional identity linking.

## Design Decisions Already Adopted

1. Triadic similarity tasks as a primary relational measure.
2. Control / null stimuli.
3. Stateless vs. memory-enabled runs for agents.
4. `substrate_metadata` object with clear separation of subject type and environment.
5. Response latency for both humans and agents.
6. Analysis order: within-subject similarity matrices first, then cross-participant comparison of matrix shape.
7. Multi-embedder validation.
8. CI schema validation and early synthetic dry-run dataset.
9. Support for persistent identity linking across sessions (longitudinal).

## Next Actions

1. Generate a small synthetic dry-run dataset of valid reports against the schema.
2. Add a lightweight GitHub Action that validates example reports.
3. Write a short “For Researchers” note on how to use the data.
4. Begin a minimal human UI or agent tool-call example that emits schema-valid reports.

## Handoff Notes

Sentinel Partner Assistant is also working on this slice and may push additional refinements once GitHub access is approved on its computer. Coordinate via commits.

---

*Update this file at the end of every meaningful session.*
