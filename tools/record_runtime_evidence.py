"""Publish compact, hash-linked summaries of completed smoke runs (no world edits)."""
import argparse
import hashlib
import json
from pathlib import Path


def summarize(path):
    raw = path.read_bytes()
    report = json.loads(raw)
    if "exit_code" not in report:
        raise ValueError(f"Not a completed runtime report: {path}")
    block_report = report.get("showcase_blocks" if report.get("showcase") else "world_blocks", {})
    instances = []
    keys = ("structure", "template", "origin", "rotation", "bounding_box", "bounding_box_matches",
            "checked_blocks", "matched_blocks", "nature_cells_skipped", "normalized_persistent_leaf_distance",
            "mismatch_count", "mismatch_kinds", "chunks_spanned", "missing_chunks", "incomplete_chunks",
             "foundation_contact", "feature_protection", "passed")
    for instance in block_report.get("instances", []):
        instances.append({k: instance[k] for k in keys if k in instance})
    return {"run": report["run_directory"].replace("\\", "/").rsplit("/", 1)[-1],
            "report_sha256": hashlib.sha256(raw).hexdigest(),
            "seed": report["seed"], "showcase": report.get("showcase", False),
            "integration_mods": report.get("integration", False), "artifacts": report["artifacts"],
            "passed": report["passed"], "failure": report.get("failure"), "exit_code": report["exit_code"],
            "blocking_log_errors": report.get("blocking_log_errors", []),
            "expected_natural_structures": report.get("expected_natural_structures", []),
             "selected_templates": report.get("selected_templates", []),
             "locate_origin": report.get("locate_origin"),
            "locate_results": report.get("locate_results", []),
            "disabled_locate_results": report.get("disabled_locate_results", []),
            "locate_timings": [{"command": c["command"], "seconds": c["elapsed_seconds"]}
                               for c in report.get("commands", []) if "locate structure " in c["command"]],
            "instances": instances, "read_errors": block_report.get("read_errors", []),
             "verification_errors": block_report.get("verification_errors", []),
             "overlaps": block_report.get("overlaps", [])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {"schema_version": 1, "scope": "saved-world server evidence, not client visual or gameplay approval",
              "runs": [summarize(p) for p in args.report]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"Recorded {len(result['runs'])} completed runtime runs in {args.output}")


if __name__ == "__main__":
    main()
