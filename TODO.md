# Project TODO

A checklist for keeping the Austin climate analysis project reproducible, polished, and publication-ready.

## Immediate priorities

- [x] Define the project scope around Austin weather observations and climate trend analysis.
- [x] Write the project overview and setup instructions in `README.md`.
- [x] Add sample output charts to the repository and document their purpose.
- [x] Add a Python environment ignore configuration for local tooling and caches.
- [x] Review the repository and create an initial commit.
- [x] Create a public GitHub repository and push the project.
- [x] Verify that the project installs cleanly from a fresh environment using `requirements.txt`.
- [x] Confirm that the notebooks run end-to-end without manual fixes.
- [x] Document the exact data source, retrieval date, and station metadata in a single place.
- [x] Keep `data/historical_weather_austin_sample.csv` as a legacy/reference file and document that it is not the active analysis dataset.

## Data quality and reproducibility

- [x] Add a validation step for missing dates, duplicated rows, and missing `tmin`/temperature values.
- [x] Document the analysis baseline and how anomaly values are calculated.
- [x] Add a script or clear notebook instructions for re-generating all output charts.
- [x] Record the date of the most recent data refresh and when it was last reviewed.
- [x] Add a note that results are descriptive and based on a single weather station, not a full regional assessment.
- [x] Consider a small statistical add-on such as confidence intervals or a trend test.
- [x] Add an annual chart counting days with daily maximum temperatures of at least 100°F for the 40 complete years from 1986 through 2025.

## Project polish

- [x] Add a `LICENSE` and contributor guidance if the repo is meant for wider sharing.
- [x] Add a short project status section with the current analysis scope and known limitations.
- [x] Include a screenshot or summary of the notebook outputs in the main documentation.
- [x] Make sure file names and chart outputs match the README references exactly.

## Future public-facing features

- [x] Choose a lightweight web stack for a simple Austin climate landing page: static GitHub Pages site with HTML, CSS, and vanilla JavaScript.
- [x] Choose a lightweight web stack for a simple Austin climate landing page: static GitHub Pages site with HTML, CSS, and vanilla JavaScript.
- [x] Build a summary page with annual temperature anomaly findings.
- [x] Add annual nighttime low and summer nighttime low trend charts.
- [x] Add precipitation anomaly visuals and explanatory text.
- [x] Add unit toggles for Celsius/Fahrenheit if the site is user-facing.
- [x] Add source notes, baseline dates, station information, and data coverage details.
- [ ] Prepare exportable PNG charts and CSV summaries for reuse in posts or presentations.
- [ ] Design a social-media-friendly chart template for Austin climate summaries.

## Recommended order

1. Verify the repository works from a fresh Python environment.
2. Clean up data validation and chart regeneration steps.
3. Publish the repo to GitHub and confirm the docs still match the outputs.
4. Build the simple website from the existing analysis outputs.
5. Reuse the same charts for social-media assets once the manual workflow is stable.
