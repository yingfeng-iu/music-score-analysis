"""Extract a deliberately small set of explainable features from MusicXML."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from music21 import chord, converter, interval, meter, note

PITCH_CLASSES = ("C", "C#/D♭", "D", "D#/E♭", "E", "F", "F#/G♭", "G", "G#/A♭", "A", "A#/B♭", "B")


def _metadata_text(value: Any, fallback: str = "Unknown") -> str:
    """Return a printable metadata value while labeling absent data honestly."""
    if value is None or not str(value).strip():
        return fallback
    return str(value).strip()


def analyze_score(path: str | Path) -> dict[str, Any]:
    """Parse one MusicXML file and return JSON-serializable written-pitch features.

    Pitches remain as notated. This is important for future transposing parts:
    callers must not interpret these values as concert pitch without conversion.
    """
    source = Path(path)
    score = converter.parse(source)
    metadata = score.metadata
    pitched_notes = list(score.recurse().getElementsByClass(note.Note))
    all_chords = list(score.recurse().getElementsByClass(chord.Chord))
    pitch_values = [item.pitch for item in pitched_notes]
    pitch_class_counts = Counter(item.pitch.pitchClass for item in pitched_notes)
    duration_counts = Counter(str(item.duration.quarterLength) for item in pitched_notes)

    signatures = []
    for signature in score.recurse().getElementsByClass(meter.TimeSignature):
        if signature.ratioString not in signatures:
            signatures.append(signature.ratioString)

    key_signatures = []
    for signature in score.recurse().getElementsByClass("KeySignature"):
        if signature.sharps == 0:
            label = "No sharps or flats"
        elif signature.sharps > 0:
            label = f"{signature.sharps} sharp{'s' if signature.sharps != 1 else ''}"
        else:
            flats = abs(signature.sharps)
            label = f"{flats} flat{'s' if flats != 1 else ''}"
        if label not in key_signatures:
            key_signatures.append(label)

    part_summaries = []
    melodic_intervals: Counter[str] = Counter()
    for index, part in enumerate(score.parts, start=1):
        label = _metadata_text(part.partName, f"Part {index}")
        part_notes = list(part.recurse().getElementsByClass(note.Note))
        part_chords = list(part.recurse().getElementsByClass(chord.Chord))
        is_monophonic = not part_chords and not list(part.recurse().getElementsByClass("Voice"))
        part_summaries.append(
            {"label": label, "note_count": len(part_notes), "monophonic": is_monophonic}
        )
        if is_monophonic:
            for first, second in zip(part_notes, part_notes[1:]):
                distance = interval.Interval(first, second)
                melodic_intervals[distance.directedSimpleName] += 1

    estimate = score.analyze("key") if pitched_notes else None
    measure_count = max(
        (len(part.getElementsByClass("Measure")) for part in score.parts),
        default=0,
    )

    return {
        "id": source.stem,
        "source_file": source.name,
        "title": _metadata_text(metadata.title if metadata else None),
        "composer": _metadata_text(metadata.composer if metadata else None),
        "parts": part_summaries,
        "measure_count": measure_count,
        "time_signatures": signatures or ["Not encoded"],
        "key_signatures": key_signatures or ["Not encoded"],
        "note_count": len(pitched_notes),
        "chord_count": len(all_chords),
        "written_pitch_range": (
            {"lowest": min(pitch_values).nameWithOctave, "highest": max(pitch_values).nameWithOctave}
            if pitch_values
            else None
        ),
        "pitch_class_counts": {
            PITCH_CLASSES[index]: pitch_class_counts.get(index, 0) for index in range(12)
        },
        "duration_counts_quarter_notes": dict(
            sorted(duration_counts.items(), key=lambda item: float(item[0]))
        ),
        "melodic_interval_counts": dict(sorted(melodic_intervals.items())),
        "estimated_key": (
            {"name": str(estimate), "correlation": round(float(estimate.correlationCoefficient), 3)}
            if estimate is not None
            else None
        ),
        "preview_pitches": [item.pitch.nameWithOctave for item in pitched_notes[:16]],
        "method_notes": [
            "Counts and pitch range use written pitches, not concert-pitch conversion.",
            "Melodic intervals are computed only for parts without encoded chords or voices.",
            "Estimated key is music21's algorithmic estimate, not an encoded fact.",
        ],
    }


def compare_scores(analyses: list[dict[str, Any]]) -> dict[str, Any]:
    """Create normalized, directly explainable cross-score comparisons."""
    rows = []
    for result in analyses:
        total = result["note_count"] or 1
        durations = result["duration_counts_quarter_notes"]
        short_notes = sum(count for value, count in durations.items() if float(value) < 1.0)
        rows.append(
            {
                "id": result["id"],
                "title": result["title"],
                "note_count": result["note_count"],
                "short_note_proportion": round(short_notes / total, 3),
                "distinct_pitch_classes": sum(
                    1 for count in result["pitch_class_counts"].values() if count
                ),
            }
        )

    observations = []
    if rows:
        fastest = max(rows, key=lambda row: row["short_note_proportion"])
        slowest = min(rows, key=lambda row: row["short_note_proportion"])
        observations.append(
            f"{fastest['title']} has {fastest['short_note_proportion']:.0%} notes shorter than a quarter note, "
            f"compared with {slowest['short_note_proportion']:.0%} in {slowest['title']}."
        )
        widest = max(rows, key=lambda row: row["distinct_pitch_classes"])
        observations.append(
            f"{widest['title']} uses the most distinct written pitch classes in this sample "
            f"({widest['distinct_pitch_classes']})."
        )
    return {"rows": rows, "observations": observations}
