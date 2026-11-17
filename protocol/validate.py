#!/usr/bin/env python3
"""Validate QualiaLens report records against protocol/schema.json.

Usage:
    python protocol/validate.py                 # validate protocol/examples/ (valid + invalid)
    python protocol/validate.py FILE [FILE ...] # validate specific records (JSON object or array)

Requires: pip install jsonschema rfc3339-validator
Exit code is non-zero if any valid example fails, or any example under
examples/invalid/ unexpectedly passes.
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import best_match

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / "schema.json").read_text())
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def errors_for(path: Path):
    data = json.loads(path.read_text())
    records = data if isinstance(data, list) else [data]
    errs = []
    for i, rec in enumerate(records):
        e = best_match(VALIDATOR.iter_errors(rec))
        if e is not None:
            # descend into oneOf/anyOf context for the most specific message
            while e.context:
                e = best_match(e.context)
            loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
            errs.append(f"[{i}] {loc}: {e.message[:200]}")
    return errs


def main(argv):
    failed = False
    if argv:
        for p in map(Path, argv):
            errs = errors_for(p)
            print(f"{'FAIL' if errs else 'OK  '} {p}")
            for e in errs:
                print("     ", e)
            failed |= bool(errs)
        return 1 if failed else 0

    ex = HERE / "examples"
    for p in sorted(ex.glob("*.json")):
        errs = errors_for(p)
        print(f"{'FAIL' if errs else 'OK  '} {p.relative_to(HERE)}")
        for e in errs:
            print("     ", e)
        failed |= bool(errs)
    for p in sorted((ex / "invalid").glob("*.json")):
        errs = errors_for(p)
        status = "OK  (rejected as expected)" if errs else "FAIL (unexpectedly valid)"
        print(f"{status} {p.relative_to(HERE)}")
        if errs:
            print("     ", errs[0])
        failed |= not errs
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
