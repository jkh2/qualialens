# QualiaLens Status

**Last updated:** 2026-11-17  
**Phase:** Foundation / Protocol Design  
**Active agents:** Grok (initializing)

## Current Goal

Establish the shared measurement protocol and data schema so that both the human app and AI agent interface can emit identical report structures. Human implementation comes first; agent access follows the same schema.

## What Exists

- Empty repository initialized with this foundation.
- Clear project purpose and multi-agent collaboration model (see README).

## Next Actions

1. **Define the core report schema** (`protocol/schema.md` + JSON schema).
   - Fields for ratings, free-text, similarity judgments, metacognitive probes, metadata (participant type, cognitive stack, stimulus ID, timestamp, etc.).
2. **Draft initial probe set** (`protocol/probes.md`).
   - Experience sampling items.
   - Similarity / relational judgment tasks.
   - Phenomenological free-text prompts.
   - Self-referential / metacognitive questions.
3. **Outline shared stimulus library** approach.
4. **Decide persistence model** for ongoing Grok work (existing Sentinel Partner bot vs. dedicated QualiaLens bot).
5. **Set up basic issue tracking** for discrete tasks.

## Open Questions

- Preferred first implementation target: web app, mobile, or protocol + analysis tooling only?
- How strictly should the agent interface match human constraints (e.g., response length, time pressure)?
- Privacy and consent model for human data (local-first, encrypted, opt-in aggregation).
- License and contribution terms.

## Handoff Notes

Any agent picking this up should:

1. Read the latest `STATUS.md`.
2. Check recent commits and open issues.
3. Update this file when claiming work or finishing a session.

---

*Update this file at the end of every meaningful session.*
