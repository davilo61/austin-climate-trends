import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.image
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from outputs.instagram_export import finish_slide, new_slide, short_date, trend_phrase


def test_slide_is_instagram_portrait_size(tmp_path):
    fig, ax = new_slide("Title", "Headline\nsecond line")
    ax.plot([1, 2], [1, 2])
    output_path = tmp_path / "slide.png"
    finish_slide(fig, "Footnote", output_path)

    height, width = matplotlib.image.imread(output_path).shape[:2]
    assert (width, height) == (1080, 1350)


def test_text_helpers():
    assert short_date(pd.Timestamp("2026-10-04")) == "Oct 4"
    assert trend_phrase(0.46) == "warming about 0.5°F per decade"
    assert trend_phrase(-0.2) == "cooling about 0.2°F per decade"
