# Music Score Analysis Explorer

This is a small, public proof of concept for examining symbolic music scores in
a form that musicologists and collection managers can inspect. The first
milestone deliberately starts with known MusicXML: it demonstrates what can be
measured and compared before optical music recognition (OMR) or language models
add uncertainty.

## View the demonstration

## Demo

**[View the rendered prototype report](https://yingfeng-iu.github.io/music-score-analysis/)**, published through GitHub Pages.

The report is self-contained and can also be viewed offline by opening
[`demo/index.html`](demo/index.html) in a browser. No server, Python installation,
account, network connection, or API key is required.

The report analyzes three short original teaching fixtures and shows:

- encoded facts such as title, composer label, meter, and key signature;
- computed note counts, written pitch ranges, pitch-class frequencies, note
  durations, and melodic intervals;
- an estimated key, clearly separated from the encoded key signature; and
- a transparent comparison with observations traceable to the displayed data.

The examples are synthetic and are **not archival scores**. They exist to make
the analysis path reproducible and testable. Their provenance and terms are in
[`samples/SOURCES.md`](samples/SOURCES.md).

## What this does not establish

Pitch and rhythm summaries do not establish genre, authorship, cultural
tradition, historical influence, or overall musical similarity. Measurements
use written pitch; transposing instruments would require an explicit
written-versus-concert-pitch policy. The estimated key is an algorithmic result,
not a confirmed tonal analysis. No OMR or LLM is used in Milestone A.

## Reproduce the analysis

Python 3.11 or newer is recommended. From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python scripts/build_demo.py
.venv/bin/python -m pytest
```

The build command parses `samples/*.musicxml`, writes the reviewable feature
data to `outputs/analysis.json`, and regenerates `demo/index.html`. The report
contains no external assets, so direct `file://` viewing works.

The companion notebook, [`notebooks/explore_scores.ipynb`](notebooks/explore_scores.ipynb),
walks through the same parsing and comparison functions without requiring an
LLM key. To execute it after installing the development dependencies:

```bash
.venv/bin/jupyter-nbconvert --execute --to notebook --output-dir /tmp notebooks/explore_scores.ipynb
```

## Repository map

```text
src/music_score_analysis/  MusicXML feature extraction and HTML generation
scripts/build_demo.py       Rebuild entry point
samples/                    Small MusicXML fixtures and provenance
outputs/analysis.json       Generated, inspectable feature data
demo/index.html             Primary shareable artifact
notebooks/                  Reproducible guided exploration
tests/                      Focused feature checks
```

`Notes.md` describes the broader research context. `Prototype.md` defines the
milestones and boundaries. OMR evaluation is intentionally deferred until this
symbolic-analysis baseline has been reviewed.

## Current result and limitations

Milestone A provides a deterministic MusicXML-to-analysis-to-HTML path. The
fixtures make expected contrasts easy to verify, but success on them says
nothing about OMR accuracy or a 17,000-score collection. A next milestone would
test one OMR backend on a legally reusable printed score, compare the recognized
notation with ground truth, and report errors rather than treating parse success
as musical accuracy.
