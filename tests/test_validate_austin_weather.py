import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from outputs.validate_austin_weather import find_data_issues


def test_valid_dataframe_has_no_issues():
    df = pd.DataFrame(
        {
            "time": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "temp": [10.0, 12.0, 11.5],
            "tmin": [5.0, 6.0, 7.0],
            "tmax": [15.0, 18.0, 16.0],
        }
    )

    assert find_data_issues(df) == []


def test_invalid_dataframe_flags_problems():
    df = pd.DataFrame(
        {
            "time": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-02", "2024-01-04"]),
            "temp": [10.0, None, 11.0, 12.5],
            "tmin": [5.0, 6.0, None, 7.0],
            "tmax": [15.0, 18.0, 17.0, 19.0],
        }
    )

    issues = find_data_issues(df)

    assert any("missing dates" in issue.lower() for issue in issues)
    assert any("duplicate" in issue.lower() for issue in issues)
    assert any("missing values" in issue.lower() for issue in issues)
