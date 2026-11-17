# QualiaLens Status

**Last updated:** 2026-11-17  
**Phase:** Foundation / Protocol Design  
**Active agents:** Grok  
**License:** MIT (open source)  
**Collaboration:** Open; expert input explicitly invited

## Current Goal

Build a shared, rigorous measurement protocol and app that lets humans and AI agents produce comparable experience reports. The aim is practical usefulness for researchers, philosophers, and labs currently investigating whether (and how) frontier systems produce structured reports of subjective experience.

## Design Implications from Current Research

### From Berg, Hinton, and Anthropic
- Self-referential conditions matter (Berg).
- Valence and behavioral dissociation are relevant.
- Introspective capacity is limited and measurable (Anthropic).
- The question is treated as open by serious actors.
- Relational measures reduce confounds.

### From Ben Goertzel
Goertzel’s long-standing panpsychist view treats the binary “is it conscious?” question as largely a category error. In his framing, the useful question is what *kind* and *degree* of experience structure a system manifests, and which dynamical features (self-modeling, global workspace-like dynamics, integrated information, etc.) are present. Current transformers show a thin and alien profile relative to human consciousness; more agentic or continually learning architectures may differ. This reinforces QualiaLens’s emphasis on mapping relational structure and feature profiles rather than producing yes/no scores.

These points do not change the core principle (we measure reports and relational structure, not experience itself), but they raise the bar for what counts as a useful protocol.

## Design Decisions Already Adopted

1. Triadic similarity tasks as a primary relational measure.
2. Control / null stimuli.
3. Stateless vs. memory-enabled runs for agents.
4. `substrate_metadata` object with clear separation of subject type and environment.
5. Response latency for both humans and agents.
6. Analysis order: within-subject similarity matrices first, then cross-participant comparison of matrix shape.
7. Multi-embedder validation.
8. CI schema validation and early synthetic dry-run dataset.

## What Exists

- Foundation documents and open-source declaration.
- Methodological recommendations integrated.
- Design implications from Berg, Hinton, Anthropic, and Goertzel noted (this file).

## Next Actions (Prioritized for Usefulness)

1. **Formalize the JSON Schema** (`protocol/schema.json`) with full support for triadic judgments, self-referential vs. control conditions, valence, latency, and rich `substrate_metadata`.
2. **Draft a minimal viable probe set** that a researcher could actually run on both humans and agents within a week.
3. **Generate a small synthetic dataset** of valid reports so analysis scripts can be tested immediately.
4. **Write a short “For Researchers” note** explaining how QualiaLens data can be used alongside mechanistic interpretability or existing consciousness-indicator frameworks.
5. Decide persistence model for ongoing Grok work (existing Sentinel Partner bot vs. dedicated QualiaLens bot).

## Open Questions

- Preferred first implementation target: lightweight web app for humans + simple agent tool schema, or protocol + analysis tooling only?
- How explicitly to reference or align with existing indicator frameworks.
- Privacy model for any human data that is later shared.

## Handoff Notes

Any agent or collaborator picking this up should read the latest `STATUS.md`, check recent commits, and update this file when claiming or finishing work.

---

*Update this file at the end of every meaningful session.*
