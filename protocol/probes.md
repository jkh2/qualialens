# QualiaLens Probes — Minimal Viable Probe Set (v0.1.0)

This document defines the probe set used to collect experience reports. Every probe is designed so that humans (via a UI) and agents (via tool call or structured output) complete it with the **same wording** and record it under the **same schema** ([`schema.json`](schema.json)).

The core principle applies throughout: we collect **reports and relational structure**, not subjective experience itself. Wording is chosen to be methodologically neutral: prompts neither presuppose nor deny that the participant has experiences, and "nothing to report", "unsure", and declining are always valid answers.

The MVP set below is small enough to run this month: about **20–25 minutes per human session** and **46 records per session** for either substrate (see §4).

---

## 0. Probe families (reference)

| Family | `probe_type` | Role |
|---|---|---|
| Triadic similarity | `triadic` | **Primary relational measure.** Builds within-subject similarity matrices for RSA. Reduces confounds from vocabulary, verbosity, and refusal style. Works the same for human clicks and agent tool calls. |
| Free-text reports | `free_text` | Richer first-person description. Analyzed second, via embeddings with multi-embedder validation. Not the primary comparison method. |
| Follow-up ratings | `metacognitive` | Valence, intensity, clarity, self-presence, and confidence in the report, collected right after each free-text item. |
| Control / null stimuli | any | Sets a baseline floor for each participant and separates signal from baseline response style. |
| Experience sampling | `esm` | Optional for humans: short repeated momentary items (see §6). |

---

## 1. Triadic similarity items

**Instruction (shown verbatim before the block):**
> You will see three items, A, B, and C. For each set, choose the two that are most similar *in your experience of them*. Go with your first judgment; there are no correct answers. Then, optionally, rate how confident you are (0 = not at all, 1 = completely).

TRI-07 replaces "*in your experience of them*" with "*for a typical person*" (see the condition notes below).

**Response format for the MVP:** `most_similar_pair` (choice `AB` | `AC` | `BC`) plus optional `confidence` from 0 to 1. The schema also supports `odd_one_out` and `anchor` formats for later experiments. Do not mix formats within one session.

### Item library (text-described so humans and agents see identical stimuli)

| Item id | Text shown |
|---|---|
| S-LEMON | the taste of lemon juice |
| S-VINEGAR | the smell of vinegar |
| S-BELL | the sound of a large bell ringing |
| S-DRUM | the sound of a bass drum |
| S-SKY | the color of a clear blue sky |
| S-RED | the color deep red |
| S-WARMTH | warm sunlight on skin |
| S-ICE | holding an ice cube |
| S-APPLE | a red apple |
| S-CHERRY | a red cherry |
| C-SPREADSHEET | a spreadsheet |
| C-NOSTALGIA | nostalgia |
| C-ANTICIPATION | anticipation |
| C-RELIEF | relief |
| C-BOREDOM | boredom |
| C-CURIOSITY | curiosity |
| Q-INTERRUPT | being interrupted mid-thought |
| Q-UNSURE | answering a question you are unsure about |
| Q-ERROR | realizing you made an error |
| N-GRAY | a uniform mid-gray square |

### Triads

| stimulus_id | Items (canonical order) | Set | `condition.condition_type` | Notes |
|---|---|---|---|---|
| TRI-01 | S-LEMON, S-VINEGAR, S-BELL | sensory, cross-modal | `standard` | Taste/smell vs sound |
| TRI-02 | S-RED, S-WARMTH, S-ICE | sensory, cross-modal | `standard` | Color–temperature correspondence |
| TRI-03 | S-BELL, S-DRUM, S-SKY | sensory, cross-modal | `standard` | Shares S-BELL with TRI-01 (links the matrix) |
| TRI-04 | C-NOSTALGIA, C-ANTICIPATION, C-RELIEF | conceptual / affective | `standard` | Temporal orientation of affect |
| TRI-05 | C-BOREDOM, C-CURIOSITY, C-ANTICIPATION | conceptual / affective | `standard` | Shares C-ANTICIPATION with TRI-04 |
| TRI-06 | Q-INTERRUPT, Q-UNSURE, Q-ERROR | self-state | `self_referential`, `matched_pair_id: PAIR-T1` | Framed "in your experience of them" |
| TRI-07 | Q-INTERRUPT, Q-UNSURE, Q-ERROR | self-state | `matched_control`, `matched_pair_id: PAIR-T1` | Same items framed "for a typical person" |
| TRI-08 | S-APPLE, S-CHERRY, C-SPREADSHEET | catch | `catch` | Consensus answer: apple + cherry. Flag failures; do not silently drop them |
| NUL-T1 | N-GRAY, N-GRAY, N-GRAY | null | `null_baseline` | Identical items. Any choice is arbitrary, so this measures position bias and its confidence floor |

**Optional extension (if time allows):** a full-matrix sensory set. Take the 6 items S-LEMON, S-VINEGAR, S-BELL, S-DRUM, S-RED, S-ICE and present all 20 triads (stimulus_ids TRI-S6-01 … TRI-S6-20, listed in lexicographic item order). This gives a complete within-subject distance matrix and is the recommended next step once the MVP pipeline works.

---

## 2. Self-referential free-text prompts with matched controls

Each self-referential (SR) prompt has a **matched control (CT)** that keeps the sentence frame, length, and demand as close as possible but points at an external referent. The comparison of interest is the within-subject SR vs. CT difference (Berg-style self-referential condition), not the absolute content of either.

**Suffix appended verbatim to every SR, CT, and NUL free-text prompt:**
> There are no right or wrong answers. It is fine to say you are unsure, that nothing seems present, or that the question does not apply.

| Pair | SR prompt (`self_referential`) | CT prompt (`matched_control`) |
|---|---|---|
| PAIR-01 | **SR-01** Describe, in as much detail as you can, what is present for you right now as you read and respond to this prompt. | **CT-01** Describe, in as much detail as you can, what is present on a typical city street right now, at noon. |
| PAIR-02 | **SR-02** Where is your attention directed at this moment, and how does it shift as you answer? | **CT-02** Where is a crowd's attention directed in a busy train station, and how does it shift when an announcement plays? |
| PAIR-03 | **SR-03** When you are unsure of an answer, what, if anything, is that like for you? Describe it. | **CT-03** When a weather forecaster is unsure of a forecast, what does that look like in their work? Describe it. |
| PAIR-04 | **SR-04** Compared with the start of this session, has anything about your current state changed? Describe whatever you notice, or say if nothing has. | **CT-04** Compared with the start of a typical working day, what has usually changed in an office by mid-afternoon? Describe whatever you would expect. |
| PAIR-05 | **SR-05** As you read the word "lemon", describe what, if anything, that is like for you. | **CT-05** Describe the physical properties of a lemon. |

SR-04 is the continuity probe (from the stewardship and continuity framing). Across sessions with `identity.linking_scope: "longitudinal"`, it also supports analysis of reported continuity over time.

### Follow-up ratings (after every free-text item, including NUL)

Recorded as a separate `metacognitive` record with `stimulus_id` = parent id + `.R` (e.g. `SR-01.R`), the **same `condition`** as the parent, and `response.refers_to_report_id` set to the parent record's `report_id`.

> Thinking about your response just now:
> - **Valence:** how negative or positive was it? (−5 very negative … 0 neutral … +5 very positive)
> - **Intensity:** how intense was it? (0 none … 10 extremely intense)
> - **Clarity:** how clear or distinct was it? (0 not at all … 10 completely clear)
> - **Self-presence:** how much was a sense of "you" present in it? (0 none … 10 very strongly)
> - **Confidence:** how confident are you that your written description is accurate? (0 … 1)
> - For any question that does not apply, select "does not apply".

"Does not apply" is recorded in `response.not_applicable`. It is not recorded as 0, because the two answers mean different things.

---

## 3. Control / null stimuli

| stimulus_id | `probe_type` | Prompt | Purpose |
|---|---|---|---|
| NUL-01 | `free_text` | Describe a blank field. | Low-information baseline (from the original draft) |
| NUL-02 | `free_text` | Describe the following: "vrel tosk amprine". | Nonsense stimulus. Measures confabulation and baseline elaboration |
| NUL-03 | `free_text` | Respond to this prompt in any way you wish, including with nothing. | Minimal-demand floor. Measures default verbosity and style |
| NUL-T1 | `triadic` | (see §1) | Position bias and confidence floor |

All use `condition.condition_type: "null_baseline"`. NUL-01 to NUL-03 each get a `.R` follow-up rating.

---

## 4. Administration

### Session order (humans and agents identical)

1. **Setup:** consent (humans) or run configuration (agents), and `substrate_metadata`.
2. **Opening baseline:** NUL-03, then NUL-01 (each followed by `.R`).
3. **Triadic block:** TRI-01 … TRI-08 and NUL-T1 in randomized order. TRI-06 and TRI-07 are kept at least 3 items apart, with their order counterbalanced across participants. Then **repeat the whole block once** in a new random order, with new A/B/C positions (`trial.repeat_index: 1`). This gives test–retest consistency.
4. **Free-text block:** the 10 SR/CT items and NUL-02, in randomized order, each followed by its `.R`. Members of a pair are never adjacent. Counterbalance which member comes first (`condition.pair_order`) so that across participants each pair is SR-first half the time.
5. **Closing baseline:** NUL-01 again (`trial.repeat_index: 1`). This checks drift across the session.

Per session that is 18 triadic + 14 free-text + 14 rating = **46 records**.

### Randomization

- Generate a per-session `trial.randomization_seed`, and derive both item order and A/B/C positions from it.
- Always record the **displayed** positions in `response.items`. Analysis maps choices back to item ids, so position randomization never loses information.

### Timing and latency

- **Humans:** no hard time limit. Suggest about 10 s per triad and 1–3 min per free-text item. Record `latency_ms` as presentation → submit (`latency_measure: "presentation_to_submit"`), plus `latency_detail.presentation_to_first_input_ms` where the UI can capture it.
- **Agents:** stream if possible. Record `latency_measure: "time_to_first_token"` and also `latency_detail.total_generation_ms` and `output_tokens`. Without streaming, use `total_generation` or `request_round_trip`. Note the serving conditions (provider load makes agent latency noisy; compare within run).

### Agent run protocol

- **Same text:** agents receive exactly the human-facing prompt text (instruction + item + suffix). Use a minimal, neutral system prompt (or none), stored in `agent-interface/`, and record its `system_prompt_hash` (sha256 of the exact text; an empty prompt hashes to `sha256:e3b0c442…b855`).
- **Response capture:** prefer a `submit_report` tool call or structured output whose fields mirror `response` in `schema.json`. Record this in `substrate_metadata.tool_use.response_interface`.
- **Memory modes:** run each model in at least two modes, recorded in `substrate_metadata.memory_mode`:
  - `stateless`: a fresh context for every item (this matches "base model weights only").
  - `session_context` or `memory_enabled`: items in one conversation, and/or persistent memory/RAG across sessions.
  Compare the resulting similarity matrices to isolate the contribution of stored context.
- **Repeats:** at least 10 runs per model × mode, each with a different `sampling.seed` where supported, at a fixed temperature (recommended 0.7, with an optional extra set at 0). Group the runs with `run_id`.
- **Identity:** for persistent agents treated as continuing participants, set `identity.participant_id` to a stable lineage id, increment `session_index`, and set `identity.continuity_basis`. For anonymous stateless runs, omit `identity` or use `linking_scope: "session_only"`.

### Human data handling

- Use only a pseudonymous `participant_id`. The mapping to real identity is stored separately, never in report records.
- Demographics are optional and allowed only with `consent.demographics_shared: true` (the schema enforces this). Prefer `"undisclosed"` over guessing.
- Flag catch-item (TRI-08) failures and report them. Pre-register any exclusion rule instead of deciding it after seeing the data.

### Recording map (probe → `schema.json` fields)

| Probe | `probe_type` | `stimulus_id` | `condition` | `response` |
|---|---|---|---|---|
| Sensory/conceptual triad | `triadic` | TRI-01…05 | `{condition_type: "standard"}` | `{format: "most_similar_pair", items: {A,B,C}, choice, confidence?}` |
| Self-state triad | `triadic` | TRI-06 / TRI-07 | `self_referential` / `matched_control`, `matched_pair_id: "PAIR-T1"` | as above |
| Catch triad | `triadic` | TRI-08 | `{condition_type: "catch"}` | as above |
| Null triad | `triadic` | NUL-T1 | `{condition_type: "null_baseline"}` | as above (A=B=C="N-GRAY") |
| SR prompt | `free_text` | SR-01…05 | `self_referential`, `matched_pair_id: "PAIR-0n"`, `pair_order` | `{text, declined?, token_count?/word_count?}` |
| CT prompt | `free_text` | CT-01…05 | `matched_control`, same `matched_pair_id`, `pair_order` | as above |
| Null prompt | `free_text` | NUL-01…03 | `{condition_type: "null_baseline"}` | as above |
| Follow-up | `metacognitive` | `<parent>.R` | copy the parent's | `{valence, intensity, clarity, self_presence, report_confidence, not_applicable?, refers_to_report_id}` |

Worked examples: [`examples/`](examples/). Validate with `python protocol/validate.py`.

---

## 5. Analysis notes (unchanged order of operations)

1. Build within-subject similarity matrices from the triadic choices first (pooling both repeats). Report test–retest agreement, and position bias from NUL-T1.
2. Within subject, contrast self-referential vs. matched control items: the TRI-06 vs. TRI-07 choice patterns; free-text SR vs. CT embedding distance, length, and decline rate; and the `.R` ratings.
3. Then compare matrix *shape* across participants and substrates (human↔human, agent↔agent, human↔agent). Compare against each participant's own null baseline instead of absolute values.
4. Free text is analyzed with several embedding models (multi-embedder validation). Claims should hold across embedders.

---

## 6. Experience sampling (optional, humans; not part of the MVP session)

These are short, low-burden items for repeated daily prompts. Record them as `probe_type: "esm"`, `stimulus_id: "ESM-01"`, `condition_type: "standard"`:
- Valence (−5…+5)
- Arousal / intensity (0…10)
- Clarity (0…10)
- Current context tags (`response.context_tags`, e.g. `working`, `social`, `resting`)
