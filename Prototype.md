# Music Score AI Explorer — Prototype Implementation Brief

**Date:** 8 October 2026  
**Project type:** Personal, public, exploratory proof of concept. Not an AMPAV implementation or an IU-sponsored project.  
**Companion document:** `Notes.md` (research landscape and context).

## 1. Goal and audience

Build a **small, reproducible, visually accessible demonstration** of how existing tools can recognize and analyze digitized musical scores and compare a few works. The intended audience includes musicologists and collection managers who may have no programming background. Optimize for **a compelling, honest, five-minute walkthrough**, not for a production library or collection-scale pipeline.

The prototype should answer:

1. Can a scan or PDF of printed music be converted to useful MusicXML?
2. What musical characteristics can be extracted from the resulting symbolic score?
3. Can two or more scores be compared in an interpretable way?
4. Optionally, can an LLM summarize computed evidence without making unsupported musicological claims?

The demo should remain useful **without any LLM API access** and **even if OMR fails on a difficult score**.

## 2. Operating environment and constraints

- Develop in **WSL/Linux**, in a **separate directory and Python virtual environment** from AMPAV. Use the existing developer's installation as convenient, but do not import AMPAV workflows, namespace packages, workflow phases, status/roadmap/summary machinery, Jira conventions, or core libraries.
- Public personal GitHub repository; avoid IU-restricted materials, private scans, credentials, local paths, or licensed assets that cannot be redistributed. The repository URL has not been specified in this brief.
- Prefer open-source, documented, actively usable tools. Review dependency and model licenses before redistribution or embedding in the project; do not copy third-party code or weights into the repository by default.
- Keep implementation minimal, with direct Python functions/scripts, a notebook, and a static HTML export. Avoid service frameworks, databases, queues, generic pipelines, or elaborate abstraction layers.
- Record dependency versions and exact commands needed to reproduce the demo. No requirement for AMPAV-style retained native run manifests.
- No deployment to a public server, no paid API calls without explicit approval, and no unapproved upload of score images to cloud LLM services.

## 3. Technical choices and order of implementation

### Milestone A — guaranteed working symbolic-analysis path (first)

1. Select **2–3 small, legally reusable examples** with existing MusicXML, or create tiny synthetic MusicXML fixtures with known contents. Use varied meter/rhythm/pitch to make comparison visible; do not present synthetic examples as archival sources.
2. Implement analysis using **music21**. Candidate initial features:
   - work title/composer if encoded (label absent data as unknown);
   - parts/instrument labels, measure count, notated time and key signatures;
   - note count, pitch range, pitch-class histogram;
   - note-duration distribution, simple melodic interval profile where a monophonic part can be identified;
   - optionally an estimated key, explicitly labeled as an estimate.
3. Make a per-score HTML view and a small cross-score comparison. Include understandable labels and brief explanations of what each feature measures.
4. Avoid misleading aggregation: do not mix transposing parts without acknowledging written/concert pitch, do not call a key signature a confirmed tonal center, and do not infer style/genre from a pitch histogram.

**Exit criterion:** a nontechnical reader can open one HTML file and see two or more score analyses and a comprehensible comparison, with no network connection or Python execution.

### Milestone B — image/PDF-to-MusicXML recognition

1. Evaluate **Audiveris** and **homr** installation and CLI documentation. Choose **one** initial OMR backend based on reproducibility, dependency burden, and an actual test on a clean printed score. Do not implement both unless a short comparison materially helps.
2. Accept a sample image or PDF and produce a MusicXML derivative. If the tool needs a separate Java or model environment, document that clearly rather than hiding installation complexity.
3. Validate that the exported file parses with music21 and contains plausible measures/notes. **Parse success is not musical accuracy.**
4. Show source page next to a rendering of recognized notation, where feasible. Consider MuseScore CLI or another documented renderer; if rendering is impractical, show an excerpt/preview and provide the MusicXML download link.
5. Report missing symbols, note/measure mismatches, and any obvious OMR errors. If an OMR output is unusable, show the failure and continue the rest of the demo using an explicitly labeled verified MusicXML fallback.

**Exit criterion:** at least one real score image follows the scan → OMR → MusicXML → analysis path, or a documented technical/quality blocker is shown with the independent symbolic-analysis demo still functioning.

### Milestone C — small collection comparison

- Use **3–5 works if available**; otherwise 2–3 is sufficient for the first version.
- Create one simple comparison chart or table using clearly defined, normalized features (for example, pitch-class frequencies and duration proportions). A similarity ranking is optional; if included, state its metric, selected features, and limitations.
- Include at least one plain-language observation directly traceable to the computed results, such as “Work A has a larger proportion of short notated durations than Work B.”
- Do not label a cluster or similarity result as proof of common authorship, genre, historical influence, or cultural tradition.

### Milestone D — optional LLM description (only after A–C work)

- Prefer a **provider-neutral, manually optional step** that consumes only the computed evidence and public metadata, not raw scans by default.
- If no suitable API/local model is configured, include a **clearly labeled illustrative prompt and expected output structure**, but do not fabricate a model-generated result or claim a live LLM experiment occurred.
- Ask for a short evidence-grounded musical description, separating observed, computed/estimated, and interpretive statements. Require the model to state when style, influence, or historical context cannot be established from the supplied features.
- Show the prompt, model/provider/version when used, and generated text with an “experimental, not expert-verified” warning.
- Never send restricted source materials to external providers without approval.

## 4. Primary deliverables

**A. Public-facing `README.md`**

Explain the motivation, what the demo actually shows, what it does not establish, how to view results, where the source examples came from, and how to run it. Keep the first screen comprehensible to a musicologist; move environment and engineering details lower down.

**B. Static, self-contained or locally linked HTML demo (`demo/index.html`)**

This is the **primary artifact for sharing**. It should open in an ordinary browser without Jupyter, Python, a running server, an account, or an API key. Include:

- Short introduction and method diagram.
- A gallery of source scores, with title, composer, source/license, and original scan preview when redistribution is allowed.
- Side-by-side original/recognized notation where possible, with clear OMR quality notes.
- For each work: a short feature summary and 1–2 legible charts.
- A comparison section with at least one substantive, evidence-based observation.
- Optional LLM interpretation section, clearly marked as experimental.
- Limitations and a short “What would you want to search for in 17,000 scores?” invitation.

Favor restrained typography, large readable score images, descriptive chart titles, and minimal technical jargon. Check relative links and images when opened directly from disk and when browsed on GitHub. If GitHub cannot render the HTML directly, make the README link to the HTML file and provide a practical viewing option; GitHub Pages may be considered later, but **do not publish/deploy it without authorization**.

**C. Reproducible analysis notebook (`notebooks/explore_scores.ipynb`)**

Show the steps from MusicXML parsing to features, plots, and comparison. Use a small amount of explanatory text. The notebook may call short reusable functions rather than duplicate the implementation. It must run without any LLM key.

**D. Minimal implementation and sample inputs**

Keep scripts/modules and `samples/` simple. Include source/license documentation for every sample, and do not commit large downloaded corpora or pretrained weights. Retain small MusicXML derivatives and representative score thumbnails if licenses permit.

**E. Short results/limitations section**

In the README or `Results.md`, state what actually worked, which OMR backend and version were used, where the recognition was wrong or uncertain, what the computed features mean, and what would need validation by a musicologist. Do not overstate success.

## 5. Suggested lightweight repository layout

```text
README.md
Notes.md
Prototype.md
pyproject.toml                 # or requirements.txt, choose one
src/                           # minimal analysis/report helpers
notebooks/explore_scores.ipynb
samples/                       # small licensed source images and/or MusicXML
samples/SOURCES.md              # attribution, rights, provenance
outputs/                       # generated MusicXML / analysis JSON, if useful
 demo/index.html                # shareable report (actual directory: demo/)
```

Adapt layout if simpler. Avoid duplicating large assets. Decide which generated artifacts should be committed based on whether they are needed for a self-contained public demonstration. Use `.gitignore` for local environments, caches, downloaded model files, and scratch outputs.

## 6. Execution approach

1. **Inspect** the new repository and local WSL environment. Confirm Python version, package manager, rendering/OMR availability, and repo state; do not assume an AMPAV venv is appropriate.
2. **Confirm sample rights** and choose a tiny, representative dataset. Start with music21's built-in corpus or other licensed symbolic examples if necessary, but prefer a score image with corresponding ground-truth MusicXML for OMR assessment.
3. **Implement Milestone A first**, including an HTML report and notebook. Show the user a sample before adding OMR complexity.
4. **Try one OMR backend** and record practical quality observations. If installation or recognition becomes a time sink, preserve the working symbolic demo and report the blocker.
5. **Add the comparison view**, then consider optional LLM enrichment only if the core demonstration is coherent.
6. **Validate** with a clean-environment install where feasible, a notebook execution, parseable MusicXML, report regeneration, and browser inspection of the generated HTML. Add only focused automated tests for nontrivial feature computations.
7. **Report** what is finished, exact commands, sample provenance, limitations, and the best link/file to share. Request user approval before remote pushes, Pages deployment, external API usage, or other public publication steps.

Do not spend substantial time optimizing, benchmarking multiple models, or implementing a general OMR abstraction before there is an actual working demo.

## 7. Review checklist

- [ ] The HTML demo is understandable without programming knowledge.
- [ ] It contains original score evidence, MusicXML/notation evidence, computed features, and a comparison.
- [ ] It distinguishes catalog facts, recognized notation, computed/estimated features, and interpretation.
- [ ] Sample sources, licenses, and any third-party attribution are documented.
- [ ] The notebook runs without an LLM key; missing optional dependencies fail gracefully.
- [ ] OMR failure does not prevent viewing the other results.
- [ ] No unverified claim of style, influence, provenance, or collection-wide accuracy appears.
- [ ] README instructions and all links/images work for the intended viewing path.
- [ ] No private files, credentials, or unapproved provider uploads are included.

## 8. Explicitly out of scope for this first version

Full manuscript OMR, 17K-score ingestion, production cataloging, user authentication, search database, vector index, music-specific model fine-tuning, score-audio alignment, Avalon integration, AMPAV APIs/schemas, production monitoring, and polished interactive web applications. These are follow-up research possibilities, not requirements.

## 9. Reference links

See `Notes.md` for context and primary sources. Initial implementation references:

- https://music21.org/music21docs/about/what.html
- https://github.com/Audiveris/audiveris
- https://github.com/liebharc/homr
- https://www.musicxml.com/
- https://partitura.readthedocs.io/en/latest/index.html

**Definition of success:** a musicologist can view a small set of real, legally shareable score examples, understand which musical properties were extracted, compare works, and identify useful questions for a possible larger study—even if some OMR recognition fails and no LLM is used.
