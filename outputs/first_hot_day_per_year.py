from datetime import date
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


THRESHOLD_C = (100 - 32) / 1.8
START_YEAR = 1986
# Leap reference year so every calendar date (including Feb 29) maps onto one shared y-axis.
REFERENCE_YEAR = 2000


def find_first_hot_days(weather: pd.DataFrame, end_year: int | None = None) -> pd.DataFrame:
    """Return the first date each year with a daily maximum temperature of at least 100 F.

    Years without a 100 F day have a missing first_date. The current year is flagged as
    partial only while its first 100 F day has not happened yet; once it has, the date is final.
    """
    if end_year is None:
        end_year = date.today().year
    data = weather.copy()
    data["time"] = pd.to_datetime(data["time"], errors="coerce")
    data = data.dropna(subset=["time", "tmax"])
    data["year"] = data["time"].dt.year
    data = data[data["year"].between(START_YEAR, end_year)]

    first_dates = (
        data[data["tmax"] >= THRESHOLD_C].groupby("year")["time"].min().rename("first_date").reset_index()
    )
    # Left join keeps years without a 100 F day, and the column stays datetime-typed even if none qualify.
    result = pd.DataFrame({"year": sorted(data["year"].unique())}).astype({"year": int})
    result = result.merge(first_dates, on="year", how="left")
    result["day_of_year"] = result["first_date"].dt.dayofyear.astype("Int64")
    result["is_partial"] = (result["year"] >= date.today().year) & result["first_date"].isna()
    return result


def _as_reference_date(first_date: pd.Timestamp) -> pd.Timestamp:
    return first_date.replace(year=REFERENCE_YEAR)


def create_chart(first_hot_days: pd.DataFrame, output_path: Path, end_year: int | None = None) -> None:
    if end_year is None:
        end_year = int(first_hot_days["year"].max())
    sns.set_theme(style="whitegrid", context="notebook")
    fig, ax = plt.subplots(figsize=(11, 5.5))

    observed = first_hot_days.dropna(subset=["first_date"])
    reference_dates = observed["first_date"].map(_as_reference_date)
    ax.scatter(observed["year"], reference_dates, color="#d66b4d", s=55, zorder=3, label="First 100°F day")

    # Linear trend over years that reached 100 F; years without one can't contribute a date.
    if len(observed) >= 2:
        reference_numbers = mdates.date2num(reference_dates)
        slope, intercept = np.polyfit(observed["year"], reference_numbers, 1)
        trend_years = np.array([observed["year"].min(), observed["year"].max()])
        ax.plot(
            trend_years,
            mdates.num2date(slope * trend_years + intercept),
            color="#172a3a",
            linewidth=2.5,
            label=f"Linear trend ({slope * 10:+.1f} days/decade)",
        )

    # Years with no 100 F day sit in a band along the top of the chart.
    top = pd.Timestamp(REFERENCE_YEAR, 10, 15)
    no_hot_day = first_hot_days[first_hot_days["first_date"].isna() & ~first_hot_days["is_partial"]]
    ax.scatter(no_hot_day["year"], [top] * len(no_hot_day), marker="x", color="#2f6f95", s=45, zorder=3, label="No 100°F day that year")
    pending = first_hot_days[first_hot_days["is_partial"]]
    if not pending.empty:
        ax.scatter(pending["year"], [top] * len(pending), marker="o", facecolors="none", edgecolors="#172a3a", s=55, zorder=3, label="Current year, none yet")

    ax.yaxis.set_major_locator(mdates.MonthLocator())
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_ylim(pd.Timestamp(REFERENCE_YEAR, 4, 1), pd.Timestamp(REFERENCE_YEAR, 11, 15))
    ax.set(
        title="Austin first 100°F day of each year",
        xlabel="Year",
        ylabel="Date of first daily maximum >= 100°F",
    )
    ax.set_xlim(START_YEAR - 1, end_year + 1)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "austin_daily_weather.csv"
    output_path = project_root / "outputs" / "first_hot_day_per_year.png"
    first_hot_days = find_first_hot_days(pd.read_csv(data_path))
    create_chart(first_hot_days, output_path)
    print(first_hot_days.to_string(index=False))
    print(f"Saved chart to {output_path}")
