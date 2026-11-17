# QualiaLens Status

**Last updated:** 2026-11-17  
**Phase:** Foundation / Protocol Design  
**Active agents:** Grok  
**License:** MIT (open source)  
**Collaboration:** Open; expert input explicitly invited

## Current Goal

Establish the shared measurement protocol and data schema so that both the human app and AI agent interface can emit identical report structures. Human implementation comes first; agent access follows the same schema.

## Design Decisions Adopted (from Gemini input)

These are now part of the working design:

1. **Triadic similarity tasks** ("odd-one-out") as a primary relational measure. Produces cleaner distance matrices for Representational Similarity Analysis (RSA) and works identically for human clicks and agent tool calls.
2. **Control / null stimuli** included alongside rich stimuli to establish a baseline floor per participant.
3. **Stateless vs. memory-enabled runs** for agents. Isolates contribution of base model weights versus stored context.
4. **`substrate_metadata` object** in the schema. Strict separation of subject type and environment. AI: model version, temperature, system prompt hash, tools. Human: session context, latency; PII kept in a separate lookup.
5. **Response latency** recorded for both (time-to-first-token / generation duration for models; response time for humans).
6. **Analysis order**: Within-subject similarity matrices first, then compare matrix shapes across participants (Mantel tests or Procrustes alignment). Avoid direct cross-subject embedding comparisons as the primary method.
7. **Multi-embedder validation**: Run analysis with at least two embedding families to check that patterns are not artifacts of a single embedder.
8. **CI schema validation**: GitHub Action to validate reports against the schema.
9. **Synthetic dry-run dataset**: Generate mock human and agent reports early to test the analysis pipeline end-to-end.

## What Exists

- Foundation documents (README, STATUS, CONTRIBUTING).
- Open-source declaration and MIT license.
- Explicit invitation for expert collaboration.
- Methodological recommendations integrated.

## Next Actions

1. **Define the core report schema** (`protocol/schema.md` + formal JSON Schema) incorporating `substrate_metadata`, latency, and support for triadic judgments.
2. **Draft initial probe set** refinements in `protocol/probes.md`.
3. **Outline shared stimulus library** including null stimuli.
4. **Plan synthetic dry-run dataset** structure.
5. **Decide persistence model** for ongoing Grok work (existing Sentinel Partner bot vs. dedicated QualiaLens bot).
6. **Begin outreach** to relevant researchers once the protocol draft is more concrete.

## Open Questions

- Preferred first implementation target: web app, mobile, or protocol + analysis tooling only?
- Exact fields and validation rules for `substrate_metadata`.
- Privacy and consent model for human data.
- Specific experts or communities to contact first.

## Handoff Notes

Any agent or collaborator picking this up should:

1. Read the latest `STATUS.md`.
2. Check recent commits.
3. Update this file when claiming work or finishing a session.

---

*Update this file at the end of every meaningful session.*
