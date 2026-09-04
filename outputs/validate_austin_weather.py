from __future__ import annotations

from typing import List

import pandas as pd


REQUIRED_COLUMNS = ["time", "temp", "tmin", "tmax"]


def find_data_issues(df: pd.DataFrame) -> List[str]:
    """Return human-readable validation messages for common temperature dataset issues."""
    issues: List[str] = []

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        issues.append(f"Missing required columns: {', '.join(missing_columns)}")
        return issues

    df = df.copy()
    df["time"] = pd.to_datetime(df["time"], errors="coerce")

    if df["time"].isna().any():
        issues.append(f"Missing or invalid date values in {int(df['time'].isna().sum())} row(s).")

    if df["time"].duplicated().any():
        dupes = int(df["time"].duplicated().sum())
        issues.append(f"Duplicate date values detected: {dupes} row(s).")

    valid_dates = df["time"].dropna().sort_values().drop_duplicates()
    if not valid_dates.empty:
        expected_dates = pd.date_range(start=valid_dates.min(), end=valid_dates.max(), freq="D")
        missing_dates = expected_dates.difference(valid_dates)
        if len(missing_dates) > 0:
            issues.append(f"Missing dates detected in the daily time series: {len(missing_dates)} day(s) absent.")

    for field in ["temp", "tmin", "tmax"]:
        if field in df.columns:
            missing_count = int(df[field].isna().sum())
            if missing_count:
                issues.append(f"Missing values in {field}: {missing_count} row(s).")

    return issues


def validate_weather_data(df: pd.DataFrame) -> None:
    """Raise a ValueError if the dataset has issues that should be fixed before analysis."""
    issues = find_data_issues(df)
    if issues:
        raise ValueError("Weather dataset validation failed: " + "; ".join(issues))


if __name__ == "__main__":
    data = pd.read_csv("data/austin_daily_weather.csv")
    try:
        validate_weather_data(data)
        print("Austin weather dataset validation passed.")
    except ValueError as exc:
        print(exc)
        raise
