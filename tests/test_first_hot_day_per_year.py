import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from outputs.first_hot_day_per_year import find_first_hot_days


def test_finds_first_100_degree_day_per_year():
    weather = pd.DataFrame(
        {
            "time": pd.to_datetime(
                ["1986-06-01", "1986-06-15", "1986-07-01", "1987-07-01", "1988-05-20", "1988-08-01"]
            ),
            "tmax": [37.7, 37.78, 40.0, 36.0, 38.0, 41.0],
        }
    )

    result = find_first_hot_days(weather, end_year=1988)

    assert result["year"].tolist() == [1986, 1987, 1988]
    assert result["first_date"].tolist()[0] == pd.Timestamp("1986-06-15")
    assert pd.isna(result["first_date"].tolist()[1])
    assert result["first_date"].tolist()[2] == pd.Timestamp("1988-05-20")
    assert result["is_partial"].tolist() == [False, False, False]


def test_current_year_is_partial_only_until_first_100_degree_day():
    current_year = date.today().year
    early_in_year = pd.DataFrame({"time": pd.to_datetime([f"{current_year}-01-15"]), "tmax": [20.0]})
    after_hot_day = pd.DataFrame({"time": pd.to_datetime([f"{current_year}-01-15"]), "tmax": [38.0]})

    assert find_first_hot_days(early_in_year)["is_partial"].tolist() == [True]
    assert find_first_hot_days(after_hot_day)["is_partial"].tolist() == [False]
