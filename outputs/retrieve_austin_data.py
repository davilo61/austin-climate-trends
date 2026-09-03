from datetime import date
from pathlib import Path

import pandas as pd
from meteostat import daily

# Austin Camp Mabry station
station_id = '72254'

# Retrieve the last 40 years through today.
start = date(1986, 1, 1)
end = date.today()

chunks = []
chunk_start = start
while chunk_start <= end:
	chunk_end = min(date(chunk_start.year + 4, 12, 31), end)
	chunk = daily(station_id, chunk_start, chunk_end).fetch()
	if not chunk.empty:
		chunks.append(chunk)
	chunk_start = date(chunk_end.year + 1, 1, 1)

if not chunks:
	raise RuntimeError(f'No daily weather data returned for station {station_id}.')

weather = pd.concat(chunks).reset_index()
output_path = Path(__file__).resolve().parents[1] / 'data' / 'austin_daily_weather.csv'
weather.to_csv(output_path, index=False)

print(weather.head())
print(f'Saved {len(weather):,} daily records to {output_path}')