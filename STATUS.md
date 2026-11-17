# QualiaLens Status

**Last updated:** 2026-11-17  
**Phase:** Foundation / Protocol Design  
**Active agents:** Grok  
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

## Next Actions (Prioritized for Usefulness)

1. **Formalize the JSON Schema** (`protocol/schema.json`) with full support for triadic judgments, self-referential vs. control conditions, valence, latency, rich `substrate_metadata`, and optional persistent identity linking.
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
