from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


THRESHOLD_C = (100 - 32) / 1.8
START_YEAR = 1986
END_YEAR = 2025


def count_hot_days(weather: pd.DataFrame) -> pd.DataFrame:
    """Count complete-year days with a daily maximum temperature of at least 100 F."""
    data = weather.copy()
    data["time"] = pd.to_datetime(data["time"], errors="coerce")
    data = data.dropna(subset=["time", "tmax"])
    data["year"] = data["time"].dt.year
    data = data[data["year"].between(START_YEAR, END_YEAR)]
    data["is_hot_day"] = data["tmax"] >= THRESHOLD_C

    return (
        data.groupby("year", as_index=False)
        .agg(hot_days=("is_hot_day", "sum"))
        .astype({"year": int, "hot_days": int})
    )


def create_chart(yearly_hot_days: pd.DataFrame, output_path: Path) -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    fig, ax = plt.subplots(figsize=(11, 5.5))
    colors = ["#d66b4d" if value > 0 else "#2f6f95" for value in yearly_hot_days["hot_days"]]
    ax.bar(yearly_hot_days["year"], yearly_hot_days["hot_days"], color=colors, width=0.8, alpha=0.85)
    rolling_mean = yearly_hot_days["hot_days"].rolling(7, center=True).mean()
    ax.plot(
        yearly_hot_days["year"],
        rolling_mean,
        color="#172a3a",
        linewidth=2.5,
        label="7-year rolling mean",
    )
    ax.set(
        title="Austin annual number of 100°F days",
        xlabel="Year",
        ylabel="Days with daily maximum temperature >= 100°F",
    )
    ax.set_xlim(START_YEAR - 1, END_YEAR + 1)
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
