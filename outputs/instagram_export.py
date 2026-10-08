"""Export Instagram-ready 4:5 (1080x1350) chart slides plus a suggested caption.

Run: python outputs/instagram_export.py
Writes outputs/social/01_*.png ... and outputs/social/caption.txt.
"""
import sys
from datetime import date
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from outputs.first_hot_day_per_year import REFERENCE_YEAR, find_first_hot_days
from outputs.hot_days_per_year import count_hot_days


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "austin_daily_weather.csv"
SOCIAL_DIR = PROJECT_ROOT / "outputs" / "social"

# 6 x 7.5 inches at 180 dpi = 1080 x 1350 px, Instagram's 4:5 portrait size.
FIGSIZE = (6, 7.5)
DPI = 180
BASELINE_YEARS = (1985, 2014)

BACKGROUND = "#faf7f2"
INK = "#172a3a"
MUTED = "#5b6670"
HOT = "#d66b4d"
COOL = "#2f6f95"


def load_daily_weather() -> pd.DataFrame:
    weather = pd.read_csv(DATA_PATH, parse_dates=["time"])
    weather["year"] = weather["time"].dt.year
    weather["temp"] = weather["temp"].fillna((weather["tmin"] + weather["tmax"]) / 2)
    return weather


def annual_anomalies_f(daily: pd.DataFrame) -> pd.DataFrame:
    """Annual mean and nighttime-low anomalies in F against the 1985-2014 baseline, complete years only."""
    last_complete_year = date.today().year - 1
    yearly = (
        daily[daily["year"] <= last_complete_year]
        .groupby("year", as_index=False)
        .agg(mean_temp_c=("temp", "mean"), mean_tmin_c=("tmin", "mean"))
    )
    in_baseline = yearly["year"].between(*BASELINE_YEARS)
    for column, name in (("mean_temp_c", "temp_anomaly_f"), ("mean_tmin_c", "tmin_anomaly_f")):
        values_f = yearly[column] * 1.8 + 32
        yearly[name] = values_f - values_f[in_baseline].mean()
    return yearly


def short_date(value) -> str:
    """Format like "Oct 6" on every platform (strftime's %-d is not available on Windows)."""
    return f"{value:%b} {value.day}"


def linear_slope_per_decade(x: pd.Series, y: pd.Series) -> float:
    return float(np.polyfit(x, y, 1)[0] * 10)


def new_slide(title: str, headline: str):
    """Create a 4:5 slide with title and headline text, returning the figure and chart axes."""
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=BACKGROUND)
    fig.text(0.07, 0.94, "AUSTIN, TX · CAMP MABRY", fontsize=9, color=MUTED, fontweight="bold", va="top")
    fig.text(0.07, 0.905, title, fontsize=19, color=INK, fontweight="bold", va="top", wrap=True)
    fig.text(0.07, 0.835, headline, fontsize=13, color=HOT, fontweight="bold", va="top", linespacing=1.3)
    ax = fig.add_axes([0.14, 0.19, 0.80, 0.56], facecolor=BACKGROUND)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=INK, labelsize=10)
    ax.grid(axis="y", color="#e2ddd5", linewidth=0.8)
    ax.set_axisbelow(True)
    return fig, ax


def finish_slide(fig, footnote: str, output_path: Path) -> None:
    fig.text(0.07, 0.115, footnote, fontsize=8, color=MUTED, va="top", linespacing=1.4)
    fig.text(0.07, 0.025, "Data: Meteostat station 72254 · Chart: austin-climate-trends", fontsize=8, color=MUTED)
    # No bbox_inches="tight": it would change the pixel size away from 1080x1350.
    fig.savefig(output_path, dpi=DPI, facecolor=BACKGROUND)
    plt.close(fig)
    print(f"Saved {output_path}")


def hot_days_slide(daily: pd.DataFrame, data_through: pd.Timestamp, output_path: Path) -> dict:
    counts = count_hot_days(daily)
    complete = counts[~counts["is_partial"]]
    record = complete.loc[complete["hot_days"].idxmax()]
    first_decade = complete[complete["year"] < complete["year"].min() + 10]["hot_days"].mean()
    last_decade = complete[complete["year"] > complete["year"].max() - 10]["hot_days"].mean()
    current = counts[counts["is_partial"]]

    headline = f"About {last_decade:.0f} days a year now,\nup from {first_decade:.0f} in the first decade"
    fig, ax = new_slide("Days reaching 100°F", headline)
    ax.bar(complete["year"], complete["hot_days"], color=HOT, width=0.75)
    if not current.empty:
        ax.bar(current["year"], current["hot_days"], color=HOT, alpha=0.45, hatch="///", edgecolor=INK, width=0.75)
    ax.annotate(
        f"{int(record['year'])}: {int(record['hot_days'])} days",
        (record["year"], record["hot_days"]),
        xytext=(-8, 4), textcoords="offset points", ha="right", fontsize=10, color=INK,
    )
    ax.set_ylabel("Days per year", color=INK, fontsize=11)
    footnote = f"Days with a high of at least 100°F, {int(counts['year'].min())}–{data_through.year}."
    if not current.empty:
        footnote += f"\nHatched bar: {data_through.year} so far ({int(current['hot_days'].iloc[0])} days through {short_date(data_through)})."
    finish_slide(fig, footnote, output_path)
    return {"last_decade": last_decade, "first_decade": first_decade, "record_year": int(record["year"]), "record_days": int(record["hot_days"])}


def first_hot_day_slide(daily: pd.DataFrame, output_path: Path) -> dict:
    first_days = find_first_hot_days(daily)
    observed = first_days.dropna(subset=["first_date"])
    reference_dates = observed["first_date"].map(lambda d: d.replace(year=REFERENCE_YEAR))
    reference_numbers = mdates.date2num(reference_dates)
    slope, intercept = np.polyfit(observed["year"], reference_numbers, 1)
    days_earlier = -slope * 10

    headline = f"Arriving ~{days_earlier:.0f} days earlier\nper decade since {int(first_days['year'].min())}"
    fig, ax = new_slide("First 100°F day of the year", headline)
    ax.scatter(observed["year"], reference_dates, color=HOT, s=28, zorder=3)
    trend_years = np.array([observed["year"].min(), observed["year"].max()])
    trend_dates = mdates.num2date(slope * trend_years + intercept)
    ax.plot(trend_years, trend_dates, color=INK, linewidth=2.5)
    for year, trend_date, align in zip(trend_years, trend_dates, ("left", "right")):
        ax.annotate(short_date(trend_date), (year, trend_date), xytext=(0, 8), textcoords="offset points", ha=align, fontsize=10, color=INK, fontweight="bold")
    ax.yaxis.set_major_locator(mdates.MonthLocator())
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_ylim(pd.Timestamp(REFERENCE_YEAR, 4, 15), pd.Timestamp(REFERENCE_YEAR, 9, 30))
    missing = first_days[first_days["first_date"].isna() & ~first_days["is_partial"]]["year"].tolist()
    footnote = "Each dot is the first day that year with a high of at least 100°F; line is the linear trend."
    if missing:
        footnote += f"\nNo 100°F day in {', '.join(str(y) for y in missing)} (not plotted)."
    finish_slide(fig, footnote, output_path)
    return {"days_earlier_per_decade": days_earlier}


def anomaly_slide(yearly: pd.DataFrame, column: str, title: str, subject: str, output_path: Path) -> dict:
    slope = linear_slope_per_decade(yearly["year"], yearly[column])
    first_year, last_year = int(yearly["year"].min()), int(yearly["year"].max())
    direction = "up" if slope >= 0 else "down"
    total_change = abs(slope) * (last_year - first_year) / 10
    headline = f"{subject} {direction} {abs(slope):.1f}°F per decade\n(about {total_change:.1f}°F since {first_year})"
    fig, ax = new_slide(title, headline)
    colors = [COOL if value < 0 else HOT for value in yearly[column]]
    ax.bar(yearly["year"], yearly[column], color=colors, width=0.75)
    ax.plot(yearly["year"], yearly[column].rolling(7, center=True).mean(), color=INK, linewidth=2.5)
    ax.axhline(0, color=INK, linewidth=1)
    ax.set_ylabel("°F vs. 1985–2014 average", color=INK, fontsize=11)
    footnote = f"Bars: each year compared with the 1985–2014 average, {first_year}–{last_year}.\nLine: 7-year rolling mean. Red = warmer, blue = cooler."
    finish_slide(fig, footnote, output_path)
    return {"slope_per_decade": slope}


def trend_phrase(slope_per_decade: float) -> str:
    direction = "warming" if slope_per_decade >= 0 else "cooling"
    return f"{direction} about {abs(slope_per_decade):.1f}°F per decade"


def write_caption(stats: dict, data_through: pd.Timestamp, output_path: Path) -> None:
    hot, first, tmin, temp = stats["hot_days"], stats["first_hot_day"], stats["tmin"], stats["temp"]
    caption = (
        f"Austin is heating up. 🌡️ Four charts from {data_through.year - 1986 + 1} years of daily weather at Camp Mabry:\n\n"
        f"1️⃣ 100°F days: about {hot['last_decade']:.0f} a year over the last decade, up from {hot['first_decade']:.0f} in the first. "
        f"Record: {hot['record_days']} in {hot['record_year']}.\n"
        f"2️⃣ The first 100°F day is arriving about {first['days_earlier_per_decade']:.0f} days earlier per decade.\n"
        f"3️⃣ Nighttime lows are {trend_phrase(tmin['slope_per_decade'])}.\n"
        f"4️⃣ The average annual temperature is {trend_phrase(temp['slope_per_decade'])}.\n\n"
        f"Data: Meteostat station 72254 (Austin Camp Mabry), through {data_through:%B} {data_through.day}, {data_through.year}.\n\n"
        "#Austin #ATX #AustinTexas #ClimateChange #Heat #Weather #DataViz #ClimateData #Texas"
    )
    output_path.write_text(caption + "\n", encoding="utf-8")
    print(f"Saved {output_path.relative_to(PROJECT_ROOT)}")


def main() -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    SOCIAL_DIR.mkdir(parents=True, exist_ok=True)
    daily = load_daily_weather()
    data_through = daily.dropna(subset=["tmax"])["time"].max()
    yearly = annual_anomalies_f(daily)

    stats = {
        "hot_days": hot_days_slide(daily, data_through, SOCIAL_DIR / "01_hot_days.png"),
        "first_hot_day": first_hot_day_slide(daily, SOCIAL_DIR / "02_first_hot_day.png"),
        "tmin": anomaly_slide(yearly, "tmin_anomaly_f", "Warmer nights", "Nighttime lows", SOCIAL_DIR / "03_nighttime_lows.png"),
        "temp": anomaly_slide(yearly, "temp_anomaly_f", "Annual temperature", "Average temperature", SOCIAL_DIR / "04_annual_temperature.png"),
    }
    write_caption(stats, data_through, SOCIAL_DIR / "caption.txt")


if __name__ == "__main__":
    main()
