"""Build the committed Milestone A data and static demonstration."""

from __future__ import annotations

import json
from pathlib import Path

from music_score_analysis import analyze_score, build_report, compare_scores

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    sample_paths = sorted((ROOT / "samples").glob("*.musicxml"))
    if not sample_paths:
        raise SystemExit("No MusicXML samples found in samples/")
    analyses = [analyze_score(path) for path in sample_paths]
    comparison = compare_scores(analyses)
    output = {"method": "music21 written-pitch analysis", "scores": analyses, "comparison": comparison}
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "analysis.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    build_report(analyses, comparison, ROOT / "demo" / "index.html")
    print(f"Analyzed {len(analyses)} scores; wrote outputs/analysis.json and demo/index.html")


if __name__ == "__main__":
    main()
