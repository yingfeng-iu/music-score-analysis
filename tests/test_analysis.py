from pathlib import Path

from music_score_analysis import analyze_score, compare_scores

SAMPLES = Path(__file__).parents[1] / "samples"


def test_stepwise_fixture_has_expected_features() -> None:
    result = analyze_score(SAMPLES / "stepwise-study.musicxml")

    assert result["title"] == "Stepwise Study"
    assert result["note_count"] == 8
    assert result["measure_count"] == 2
    assert result["time_signatures"] == ["4/4"]
    assert result["key_signatures"] == ["No sharps or flats"]
    assert result["written_pitch_range"] == {"lowest": "C4", "highest": "C5"}
    assert result["pitch_class_counts"]["C"] == 2


def test_comparison_uses_normalized_short_note_proportion() -> None:
    results = [
        analyze_score(SAMPLES / "stepwise-study.musicxml"),
        analyze_score(SAMPLES / "waltz-arpeggio.musicxml"),
    ]

    comparison = compare_scores(results)

    rows = {row["id"]: row for row in comparison["rows"]}
    assert rows["stepwise-study"]["short_note_proportion"] == 0
    assert rows["waltz-arpeggio"]["short_note_proportion"] == 0.667
