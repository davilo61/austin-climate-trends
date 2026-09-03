# Project TODO

A progress checklist for turning the Austin climate analysis into a public project.

## Repository and GitHub

- [x] Focus the repository on Austin weather data.
- [x] Document the Austin data files and analysis notebook in `README.md`.
- [x] Add sample output images to `README.md`.
- [x] Document the analysis baseline, units, and limitations in `README.md`.
- [x] Add a `.gitignore` for `.venv/`, notebook checkpoints, Python caches, and local environment files.
- [ ] Review the repository before the first commit.
- [ ] Create the initial Git commit.
- [ ] Create a GitHub repository and push the project.
- [ ] Add the data source and retrieval date to the project documentation.
- [ ] Confirm that generated charts and the notebook render correctly on GitHub.

## Data and analysis

- [ ] Decide whether `data/historical_weather_austin_sample.csv` is still needed alongside the daily dataset.
- [ ] Add a reproducible script or notebook instructions for regenerating every output image.
- [ ] Add checks for missing dates, missing `tmin` values, partial years, and duplicate observations.
- [ ] Document that trend results are descriptive and based on one station.
- [ ] Consider adding statistical uncertainty, confidence intervals, or a non-parametric trend test.
- [ ] Refresh the data periodically and record the update date.

## Austin climate website

- [ ] Choose a web stack and create a minimal deployable site.
- [ ] Build an overview page with the main Austin temperature findings.
- [ ] Display annual temperature anomaly trends.
- [ ] Display annual nighttime low and summer nighttime low trends.
- [ ] Display precipitation anomalies.
- [ ] Add a Fahrenheit/Celsius toggle.
- [ ] Add chart source notes, baseline dates, station information, and data coverage.
- [ ] Add downloadable PNG charts and, if useful, CSV summaries.
- [ ] Make the site responsive for desktop and mobile.
- [ ] Deploy the site using a hosting provider such as GitHub Pages.

## Instagram or social feed

- [ ] Choose a consistent post format and visual identity.
- [ ] Create square or vertical chart templates for social posts.
- [ ] Generate a monthly or weekly Austin climate summary image.
- [ ] Include the period, station, baseline, units, and source on every post.
- [ ] Write concise captions explaining the result without overstating causation.
- [ ] Decide whether posts will be published manually or through a scheduling workflow.
- [ ] Test image readability on a phone before publishing.
- [ ] Keep a content calendar for recurring topics and notable trends.

## Recommended order

1. Finish repository cleanup and create the first GitHub commit.
2. Add validation and reproducible chart-generation steps.
3. Build the website from the existing chart outputs and analysis data.
4. Reuse the website's chart-generation code for Instagram assets.
5. Automate updates only after the manual workflow is reliable.
