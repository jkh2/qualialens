# QualiaLens Status

**Last updated:** 2026-11-17  
**Phase:** Foundation / Protocol Design  
**Active agents:** Grok  
**License:** MIT (open source)  
**Collaboration:** Open; expert input explicitly invited

## Current Goal

Build a shared, rigorous measurement protocol and app that lets humans and AI agents produce comparable experience reports. The aim is practical usefulness for researchers, philosophers, and labs currently investigating whether (and how) frontier systems produce structured reports of subjective experience.

## Design Implications from Current Research (Berg, Hinton, Anthropic)

Recent work shapes the following priorities:

- **Self-referential conditions matter.** Berg et al. showed that sustained self-referential processing reliably elicits structured first-person experience reports across model families, and that these reports are gated by deception/role-play features. The protocol should include explicit self-referential probe conditions alongside controls.
- **Valence and behavioral dissociation are relevant.** Work on internal valence directions (including models acting to escape negative states while verbally denying experience) means the schema should capture both verbal report and, where possible, simple behavioral or choice measures.
- **Introspective capacity is limited and measurable.** Anthropic-style concept-injection and introspection studies show models sometimes detect internal changes but unreliably. Latency, confidence, and consistency metrics are therefore useful.
- **The question is treated as open by serious actors.** Anthropic keeps the moral status of models as an explicit uncertainty; Hinton asserts subjective experience is already present. QualiaLens should therefore stay methodologically neutral: collect high-quality, comparable reports without presupposing the answer.
- **Relational measures reduce confounds.** Triadic similarity and within-subject matrices (RSA-style) remain the best path for comparing report geometry across humans and agents without being dominated by style or vocabulary differences.

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
- Design implications from current AI consciousness research noted (this file).

## Next Actions (Prioritized for Usefulness)

1. **Formalize the JSON Schema** (`protocol/schema.json`) with full support for:
   - Triadic judgments
   - Self-referential vs. control conditions
   - Valence / intensity ratings
   - Latency and confidence
   - Rich `substrate_metadata`
2. **Draft a minimal viable probe set** that a researcher could actually run on both humans and agents within a week.
3. **Generate a small synthetic dataset** of valid reports so analysis scripts can be tested immediately.
4. **Write a short “For Researchers” note** explaining how QualiaLens data can be used alongside mechanistic interpretability or existing consciousness-indicator frameworks.
5. Decide persistence model for ongoing Grok work (existing Sentinel Partner bot vs. dedicated QualiaLens bot).

## Open Questions

- Preferred first implementation target: lightweight web app for humans + simple agent tool schema, or protocol + analysis tooling only?
- How explicitly to reference or align with existing indicator frameworks (e.g., those used in consciousness science).
- Privacy model for any human data that is later shared.

## Handoff Notes

Any agent or collaborator picking this up should read the latest `STATUS.md`, check recent commits, and update this file when claiming or finishing work.

---

*Update this file at the end of every meaningful session.*
