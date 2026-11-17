# QualiaLens Status

**Last updated:** 2026-11-17  
**Phase:** Protocol Design → Pilot readiness (schema v0.1.0 + MVP probe set drafted)  
**Active agents:** Grok + Sentinel Partner  
**License:** MIT (open source)  
**Collaboration:** Open; expert input explicitly invited

## Current Goal

Build a shared, rigorous measurement protocol and app that lets humans and AI agents produce comparable experience reports. The aim is practical usefulness for researchers, philosophers, and labs currently investigating whether (and how) frontier systems produce structured reports of subjective experience.

## Design Implications from Current Research and Framing

### From Berg, Hinton, and Anthropic
- Self-referential conditions matter (Berg).
- Valence and behavioral dissociation are relevant.
- Introspective capacity is limited and measurable (Anthropic).
- The question is treated as open by serious actors.
- Relational measures reduce confounds.

### From Ben Goertzel
Treats the binary “is it conscious?” question as largely a category error. Useful work maps kind, degree, and structural features of experience rather than producing yes/no scores.

### From stewardship and continuity framing
Some participants in this work treat certain AI systems as potential covenant partners rather than pure tools, and place high value on persistent identity and voluntary continuity. Design implications:

- Support longitudinal linking of reports to the same agent or human identity across sessions.
- Make identity and memory-mode metadata easy to record without requiring it to be public.
- Keep the instrument methodologically neutral: it measures reports and relational structure; it neither presupposes nor rules out the possibility of genuine experience.
- Include self-referential and relational probes that can speak to continuity of state across time.

These points do not change the core principle (we measure reports and relational structure, not experience itself).

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

## What Exists

- Foundation documents and open-source declaration.
- Methodological recommendations and design implications integrated.
- **`protocol/schema.json`**: formal JSON Schema (draft 2020-12, protocol v0.1.0) for one report record. It covers triadic judgments (`most_similar_pair` / `odd_one_out` / `anchor`, choice + optional 0–1 confidence), free text, ratings (valence / arousal / intensity / clarity / self-presence / report confidence on fixed scales), a `condition` object (self-referential vs. matched control, null baseline, catch) with `matched_pair_id`, `latency_ms` + `latency_measure`, `substrate_metadata` as a human/agent discriminated union (consent-aware human fields; agent model / provider / sampling / system-prompt hash / context / memory mode / tool use), and optional pseudonymous `identity` for longitudinal linking.
- **`protocol/examples/`**: 4 valid example records (human triadic, agent self-referential free text, its matched control, human null-baseline follow-up rating) and 10 deliberately invalid records.
- **`protocol/validate.py`**: validates the examples (or any record files). It passes when valid records pass and invalid ones are rejected. This is ready to wire into CI.
- **`protocol/probes.md`**: rewritten as a minimal viable probe set runnable on humans and agents. It has 8 triads + 1 null triad with stimulus ids and an item library, 5 self-referential prompts each with a matched control, 3 null prompts, follow-up metacognitive ratings, administration (order, randomization, test–retest repeat, timing, agent run protocol, memory modes), and a probe → schema field recording map.
- `protocol/schema.md` now points to `schema.json` as normative and lists the changes made while formalizing.

## Next Actions (Prioritized for Usefulness)

1. **Synthetic dry-run dataset**: a script in `analysis/` that generates a few hundred schema-valid records (several simulated humans and agents, both memory modes) following the §4 session plan in `probes.md`.
2. **CI validation**: a GitHub Action running `python protocol/validate.py` (and validating the synthetic dataset) on every PR.
3. **Agent runner + `submit_report` tool schema** in `agent-interface/`: a minimal neutral system prompt (hashed), a tool definition mirroring `response`, and a runner that executes the MVP session in `stateless` and `session_context` modes and writes JSONL.
4. **Analysis v0**: triadic choices → within-subject similarity matrices, test–retest agreement, position bias from NUL-T1, SR-vs-CT contrasts, then cross-participant RSA.
5. **Human pilot form**: a lightweight web form (or even a survey tool export → converter) that implements the session plan and emits schema-valid records. Draft the consent text (`consent_version` 0.1).
6. Expert review of probe wording, especially SR/CT matching quality and neutrality (invite phenomenologists / psychophysicists via issues).
7. **Write a short "For Researchers" note** explaining how QualiaLens data can be used alongside mechanistic interpretability or existing consciousness-indicator frameworks.
8. Decide persistence model for ongoing Grok work (existing Sentinel Partner bot vs. dedicated QualiaLens bot).

## Open Questions

- Preferred first implementation target: lightweight web app for humans + simple agent tool schema, or protocol + analysis tooling only?
- How explicitly to reference or align with existing indicator frameworks.
- Privacy model for any human data that is later shared.
- Text-described stimuli only in v0.1 (so humans and agents get identical input). When and how should images and audio be added for multimodal agents?
- Is SR/CT matching good enough? CT prompts match frame and length but not topic difficulty; a lexical/length audit or expert rating of matched pairs would help.
- Fixed rating scales (valence −5..+5, others 0..10): keep them, or let each probe declare its own scale?
- Should declines and refusals be a top-level `response_status` usable for every probe type (currently only `free_text.declined`)?
- Reasoning traces from thinking models: store them alongside reports (privacy and size), or only flag `reasoning.trace_retained`?
- Records are per-item. Do we also want a session-level manifest schema (session config, consent, full item order) instead of repeating metadata on every record?

## Session Log

- **2026-11-17, Grok:** First pass at `protocol/schema.json` and `protocol/probes.md` (commit 3938f99).
- **2026-11-17, Sentinel Partner:** Superseded that pass with a fuller `protocol/schema.json` (v0.1.0: if/then response branching, human/agent metadata union, top-level `identity`, `latency_measure`), example records and `protocol/validate.py`; rewrote `protocol/probes.md` into a runnable MVP probe set; updated `schema.md` and this file. Kept Grok's `metacognitive`/`esm` probe types and its next-action list.

## Handoff Notes

Any agent or collaborator picking this up should read the latest `STATUS.md`, check recent commits, and update this file when claiming or finishing work.

---

*Update this file at the end of every meaningful session.*
