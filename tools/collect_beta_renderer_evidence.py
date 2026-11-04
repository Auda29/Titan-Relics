"""Retain the manually reviewed real-client renderer matrix without changing fixtures."""
import hashlib
import json
import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = Path("E:/Relic_Mod_QA/renderer-20261104")
EXPECTED = {
    "fabric-1.21.1": "a10c4e665798568064ffb8eb37a25c8ded86d193ae5e4e3d785c3091243b9c16",
    "fabric-26.2": "9ce11af173ebfd5e2db2ad85a38133c1b1bcc7832154a4dee0c5ee1df01a6508",
    "neoforge-1.21.1": "86bb9380a3ed80d9bd2a15d51d1e444f2faba3a0aa53832acce52defce5cf50d",
    "neoforge-26.2": "bfd259fe5369e3ad42a00550e11f20f44459b5a748a317d29d8f359233dee486",
}


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def binding(path):
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def main():
    selection = json.loads((SCRATCH / "review-selection.json").read_text())
    result = {
        "date": "2026-11-04",
        "scope": "Roadmap point 4, real renderer additions to existing gameplay acceptance",
        "fixture": "Operator exhibition of exact JAR templates with native marker replacements; armour is operator equipment",
        "limitations": [
            "No new natural-generation, Survival, lighting or performance acceptance",
            "Interrupted earlier processes keep unknown exits; reviewed images remain individual evidence",
            "JVM-local hosts file prevents normal external DNS resolution, not an OS network firewall",
        ],
        "rejected_images": selection["rejected"],
        "manual_review_selection": selection["selected_runs_in_override_order"],
        "targets": {},
    }
    for target, run_names in selection["selected_runs_in_override_order"].items():
        version = "21" if "1.21.1" in target else "26"
        expected = [s["label"] for s in json.loads((SCRATCH / f"cases{version}.json").read_text()) if "load footprint" not in s["label"]]
        expected += ["worn Monolith amethyst armor front operator equipment", "worn Monolith amethyst armor rear"]
        chosen = {}
        runs = []
        for run_name in run_names:
            run = SCRATCH / run_name
            artifact = next(run.glob("mods/relics-*.jar"))
            if sha(artifact) != EXPECTED[target]:
                raise AssertionError(f"Unexpected tested artifact: {run}")
            labels = [line.split(" ", 1)[1] for line in (run / "visual-actions.log").read_text().splitlines()]
            screenshots = sorted((run / "screenshots").glob("*.png"))
            if len(labels) != len(screenshots):
                raise AssertionError(f"Label/image mismatch: {run}")
            rejected = {e["label"] for e in selection["rejected"] if e["run"] == run_name}
            for label, screenshot in zip(labels, screenshots):
                if label not in expected or label in rejected or "all" in rejected:
                    continue
                with Image.open(screenshot) as image:
                    image.load()
                    if image.size != (1280, 720):
                        raise AssertionError(f"Unexpected capture dimensions: {screenshot}")
                chosen[label] = (run_name, screenshot)
            process_file = run / "process.json"
            process = json.loads(process_file.read_text()) if process_file.exists() else None
            if process and process.get("exit") not in (0, None):
                raise AssertionError(f"Selected unsuccessful process: {run}")
            source_files = [p for p in run.glob("sources/*.java")]
            files = [run / "client-args.txt", run / "options.txt", run / "loopback-hosts.txt", run / "visual-actions.log", run / "visual-cases.json", run / "console.log"]
            files += list(run.glob("visual-state.jsonl")) + list(run.glob("visual-proof.txt"))
            files += list(run.glob("mods/*checks.jar")) + source_files
            logs = (run / "console.log").read_text(errors="replace")
            runs.append({
                "run": str(run), "artifact": binding(artifact),
                "exit": process.get("exit") if process else None,
                "exit_note": "Exit recorded by launcher" if process and process.get("exit") is not None else "Earlier run interrupted by user; no successful exit claimed",
                "process": binding(process_file) if process_file.exists() else None,
                "pid": process.get("pid") if process else None,
                "started": process.get("started") if process else None,
                "ended": process.get("ended") if process else None,
                "java_args": (run / "client-args.txt").read_text(),
                "scene_definitions": json.loads((run / "visual-cases.json").read_text()),
                "files": [binding(p) for p in files],
                "external_dns_failures": sorted(set(re.findall(r"UnknownHostException: ([A-Za-z0-9.-]+)", logs))),
                "http_401_present": "HTTP 401" in logs or "status: 401" in logs or "status code: 401" in logs,
                "mute_option_present": "soundCategory_master:0.0" in (run / "options.txt").read_text(),
            })
        missing = sorted(set(expected) - chosen.keys())
        if missing:
            raise AssertionError(f"Missing reviewed scenes for {target}: {missing}")
        images = []
        for index, label in enumerate(expected, 1):
            run_name, screenshot = chosen[label]
            filename = f"{index:02d}-" + re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-") + ".png"
            retained = ROOT / "docs/testing/images/beta-renderer-20261104" / target / filename
            retained.parent.mkdir(parents=True, exist_ok=True)
            if retained.exists() and sha(retained) != sha(screenshot):
                raise AssertionError(f"Refusing to overwrite different retained evidence: {retained}")
            if not retained.exists():
                shutil.copy2(screenshot, retained)
            if sha(retained) != sha(screenshot):
                raise AssertionError(f"Retention mismatch: {retained}")
            images.append({"label": label, "review": "Root inspected in view_image, directly or on labelled contact sheet", "run": run_name, "source": binding(screenshot), "retained": binding(retained)})
        result["targets"][target] = {"artifact_sha256": EXPECTED[target], "reviewed_images": len(images), "images": images, "runs": runs}
    result["reviewed_images"] = sum(t["reviewed_images"] for t in result["targets"].values())
    result["collection_sources"] = [binding(Path(__file__)), binding(ROOT / "src/test/client/de/relics/testmixin/BetaVisualDriver.java")]
    validation = SCRATCH / "final-preservation.json"
    if validation.exists():
        result["validation"] = json.loads(validation.read_text())
    output = ROOT / "docs/testing/beta-renderer-acceptance-20261104.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Retained and hash-verified {result['reviewed_images']} reviewed screenshots: {output}")


if __name__ == "__main__":
    main()
