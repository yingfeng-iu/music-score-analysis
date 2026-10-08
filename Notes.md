# Exploring AI-Assisted Analysis and Discovery of Digitized Music Scores

**Preliminary research and project concept — 8 October 2026**  
**Status:** Exploratory; not a funded or formally scoped project.

## Executive overview

A recent informal conversation with Javier Leon, Director of Latin American Music at Indiana University, identified an opportunity to investigate AI-assisted cataloging, analysis, and discovery for a collection described as approximately **17,000 music scores**. The collection reportedly includes printed and handwritten material; its precise inventory, digitization status, rights, formats, and catalog coverage have not yet been established. Existing descriptive cataloging may include composer, title, and date, while content-oriented musical descriptions and collection-wide analytical discovery are limited.

This note explores how existing optical music recognition (OMR), computational musicology, machine learning, and large language models might help. It is a personal, exploratory technology study intended to support discussion with musicologists and collection stewards, not a commitment by IU Libraries, Music School, AMPAV, or Avalon/MCO. The central proposition is to **turn score images into reviewable musical evidence, then use that evidence for descriptive metadata and cross-collection discovery**. The feasibility and usefulness of this approach remain to be tested.

## Research questions and possible value

A musicologist or collection manager might wish to:

- Search by musical content rather than only title, composer, or date: instrumentation, meter, pitch range, characteristic rhythmic patterns, or recurring motifs.
- Compare works or composers by measurable melodic, rhythmic, harmonic, or textural features.
- Identify potential stylistic groupings or relationships that warrant scholarly investigation.
- Obtain draft descriptions of compositional techniques, with evidence and appropriate uncertainty.
- Find candidate matches between a digitized score and a performance recording, or navigate a recording using its score.
- Prioritize human review of scores that can be recognized and analyzed reliably, while flagging uncertain material.

These are **candidate research questions**, not confirmed requirements. Examples involving Latin American styles and traditions require domain expertise; generic Western-classical feature sets may omit crucial rhythmic, cultural, or notational characteristics.

## A layered technical approach

```text
Digitized score image / PDF       Existing MusicXML / MEI / MIDI, if any
             |                                  |
             v                                  |
   image preparation + OMR                       |
             |                                  |
             +-------------+--------------------+
                           v
               structured musical notation
                           |
                           v
            computational musical analysis
                           |
             +-------------+-------------------+
             |                                 |
             v                                 v
    measurable features              optional LLM interpretation
             |                                 |
             +----------------+----------------+
                              v
                  reviewable metadata
                              |
                              v
                 comparison and discovery
```

The stages should remain distinguishable. An inaccurate OMR transcription can corrupt all downstream analysis; polished AI prose does not establish correctness.

### 1. Text OCR versus optical music recognition

**OCR** extracts textual elements such as titles, composer names, lyrics, annotations, and performance directions. It does not, by itself, reconstruct pitches, note durations, voices, or measure structure. **OMR** attempts to recover that musical notation and export a symbolic representation such as MusicXML.

Candidate OMR systems:

| Candidate | What it offers | Considerations |
| --- | --- | --- |
| [Audiveris](https://github.com/Audiveris/audiveris) | Mature open-source score-image-to-MusicXML workflow with interactive correction and multi-page support. | Java-based; focus on printed common Western notation; automatic recognition is imperfect. GPL compatibility and redistribution need review before reuse. |
| [homr](https://github.com/liebharc/homr) | Python-oriented image/PDF-to-MusicXML OMR; documented CPU and optional GPU execution. | Model/runtime dependencies; test recognition accuracy and layout complexity; repository is AGPL-3.0. |
| [Sheet Music Transformer](https://github.com/antoniorv6/SMT) | Research implementation for end-to-end, full-page, polyphonic OMR. | Research-oriented, with dataset and notation-domain constraints; defer unless first-line tools prove inadequate. |

**Printed versus handwritten scores must be evaluated separately.** Historical handwriting, marginal corrections, degraded scans, unusual notation, and complex polyphony may defeat tools trained mainly on modern engraved notation. No general manuscript-recognition capability should be assumed.

### 2. Symbolic representations

- **[MusicXML](https://www.musicxml.com/)** is the practical initial interchange format for OMR output, score editors, and Python analysis.
- **[MEI](https://music-encoding.org/)** is especially relevant to scholarly music encoding, source description, editorial detail, and historical documents. It should remain in the broader research scope, without making it a prototype requirement.
- **MIDI** can represent note events and support playback or some ML pipelines, but may discard important notational and editorial distinctions.

Retain source images and metadata alongside symbolic derivatives. A generated MusicXML file is a machine interpretation, not a replacement for the archival original.

### 3. Computational musicology

**[music21](https://music21.org/music21docs/about/what.html)** is the preferred starting point. It is a Python toolkit designed for computer-aided musicology and studying large collections. It can parse symbolic music, inspect notes and measures, and support key estimation, interval/rhythm analysis, corpus queries, and other music-theoretical computations.

**[Partitura](https://partitura.readthedocs.io/en/latest/index.html)** is a complementary Python library for symbolic score/performance representations, feature extraction, and alignment-related data. It is worth revisiting for performance-oriented experiments rather than installing by default for the first demo.

Candidate features, conditional on score quality and musical suitability:

| Feature | Evidence type | Caveat |
| --- | --- | --- |
| Part/instrument names, clefs, meter, key signature | Read from symbolic notation | May be absent or misrecognized; key signature is not the same as actual tonality. |
| Note counts, pitch ranges, pitch-class distributions | Directly computed | Sensitive to incomplete pages and transposing instruments. |
| Note-duration and rhythmic distributions | Directly computed | Does not automatically identify culturally specific rhythms or syncopation. |
| Interval distributions and melodic contour | Computed with voice/part assumptions | Polyphony and voice separation matter. |
| Estimated key, harmonic patterns | Model/rule-based inference | Context-dependent, unreliable for some styles and non-tonal material. |
| Motifs, texture, form | More advanced analysis | No universal reliable detector; needs carefully defined method and expert review. |

The prototype should start with a few understandable features and **not** claim it has identified a genre, compositional influence, or specific Latin American rhythmic tradition merely from a distribution plot.

### 4. Higher-level musicological interpretation

A general-purpose LLM may be useful for converting *verified or qualified* musical observations into accessible draft descriptions and research hypotheses. Possible inputs include source/catalog metadata, score excerpts, structured features, and relevant scholarship. Possible outputs include a short synopsis, instrumentation and texture observations, candidate analytical questions, and clearly qualified stylistic interpretations.

A multimodal LLM can also be tested directly on score images, but it should **not** be assumed to read notes or analyze harmony reliably. Prefer grounding its descriptions in symbolic features, with links back to source passages and clear labels distinguishing:

1. **Observed** — explicitly present in source/catalog or verified notation.
2. **Computed/estimated** — produced by a named algorithm, with limitations.
3. **Interpretive** — tentative musical, stylistic, historical, or cultural inference.

Historical background and influence claims need external, citable scholarship; they cannot be established from the score alone. Model output should be labeled as experimental and subject to expert review.

### 5. Specialized music models and semantic discovery

Research on symbolic-music representation learning includes **[MusicBERT](https://github.com/microsoft/muzic/blob/main/musicbert/README.md)**, which targets symbolic music understanding and reports tasks including genre/style classification. Such models could eventually support clustering or candidate similarity, but performance on a Latin American archival corpus is unknown and may be affected by training-data bias.

A pragmatic first collection-comparison experiment should use transparent features: normalize simple pitch/rhythm statistics, compare several works, and explain *which* features contributed to a similarity result. Later work could compare specialized music embeddings and semantic retrieval over evidence-grounded descriptions. “Musical similarity” must be specified: similarity in instrumentation, melody, harmony, rhythm, texture, or scholarly interpretation are different targets.

### 6. Scores plus audio/video: possible connection to Avalon/MCO

Some audiovisual collections contain associated scores, programs, lyrics, or other documents. These could become complementary evidence for musical identification and discovery. Candidate future tasks include:

- Matching a performance recording to candidate scores.
- Aligning score measures/passages to recording timestamps for navigation.
- Comparing performances of the same work by tempo, timing, or articulation.
- Cross-checking score instrumentation or musical structure against audio-derived observations.

**[Sync Toolbox](https://github.com/groupmm/synctoolbox)** provides open-source music synchronization based on dynamic time warping. **Partitura** can represent symbolic score/performance data. Both are research candidates, not evidence that score-to-archival-audio alignment will work reliably across the collection. Different arrangements, improvisation, repeats, recording quality, and performance deviations complicate alignment.

This work is adjacent to the [AMPAV project](https://github.com/search?q=AMPAV&type=repositories) and the [Avalon Media System](https://avalon.samvera.org/), but the present exploration is independent. Avalon/MCO integration is a possible future use case, not a prototype dependency.

## Why 17,000 scores changes the question

A successful demonstration on one clean score is not a collection-scale solution. A future feasibility study should quantify:

- Digitization coverage and scan quality; printed/manuscript/notation-system proportions.
- Percentage of scores yielding parseable, musically plausible symbolic output.
- Human correction time and OMR error patterns, not merely whether a file exports.
- Quality of downstream features and scholarly usefulness of descriptions.
- Throughput, compute needs, storage, rights, access controls, and licensing.
- Whether retrieval and comparison answer actual user questions better than existing catalog search.

A practical long-term design would combine automated processing with selective human review. This is a research hypothesis, not an implementation plan for the full collection.

## Small initial demonstration

Use **2–3 representative openly reusable scores** for the first end-to-end demonstration; expand to 5–10 if comparison needs more variation. Prefer one clean printed example, a second contrasting work, and optionally a more challenging print or manuscript. If actual collection examples are not yet authorized, use public-domain or appropriately licensed samples and label them as proxies.

The demonstration should show:

1. Original page(s), bibliographic context, and usage rights.
2. OMR conversion to MusicXML, plus a rendered recognized excerpt or explicit recognition limitations.
3. A readable table of extracted/computed musical characteristics.
4. Simple charts (for example pitch-class or note-duration distributions).
5. A small comparison across works, with transparent feature definitions.
6. Optional, explicitly experimental LLM-generated interpretation grounded in measured evidence.
7. A static HTML report accessible to a musicologist without Python or model credentials, supported by a reproducible notebook or script.

A meaningful negative result is acceptable: if OMR fails on a manuscript, show the failure honestly and demonstrate analysis on a valid pre-existing MusicXML score rather than silently substituting data.

## Questions for prospective collaborators

1. How many of the approximately 17,000 scores are digitized? Which file formats and scan qualities are available?
2. What proportion is printed versus handwritten? Which notation systems, genres, dates, languages, and instrumentations occur?
3. What catalog fields already exist, and how consistent are they?
4. What are **three concrete searches or comparisons** that musicologists wish they could perform today?
5. Are there a few representative scores that may legally be used in a public proof of concept?
6. Are any scores associated with performances in Avalon/MCO or other collections?
7. Who could review musical correctness and practical discovery value?
8. What rights, access restrictions, and institutional processes would govern broader experiments?

## Preliminary direction and boundaries

**Recommended now:** a standalone personal GitHub proof of concept using WSL/Python, OMR (Audiveris or homr), music21, and an easily viewed HTML report. Start with a working symbolic-analysis path, add OMR, then optional LLM interpretation. Favor open tools and small public samples. Keep setup and documentation lightweight.

**Not yet proposed:** an IU-sponsored project, an AMPAV repository, a production metadata schema, an automated 17K-score pipeline, a public web service, a trained domain model, or score-audio alignment implementation.

## Primary sources and follow-up reading

Sources checked 8 October 2026. Capabilities and installation instructions can change; verify them before implementation.

- Audiveris: https://github.com/Audiveris/audiveris
- homr: https://github.com/liebharc/homr
- Sheet Music Transformer: https://github.com/antoniorv6/SMT
- music21: https://music21.org/music21docs/about/what.html
- Partitura: https://partitura.readthedocs.io/en/latest/index.html
- MusicXML: https://www.musicxml.com/
- Music Encoding Initiative: https://music-encoding.org/
- MusicBERT: https://github.com/microsoft/muzic/blob/main/musicbert/README.md
- Sync Toolbox: https://github.com/groupmm/synctoolbox
- Avalon: https://avalon.samvera.org/

**Evidence status:** tool descriptions above are drawn from project documentation; the workflow, candidate analyses, potential user benefits, and architecture are exploratory proposals. No scores from the prospective collection have yet been inspected, and no model accuracy or musical-analysis quality has yet been measured for this use case.
