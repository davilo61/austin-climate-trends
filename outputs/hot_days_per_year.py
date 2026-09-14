from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


THRESHOLD_C = (100 - 32) / 1.8
START_YEAR = 1986


def last_complete_year(today: date | None = None) -> int:
    """Return the most recently finished calendar year relative to today."""
    return (today or date.today()).year - 1


def count_hot_days(weather: pd.DataFrame, end_year: int | None = None) -> pd.DataFrame:
    """Count days with a daily maximum temperature of at least 100 F, including the current partial year."""
    if end_year is None:
        end_year = date.today().year
    data = weather.copy()
    data["time"] = pd.to_datetime(data["time"], errors="coerce")
    data = data.dropna(subset=["time", "tmax"])
    data["year"] = data["time"].dt.year
    data = data[data["year"].between(START_YEAR, end_year)]
    data["is_hot_day"] = data["tmax"] >= THRESHOLD_C

    result = (
        data.groupby("year", as_index=False)
        .agg(hot_days=("is_hot_day", "sum"))
        .astype({"year": int, "hot_days": int})
    )
    result["is_partial"] = result["year"] > last_complete_year()
    return result


def create_chart(yearly_hot_days: pd.DataFrame, output_path: Path, end_year: int | None = None) -> None:
    if end_year is None:
        end_year = int(yearly_hot_days["year"].max())
    sns.set_theme(style="whitegrid", context="notebook")
    fig, ax = plt.subplots(figsize=(11, 5.5))
    is_partial = yearly_hot_days.get("is_partial", pd.Series(False, index=yearly_hot_days.index))
    colors = ["#d66b4d" if value > 0 else "#2f6f95" for value in yearly_hot_days["hot_days"]]
    hatches = ["///" if partial else None for partial in is_partial]
    for year, value, color, hatch in zip(yearly_hot_days["year"], yearly_hot_days["hot_days"], colors, hatches):
        ax.bar(year, value, color=color, width=0.8, alpha=0.6 if hatch else 0.85, hatch=hatch, edgecolor="#172a3a" if hatch else None)
    # Exclude the partial year so it doesn't skew the rolling mean toward an artificially low value.
    complete = yearly_hot_days[~is_partial]
    rolling_mean = complete["hot_days"].rolling(7, center=True).mean()
    ax.plot(
        complete["year"],
        rolling_mean,
        color="#172a3a",
        linewidth=2.5,
        label="7-year rolling mean",
    )
    if is_partial.any():
        ax.bar(0, 0, color="#999999", alpha=0.6, hatch="///", edgecolor="#172a3a", label="current year (partial, year-to-date)")
    ax.set(
        title="Austin annual number of 100°F days",
        xlabel="Year",
        ylabel="Days with daily maximum temperature >= 100°F",
    )
    ax.set_xlim(START_YEAR - 1, end_year + 1)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "austin_daily_weather.csv"
    output_path = project_root / "outputs" / "hot_days_per_year.png"
    yearly_hot_days = count_hot_days(pd.read_csv(data_path))
    create_chart(yearly_hot_days, output_path)
    print(yearly_hot_days.to_string(index=False))
    print(f"Saved chart to {output_path}")
