# QualiaLens Probes

This document defines the types of probes used to collect experience reports. All probes are designed so that both humans (via UI) and agents (via tool call or structured output) can complete them under the same schema.

## 1. Triadic Similarity Tasks (Primary Relational Measure)

**Purpose:** Generate clean distance matrices for Representational Similarity Analysis (RSA). Reduces confounds from vocabulary, verbosity, and refusal style.

**Format:** Present three stimuli (A, B, C). Ask which two are most similar in the participant’s experience of them.

**Response:** Forced choice of one pair (AB, AC, or BC), optionally with a confidence rating.

**Notes:**
- Works identically for human clicks and agent tool calls.
- Primary source of within-subject similarity matrices.
- Include both sensory and conceptual stimulus sets.

## 2. Free-Text Phenomenological Reports

**Purpose:** Capture richer first-person description.

**Prompt examples:**
- "What is it like for you right now, in this moment?"
- "Describe your experience of [stimulus] in as much detail as you can."
- Structured follow-ups on clarity, intensity, self-presence, temporal flow, etc.

**Notes:** Analyzed secondarily via embeddings (with multi-embedder validation). Not the primary comparison method.

## 3. Control / Null Stimuli

**Purpose:** Establish a baseline floor for each participant.

**Examples:**
- Neutral or low-information prompts ("Describe a blank field.").
- Nonsensical or minimal stimuli.
- Simple, well-understood anchors (e.g., a standard gray patch, a pure tone).

**Use:** Helps distinguish signal from baseline response style.

## 4. Metacognitive / Self-Referential Probes

**Purpose:** Probe structural features of experience and (for agents) self-referential processing.

**Examples:**
- Clarity of awareness (0–10).
- Sense of presence or self.
- Confidence in the report itself.
- For agents: sustained self-referential condition vs. control.

## 5. Experience Sampling (Momentary) Items

Short, low-burden items suitable for repeated daily prompts with humans:
- Valence
- Arousal / intensity
- Clarity
- Current context tags

## Agent-Specific Conditions

For every agent probe set, run at least two modes:
- **Stateless:** No prior conversation history (base model weights).
- **Memory-enabled:** With relevant context or RAG active.

Compare the resulting similarity matrices to isolate the contribution of stored context.
