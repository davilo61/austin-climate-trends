"""Refresh the Austin dataset, then regenerate every chart and sync the docs site assets.

Run from anywhere: python outputs/refresh_all.py
"""
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "climate_analysis.ipynb"
DOCS_ASSETS_DIR = PROJECT_ROOT / "docs" / "assets"


def retrieve_data() -> None:
    # Run as a subprocess so a failed download stops the pipeline before any chart is rebuilt.
    subprocess.run([sys.executable, str(OUTPUTS_DIR / "retrieve_austin_data.py")], check=True)


def run_notebook() -> None:
    # Execute in memory so the notebook file itself is not rewritten with new cell outputs.
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    NotebookClient(
        notebook,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": str(NOTEBOOK_PATH.parent)}},
    ).execute()


def run_hot_days() -> None:
    runpy.run_path(str(OUTPUTS_DIR / "hot_days_per_year.py"), run_name="__main__")


def sync_docs_assets() -> None:
    for chart in sorted(DOCS_ASSETS_DIR.glob("*.png")):
        source = OUTPUTS_DIR / chart.name
        if source.exists():
            shutil.copy2(source, chart)
            print(f"Synced {chart.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    print("1/4 Retrieving latest Austin weather data", flush=True)
    retrieve_data()
    print("2/4 Running climate_analysis notebook", flush=True)
    run_notebook()
    print("3/4 Regenerating 100°F days chart", flush=True)
    run_hot_days()
    print("4/4 Syncing charts into docs/assets", flush=True)
    sync_docs_assets()
