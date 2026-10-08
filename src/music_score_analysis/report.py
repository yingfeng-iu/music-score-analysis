"""Render the analysis as a self-contained static HTML document."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def _bar_chart(values: dict[str, int], title: str) -> str:
    maximum = max(values.values(), default=1) or 1
    bars = []
    for label, value in values.items():
        width = 100 * value / maximum
        bars.append(
            f'<div class="bar-row"><span>{html.escape(label)}</span>'
            f'<div class="track"><i style="width:{width:.1f}%"></i></div><b>{value}</b></div>'
        )
    return f'<figure><figcaption>{html.escape(title)}</figcaption>{"".join(bars)}</figure>'


def _score_card(result: dict[str, Any]) -> str:
    pitch_range = result["written_pitch_range"]
    pitch_range_text = (
        f"{pitch_range['lowest']} to {pitch_range['highest']}" if pitch_range else "No pitched notes"
    )
    estimate = result["estimated_key"]
    estimate_text = (
        f"{estimate['name']} <small>(correlation {estimate['correlation']:.3f})</small>"
        if estimate
        else "Unavailable"
    )
    pitch_sequence = " · ".join(result["preview_pitches"])
    return f"""
      <article class="score-card" id="{html.escape(result['id'])}">
        <div class="card-heading">
          <div><p class="eyebrow">Synthetic MusicXML fixture</p><h3>{html.escape(result['title'])}</h3>
          <p>{html.escape(result['composer'])}</p></div>
          <a class="source-link" href="../samples/{html.escape(result['source_file'])}">MusicXML source</a>
        </div>
        <div class="evidence"><span>Notation evidence</span><p>{html.escape(pitch_sequence)}</p>
          <small>First written pitches in score order; a compact preview, not engraved notation.</small></div>
        <dl class="facts">
          <div><dt>Parts</dt><dd>{html.escape(', '.join(part['label'] for part in result['parts']))}</dd></div>
          <div><dt>Measures</dt><dd>{result['measure_count']}</dd></div>
          <div><dt>Meter</dt><dd>{html.escape(', '.join(result['time_signatures']))}</dd></div>
          <div><dt>Key signature</dt><dd>{html.escape(', '.join(result['key_signatures']))}</dd></div>
          <div><dt>Notes</dt><dd>{result['note_count']}</dd></div>
          <div><dt>Written range</dt><dd>{html.escape(pitch_range_text)}</dd></div>
        </dl>
        <div class="estimate"><span>Computed estimate</span><strong>{estimate_text}</strong>
          <small>Algorithmic key estimate; not the same as the encoded key signature.</small></div>
        <div class="charts">
          {_bar_chart(result['pitch_class_counts'], 'Written pitch-class counts')}
          {_bar_chart(result['duration_counts_quarter_notes'], 'Notated durations (quarter-note units)')}
        </div>
      </article>"""


def build_report(
    analyses: list[dict[str, Any]], comparison: dict[str, Any], output_path: str | Path
) -> None:
    """Write one offline-friendly HTML report containing all data and styles."""
    cards = "".join(_score_card(result) for result in analyses)
    comparison_rows = "".join(
        f"<tr><th>{html.escape(row['title'])}</th><td>{row['note_count']}</td>"
        f"<td>{row['short_note_proportion']:.0%}</td><td>{row['distinct_pitch_classes']}</td></tr>"
        for row in comparison["rows"]
    )
    observations = "".join(f"<li>{html.escape(item)}</li>" for item in comparison["observations"])
    embedded_data = html.escape(json.dumps({"scores": analyses, "comparison": comparison}))
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Music Score Analysis Explorer</title>
<style>
:root{{--ink:#18201d;--muted:#59645f;--paper:#fbfaf5;--green:#195f4b;--gold:#d79a31;--line:#d9ded8}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.55 system-ui,sans-serif}}
header,main,footer{{max-width:1120px;margin:auto;padding:2rem}} header{{padding-top:5rem;padding-bottom:4rem}}
h1{{font:clamp(2.7rem,7vw,5.7rem)/.95 Georgia,serif;max-width:850px;margin:.25rem 0 1.5rem}} h2{{font:2.2rem Georgia,serif;margin-top:3rem}} h3{{font:1.8rem Georgia,serif;margin:.1rem 0}}
.lede{{font-size:1.25rem;max-width:760px}} .eyebrow,.tag{{text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;font-weight:750;color:var(--green)}}
.method{{display:grid;grid-template-columns:repeat(5,1fr);gap:.5rem;margin:2rem 0}} .method div{{padding:1rem;border:1px solid var(--line);background:white;text-align:center}} .method b{{display:block;color:var(--gold)}}
.notice{{border-left:5px solid var(--gold);padding:1rem 1.25rem;background:#fff7e7}}
.score-card{{background:white;border:1px solid var(--line);padding:clamp(1.2rem,4vw,2.3rem);margin:1.5rem 0 3rem;box-shadow:0 10px 30px #17251f0a}}
.card-heading{{display:flex;justify-content:space-between;gap:1rem;align-items:start}} .source-link{{color:var(--green);font-weight:700}}
.evidence{{background:#17251f;color:white;padding:1rem 1.25rem;margin:1.5rem 0}} .evidence span,.estimate span{{display:block;text-transform:uppercase;letter-spacing:.1em;font-size:.72rem;color:#c7e5d9}} .evidence p{{font:1.2rem Georgia,serif;word-spacing:.35rem}}
.facts{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}} .facts div{{background:white;padding:.8rem}} dt{{color:var(--muted);font-size:.8rem;text-transform:uppercase}} dd{{margin:0;font-weight:700}}
.estimate{{background:#edf5f1;padding:1rem;margin:1.5rem 0}} .estimate span{{color:var(--green)}} .estimate strong,.estimate small{{display:block}}
.charts{{display:grid;grid-template-columns:1fr 1fr;gap:2rem}} figcaption{{font-weight:750;margin-bottom:.8rem}} .bar-row{{display:grid;grid-template-columns:4.3rem 1fr 2rem;gap:.5rem;align-items:center;font-size:.82rem;margin:.3rem 0}} .track{{height:.75rem;background:#edf0ed}} .track i{{display:block;height:100%;background:var(--green)}}
table{{width:100%;border-collapse:collapse;background:white}} th,td{{padding:.8rem;text-align:left;border-bottom:1px solid var(--line)}} thead th{{color:var(--muted);font-size:.78rem;text-transform:uppercase}} .limitations{{background:#eee9dd;padding:1.5rem}}
footer{{color:var(--muted);font-size:.9rem}} small{{color:var(--muted)}}
@media(max-width:720px){{.method{{grid-template-columns:1fr}}.facts{{grid-template-columns:1fr 1fr}}.charts{{grid-template-columns:1fr}}.card-heading{{display:block}}}}
</style></head><body>
<header><p class="eyebrow">Milestone A · Symbolic analysis first</p><h1>What can a music score tell us before AI interpretation?</h1>
<p class="lede">Three tiny, known MusicXML examples make the evidence trail visible: encoded notation becomes explainable measurements, then a modest comparison.</p></header>
<main><section><h2>Method</h2><div class="method"><div><b>1</b>Known MusicXML</div><div><b>2</b>Parse notation</div><div><b>3</b>Count features</div><div><b>4</b>Compare proportions</div><div><b>5</b>Human review</div></div>
<p class="notice"><strong>No OMR or LLM is used here.</strong> These original synthetic fixtures prove the analysis path; they do not represent archival material or recognition accuracy.</p></section>
<section><h2>Score analyses</h2>{cards}</section>
<section><h2>Comparison</h2><p>“Short notes” means written durations below one quarter note. Distinct pitch classes ignore octave. Both definitions are intentionally simple and visible.</p>
<table><thead><tr><th>Work</th><th>Notes</th><th>Short notes</th><th>Pitch classes</th></tr></thead><tbody>{comparison_rows}</tbody></table>
<h3>Evidence-based observations</h3><ul>{observations}</ul><p><small>These observations describe only the displayed fixtures. They are not claims about style, quality, provenance, or influence.</small></p></section>
<section class="limitations"><h2>Limits and next questions</h2><ul><li>Written pitches are not converted for transposing instruments.</li><li>A key signature is encoded notation; the named key is an algorithmic estimate.</li><li>Pitch and duration distributions discard order, harmony, articulation, text, and cultural context.</li><li>Synthetic success does not predict OMR quality on printed or handwritten scans.</li></ul>
<p><strong>What would you want to search for in 17,000 scores?</strong> Concrete scholarly questions should determine which features—and which validation—come next.</p></section>
<details><summary>Embedded machine-readable analysis</summary><pre>{embedded_data}</pre></details></main>
<footer>Generated from the repository's MusicXML fixtures with music21. See README.md and samples/SOURCES.md for method and provenance.</footer></body></html>"""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(document, encoding="utf-8")
