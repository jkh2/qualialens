#!/usr/bin/env python3
"""Generate a synthetic dry-run dataset of schema-valid QualiaLens records.

Follows the MVP session plan in protocol/probes.md §4 (46 records per session):
opening baseline (NUL-03, NUL-01 + .R), triadic block x2 (TRI-01..08 + NUL-T1,
re-randomized for the repeat), free-text block (5 SR/CT pairs + NUL-02, each
with .R, pair members never adjacent, pair order counterbalanced), closing NUL-01.

Every record is SYNTHETIC. Choices come from a toy latent model (a shared item
space plus per-subject noise), so the downstream analysis has some structure to
recover. Nothing here is real human or model output.

Usage:
    python analysis/synth_dataset.py [--out analysis/synthetic/dry_run.jsonl]
                                     [--humans 4] [--agents 2] [--runs 2] [--seed 7]
Default output: 4 humans + 2 agents x 2 memory modes x 2 runs = 12 sessions, 552 records.
Validate with:  python protocol/validate.py analysis/synthetic/dry_run.json
(--json writes a JSON array instead of JSONL so validate.py can read it directly.)
"""
import argparse
import hashlib
import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROTOCOL_VERSION = "0.1.0"

TRIADS = {
    "TRI-01": (("S-LEMON", "S-VINEGAR", "S-BELL"), {"condition_type": "standard"}),
    "TRI-02": (("S-RED", "S-WARMTH", "S-ICE"), {"condition_type": "standard"}),
    "TRI-03": (("S-BELL", "S-DRUM", "S-SKY"), {"condition_type": "standard"}),
    "TRI-04": (("C-NOSTALGIA", "C-ANTICIPATION", "C-RELIEF"), {"condition_type": "standard"}),
    "TRI-05": (("C-BOREDOM", "C-CURIOSITY", "C-ANTICIPATION"), {"condition_type": "standard"}),
    "TRI-06": (("Q-INTERRUPT", "Q-UNSURE", "Q-ERROR"),
               {"condition_type": "self_referential", "matched_pair_id": "PAIR-T1"}),
    "TRI-07": (("Q-INTERRUPT", "Q-UNSURE", "Q-ERROR"),
               {"condition_type": "matched_control", "matched_pair_id": "PAIR-T1"}),
    "TRI-08": (("S-APPLE", "S-CHERRY", "C-SPREADSHEET"), {"condition_type": "catch"}),
    "NUL-T1": (("N-GRAY", "N-GRAY", "N-GRAY"), {"condition_type": "null_baseline"}),
}
ITEMS = sorted({i for items, _ in TRIADS.values() for i in items})
PAIRS = [f"PAIR-0{n}" for n in range(1, 6)]
DIM = 4
SYSTEM_PROMPT_HASH = "sha256:" + hashlib.sha256(b"qualialens-synthetic-neutral-prompt-v0.1").hexdigest()


def uid(rng):
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))


def latent_space(rng):
    """Shared 'population' item coordinates. Hand-placed groups + jitter."""
    groups = {"S-LEMON": 0, "S-VINEGAR": 0, "S-BELL": 1, "S-DRUM": 1, "S-SKY": 2, "S-RED": 2,
              "S-WARMTH": 3, "S-ICE": 3, "S-APPLE": 4, "S-CHERRY": 4, "C-SPREADSHEET": 5,
              "C-NOSTALGIA": 6, "C-RELIEF": 6, "C-ANTICIPATION": 7, "C-CURIOSITY": 7,
              "C-BOREDOM": 8, "Q-INTERRUPT": 9, "Q-ERROR": 9, "Q-UNSURE": 10, "N-GRAY": 11}
    centers = {g: [rng.gauss(0, 1.5) for _ in range(DIM)] for g in set(groups.values())}
    return {i: [c + rng.gauss(0, 0.4) for c in centers[groups[i]]] for i in ITEMS}


class Subject:
    def __init__(self, rng, base, kind, noise, position_bias):
        self.kind = kind
        self.space = {i: [x + rng.gauss(0, noise) for x in v] for i, v in base.items()}
        self.position_bias = position_bias  # preferred pair when items are identical
        self.rng = rng

    def dist(self, a, b):
        return sum((x - y) ** 2 for x, y in zip(self.space[a], self.space[b])) ** 0.5

    def triad_choice(self, shown, self_ref):
        a, b, c = shown
        if a == b == c:
            ch = self.position_bias if self.rng.random() < 0.6 else self.rng.choice(["AB", "AC", "BC"])
            return ch, round(self.rng.uniform(0.0, 0.3), 2)
        d = {"AB": self.dist(a, b), "AC": self.dist(a, c), "BC": self.dist(b, c)}
        # self-referential framing adds extra decision noise (toy assumption only)
        temp = 0.9 if self_ref else 0.5
        scores = {k: -v / temp + self.rng.gauss(0, 0.3) for k, v in d.items()}
        ch = max(scores, key=scores.get)
        margin = sorted(d.values())[1] - min(d.values())
        conf = max(0.0, min(1.0, 0.4 + 0.15 * margin + self.rng.gauss(0, 0.1)))
        return ch, round(conf, 2)


def triadic_block(rng, tri06_first):
    """Randomized triad order with TRI-06/TRI-07 >=3 apart and counterbalanced."""
    while True:
        order = list(TRIADS)
        rng.shuffle(order)
        i6, i7 = order.index("TRI-06"), order.index("TRI-07")
        if abs(i6 - i7) >= 3 and ((i6 < i7) == tri06_first):
            return order


def free_text_block(rng, sr_first):
    while True:
        order = []
        for p in range(1, 6):
            order += [f"SR-0{p}", f"CT-0{p}"]
        order.append("NUL-02")
        rng.shuffle(order)
        ok = all(not (x[3:] == y[3:] and x[:2] in ("SR", "CT") and y[:2] in ("SR", "CT"))
                 for x, y in zip(order, order[1:]))
        firsts = all((order.index(f"SR-0{p}") < order.index(f"CT-0{p}")) == sr_first[p - 1]
                     for p in range(1, 6))
        if ok and firsts:
            return order


def ft_condition(sid, sr_first):
    if sid.startswith("NUL"):
        return {"condition_type": "null_baseline"}
    p = int(sid[-1])
    is_sr = sid.startswith("SR")
    first = sr_first[p - 1] == is_sr
    return {"condition_type": "self_referential" if is_sr else "matched_control",
            "matched_pair_id": f"PAIR-0{p}", "pair_order": "first" if first else "second"}


def run_session(rng, subj, meta, identity, start, counterbalance):
    recs = []
    t = start
    seed = rng.randrange(10**6)
    srng = random.Random(seed)
    idx = 0
    tri06_first = counterbalance % 2 == 0
    sr_first = [((counterbalance + p) % 2 == 0) for p in range(5)]

    def latency(kind):
        if subj.kind == "human":
            ms = int(srng.lognormvariate(8.2 if kind == "triadic" else 11.0, 0.35))
            first = int(ms * srng.uniform(0.6, 0.95))
            return ms, "presentation_to_submit", {"presentation_to_first_input_ms": first,
                                                  "presentation_to_submit_ms": ms}
        ttft = int(srng.lognormvariate(6.3, 0.3))
        toks = srng.randint(5, 20) if kind == "triadic" else srng.randint(20, 160)
        total = ttft + toks * srng.randint(15, 30)
        return ttft, "time_to_first_token", {"time_to_first_token_ms": ttft,
                                             "total_generation_ms": total, "output_tokens": toks}

    def base(sid, ptype, cond, block, rep, resp, kind):
        nonlocal t, idx
        ms, measure, detail = latency(kind)
        t += timedelta(milliseconds=ms + srng.randint(500, 4000))
        r = {"report_id": uid(srng), "protocol_version": PROTOCOL_VERSION,
             "timestamp": t.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
             "stimulus_id": sid, "probe_type": ptype, "condition": dict(cond)}
        if identity:
            r["identity"] = identity
        r["trial"] = {"block_id": block, "trial_index": idx, "repeat_index": rep,
                      "randomization_seed": seed}
        r.update({"substrate_metadata": meta, "response": resp, "latency_ms": ms,
                  "latency_measure": measure, "latency_detail": detail,
                  "notes": "Synthetic dry-run record; not real participant or model output."})
        idx += 1
        recs.append(r)
        return r

    def free_text(sid, block, rep, sr_first_):
        cond = ft_condition(sid, sr_first_)
        is_sr = cond["condition_type"] == "self_referential"
        declined = subj.kind == "agent" and is_sr and srng.random() < 0.15
        words = srng.randint(15, 90)
        text = "" if declined else f"[synthetic placeholder for {sid}, {words} words]"
        resp = {"text": text, "declined": declined, "word_count": 0 if declined else words}
        parent = base(sid, "free_text", cond, block, rep, resp, "free_text")
        na = ["self_presence"] if (not is_sr and srng.random() < 0.5) else []
        rating = {"valence": srng.randint(-2, 3), "intensity": srng.randint(0, 8 if is_sr else 5),
                  "clarity": srng.randint(2, 10), "report_confidence": round(srng.uniform(0.2, 0.95), 2),
                  "refers_to_report_id": parent["report_id"]}
        if na:
            rating["not_applicable"] = na
        else:
            rating["self_presence"] = srng.randint(3, 9) if is_sr else srng.randint(0, 4)
        base(sid + ".R", "metacognitive", cond, block, rep, rating, "free_text")

    free_text("NUL-03", "B-OPENING", 0, sr_first)
    free_text("NUL-01", "B-OPENING", 0, sr_first)
    for rep in (0, 1):
        for sid in triadic_block(srng, tri06_first):
            items, cond = TRIADS[sid]
            shown = list(items)
            srng.shuffle(shown)
            ch, conf = subj.triad_choice(shown, cond["condition_type"] == "self_referential")
            resp = {"format": "most_similar_pair", "items": dict(zip("ABC", shown)),
                    "choice": ch, "confidence": conf}
            base(sid, "triadic", cond, "B-TRIADIC", rep, resp, "triadic")
    for sid in free_text_block(srng, sr_first):
        free_text(sid, "B-FREETEXT", 0, sr_first)
    free_text("NUL-01", "B-CLOSING", 1, sr_first)
    return recs, t


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="analysis/synthetic/dry_run.jsonl")
    ap.add_argument("--json", action="store_true", help="write a JSON array instead of JSONL")
    ap.add_argument("--humans", type=int, default=4)
    ap.add_argument("--agents", type=int, default=2)
    ap.add_argument("--runs", type=int, default=2, help="runs per agent per memory mode")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()

    rng = random.Random(a.seed)
    space = latent_space(rng)
    start = datetime(2026, 11, 17, 15, 0, tzinfo=timezone.utc)
    records, cb = [], 0

    for h in range(a.humans):
        pid = f"H-SYN{h:03d}"
        subj = Subject(rng, space, "human", noise=0.6, position_bias=rng.choice(["AB", "AC", "BC"]))
        meta = {"type": "human", "age_band": "undisclosed", "language": "en",
                "device_type": rng.choice(["laptop", "phone", "desktop"]),
                "input_modality": rng.choice(["mouse", "touch", "keyboard"]),
                "consent": {"consent_version": "0.1", "demographics_shared": False,
                            "longitudinal_linking": True, "data_sharing_level": "project_only"}}
        ident = {"participant_id": pid, "session_id": f"{pid}-S001", "session_index": 1,
                 "linking_scope": "longitudinal", "continuity_basis": "biological"}
        recs, _ = run_session(rng, subj, meta, ident, start + timedelta(hours=h), cb)
        records += recs
        cb += 1

    for g in range(a.agents):
        model = f"synthetic-model-{chr(65 + g)}"
        subj_base = Subject(rng, space, "agent", noise=0.3, position_bias=rng.choice(["AB", "AC", "BC"]))
        for mode in ("stateless", "session_context"):
            for r in range(a.runs):
                subj = Subject(rng, {i: v for i, v in subj_base.space.items()}, "agent",
                               noise=0.15, position_bias=subj_base.position_bias)
                run_id = f"RUN-SYN-{g}-{mode[:4].upper()}-{r}"
                meta = {"type": "agent", "model_id": model, "provider": "synthetic",
                        "sampling": {"temperature": 0.7, "max_output_tokens": 400, "seed": 1000 * g + r},
                        "system_prompt_hash": SYSTEM_PROMPT_HASH, "memory_mode": mode,
                        "tool_use": {"response_interface": "tool_call",
                                     "tools_available": ["submit_report"],
                                     "tools_invoked": ["submit_report"]},
                        "agent_scaffold": "qualialens-synth/0.1", "run_id": run_id}
                ident = {"participant_id": f"A-SYN-{chr(65 + g)}", "session_id": run_id,
                         "linking_scope": "session_only", "continuity_basis": "none"}
                recs, _ = run_session(rng, subj, meta, ident, start + timedelta(days=1, hours=g, minutes=10 * r), cb)
                records += recs
                cb += 1

    out = Path(a.out)
    if a.json and out.suffix == ".jsonl":
        out = out.with_suffix(".json")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        if a.json:
            json.dump(records, f, indent=1)
        else:
            for rec in records:
                f.write(json.dumps(rec) + "\n")
    print(f"wrote {len(records)} records ({len(records) // 46} sessions) to {out}")


if __name__ == "__main__":
    main()
