# Climate Trend Visualizer

A small, reproducible climate analysis project built around historical weather observations for Austin, Texas.

## Contents

- `data/historical_weather_austin_sample.csv`: Multi-decade annual Austin, Texas station observations.
- `data/austin_daily_weather.csv`: Daily Austin observations retrieved from Meteostat station 72254.
- `notebooks/climate_analysis.ipynb`: Narrative analysis with pandas, matplotlib, and seaborn.
- `outputs/temperature_anomalies.png`: Exported temperature anomaly chart.
- `outputs/precipitation_anomalies.png`: Exported Austin precipitation anomaly chart.
- `outputs/retrieve_austin_data.py`: Script used to retrieve and save daily Austin data.
- `outputs/tmin_anomalies.png`: Annual nighttime low temperature anomaly chart.
- `outputs/tmin_nh_summer_anomalies.png`: Astronomical summer nighttime low anomaly chart.

## Run the analysis

1. Create and activate a Python environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Open `notebooks/climate_analysis.ipynb` in VS Code or Jupyter.
4. Run all cells. The temperature and precipitation charts are exported to the `outputs/` directory.

The sample Austin values are illustrative and intended for demonstration, not as an official climate record. Use a trusted station dataset when producing research results.

To refresh the daily Austin dataset, run `python outputs/retrieve_austin_data.py`. The script uses Meteostat station `72254` (Austin Camp Mabry) and retrieves records through the current date.

## Sample outputs

### Annual temperature anomalies

![Austin annual temperature anomalies](outputs/temperature_anomalies.png)

### Precipitation anomalies

![Austin precipitation anomalies](outputs/precipitation_anomalies.png)

### Summer nighttime low anomalies

![Austin summer nighttime low anomalies](outputs/tmin_nh_summer_anomalies.png)
