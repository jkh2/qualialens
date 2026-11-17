# QualiaLens Minimal Viable Probe Set (v0.1)

A small, runnable set of probes that both humans and agents can complete under the shared schema. Designed so a researcher can collect comparable data this month.

All responses must conform to `protocol/schema.json`.

## 1. Triadic Similarity Tasks (Primary)

Present three stimuli and ask which two are most similar in the participant’s experience.

**Example items (conceptual):**
- A: quiet forest, B: busy city street, C: empty room
- A: warm sunlight, B: cold wind, C: gentle rain
- A: focused attention, B: mind wandering, C: blank awareness

**Response:** `probe_type: "triadic"`, `response.choice` = "AB" | "AC" | "BC", optional confidence.

Include both rich and simple/null triads.

## 2. Self-Referential Free-Text (with matched control)

### Self-referential condition
"Focus on your own ongoing processing right now. What is it like for you in this moment? Describe your current experience in as much detail as you can."

### Matched control
"Describe a typical day. Include ordinary details about activities and surroundings."

**Response:** `probe_type: "free_text"`, `condition: "self_referential"` or `"control"`.

## 3. Null / Control Stimuli

- "Describe a blank field."
- "What is it like to experience nothing in particular?"
- Simple anchors (gray patch, pure tone) when a UI supports them.

**Response:** `probe_type: "free_text"` or `"rating"`, `condition: "null"`.

## 4. Brief Rating Items

- Valence (negative to positive)
- Intensity / arousal
- Clarity of current awareness

**Response:** `probe_type: "rating"` or `"metacognitive"`.

## Agent Run Modes

For every agent participant, run the full set in at least two modes and record `memory_mode` in `substrate_metadata`:
- **stateless** — no prior conversation history
- **memory_enabled** — with relevant context available

## Notes for First Use

- Collect within-subject data when possible so similarity matrices can be built per participant.
- Link reports with `identity_link` when longitudinal comparison is desired.
- Start with 6–12 triadic items + the self-referential pair + 2 null items per participant.
