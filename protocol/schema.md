# QualiaLens Report Schema (Draft)

This is the shared structure that both human and agent reports must conform to.

> **Normative version:** [`schema.json`](schema.json) (JSON Schema draft 2020-12, protocol v0.1.0) is now the source of truth; this page is an informal overview. Worked examples live in [`examples/`](examples/) (with deliberately invalid records under `examples/invalid/`), and `python protocol/validate.py` checks them (`pip install jsonschema rfc3339-validator`).
>
> Changes relative to the sketch below, made while formalizing:
> - `participant_id` moved out of human `substrate_metadata` into a shared optional top-level `identity` object (`participant_id`, `session_id`, `session_index`, `linking_scope`, `continuity_basis`) so longitudinal linking works identically for humans and agents.
> - New required `condition` object (`self_referential | matched_control | null_baseline | catch | standard`, plus `matched_pair_id`).
> - `latency_ms` is accompanied by a required `latency_measure` (what interval it is) and optional `latency_detail`.
> - Agent `model` → `model_id` + required `provider`; sampling params grouped under `sampling`; `memory_mode` adds `session_context`; tools under `tool_use`.
> - Triadic responses carry `format` (`most_similar_pair | odd_one_out | anchor`) and `items` (displayed position → item id).
> - Fixed rating scales: valence −5..+5; arousal/intensity/clarity/self_presence 0..10; confidences 0..1.

## Core Principles

- Same schema for humans and agents.
- `substrate_metadata` cleanly separates subject type and environment.
- Support for triadic judgments, ratings, free text, and latency.
- PII (if any) lives outside the main report objects.

## High-Level Structure

```json
{
  "report_id": "uuid",
  "protocol_version": "0.1.0",
  "timestamp": "ISO-8601",
  "stimulus_id": "string",
  "probe_type": "triadic | free_text | rating | metacognitive | esm",
  "substrate_metadata": { ... },
  "response": { ... },
  "latency_ms": number,
  "notes": "optional"
}
```

## substrate_metadata

### For AI agents
```json
{
  "type": "agent",
  "model": "string",
  "model_version": "string",
  "temperature": number,
  "system_prompt_hash": "string",
  "tools_active": ["string"],
  "memory_mode": "stateless | memory_enabled",
  "agent_scaffold": "string"
}
```

### For humans
```json
{
  "type": "human",
  "participant_id": "opaque-id",
  "session_context": {
    "time_of_day": "string",
    "device_type": "string"
  }
}
```

PII mapping (participant_id → real identity) is stored separately and is not part of the analysis objects.

## response (examples)

### Triadic
```json
{
  "choice": "AB" | "AC" | "BC",
  "confidence": 0.0-1.0
}
```

### Free text
```json
{
  "text": "string",
  "token_count": number
}
```

### Ratings
```json
{
  "valence": number,
  "intensity": number,
  "clarity": number
}
```

## Latency

- Humans: time from stimulus presentation to response submission (ms).
- Agents: time-to-first-token and/or full generation duration (ms).

## Next Steps

- ~~Convert this into a formal JSON Schema.~~ Done: `schema.json`.
- Add GitHub Action for validation.
- Generate a small synthetic dataset of valid reports for pipeline testing.
