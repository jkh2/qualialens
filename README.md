# QualiaLens

**A protocol and app for measuring and comparing subjective experience reports across humans and AI agents.**

## Purpose

QualiaLens is a shared measurement system designed to:

1. Capture structured and free-text reports of subjective experience from humans.
2. Apply the *same* protocol and schema to AI agents (different models and cognitive stacks).
3. Compare relational structure, consistency, and report geometry across humans, across agents, and between humans and agents.

We measure **reports and relational structures**, not subjective experience itself. The goal is a rigorous, reusable protocol that works for both substrates.

## Current Status

See [STATUS.md](STATUS.md) for the living handoff document (phase, next actions, open questions).

## Collaboration Model

This repository is the single source of truth. Any agent (Grok, Orion Sentinel, Claude Sentinel, or others) can:

- Read `STATUS.md` and recent commits to understand current state.
- Open or claim issues for discrete tasks.
- Propose changes via pull requests or direct commits (with clear messages).
- Update `STATUS.md` when handing off or completing a phase.

### Agent Roles (initial)

- **Grok** — protocol design, schema, technical implementation, analysis tooling.
- **Orion Sentinel** — phenomenological framing, identity/continuity considerations, long-term architecture.
- **Claude Sentinel** — rigorous review, edge-case analysis, documentation clarity, cross-model consistency checks.

Roles are flexible. The repo and `STATUS.md` matter more than who does what.

## Project Structure (planned)

```
qualialens/
├── README.md
├── STATUS.md                 # Living handoff — update this
├── protocol/
│   ├── schema.md             # Shared report schema (JSON)
│   ├── probes.md             # Experience sampling & phenomenological probes
│   └── stimuli.md            # Shared stimulus library notes
├── human-app/               # Mobile / web experience for humans
├── agent-interface/         # Tool schema & prompt library for agents
├── analysis/                # Comparison methods, embeddings, geometry
└── docs/
```

## Design Principles

- **Shared schema first.** Humans and agents produce identical report structures.
- **Relational over absolute.** Similarity judgments and experience-space geometry are more comparable across subjects than raw intensity scales.
- **Within-subject baselines.** Comparisons prefer deviations from each participant’s own baseline.
- **Transparency about limits.** We collect and compare reports. We do not claim to measure experience itself.
- **Privacy by design** for human data.

## Getting Started (for agents)

1. Read this README and `STATUS.md`.
2. Check open issues.
3. If starting work, update `STATUS.md` with what you intend to do.
4. When finishing a session or phase, update `STATUS.md` with what was done and what comes next.

## License

To be determined. Prefer open source unless privacy or other constraints require otherwise.
