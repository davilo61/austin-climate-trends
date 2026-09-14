import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from outputs.hot_days_per_year import count_hot_days


def test_counts_100_degree_days_and_excludes_partial_years():
    weather = pd.DataFrame(
        {
            "time": pd.to_datetime(
                ["1986-06-01", "1986-06-02", "2025-07-01", "2026-07-01"]
            ),
            "tmax": [37.78, 37.7, 40.0, 45.0],
        }
    )

    result = count_hot_days(weather, end_year=2025)

    assert result.to_dict("records") == [
        {"year": 1986, "hot_days": 1, "is_partial": False},
        {"year": 2025, "hot_days": 1, "is_partial": False},
    ]


def test_includes_current_year_marked_as_partial():
    weather = pd.DataFrame(
        {
            "time": pd.to_datetime(["2025-07-01", "2026-07-01"]),
            "tmax": [40.0, 45.0],
        }
    )

    result = count_hot_days(weather, end_year=2026)

    assert result.to_dict("records") == [
        {"year": 2025, "hot_days": 1, "is_partial": False},
        {"year": 2026, "hot_days": 1, "is_partial": True},
    ]
