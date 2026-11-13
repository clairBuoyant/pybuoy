# Test fixtures

Trimmed copies of real NOAA/NDBC responses, captured 2026-11-11.

| File | Source | Trimmed to |
| --- | --- | --- |
| `44065.txt` | `https://www.ndbc.noaa.gov/data/realtime2/44065.txt` | both header rows and the first 3 observations |
| `44065.spec` | `https://www.ndbc.noaa.gov/data/realtime2/44065.spec` | both header rows and 3 observations chosen to cover `N/A` and `MM` values |
| `activestations.xml` | `https://www.ndbc.noaa.gov/activestations.xml` | 4 stations: a buoy, a TAO mooring without sensor flags, a DART station without `elev`, and a station with every flag set |
| `ndfd_forecast.xml` | NDFD `ndfdXMLclient.php`, `product=time-series`, `Unit=e`, lat 40.368, lon -73.701 | the first 4 wind timestamps and the first 3 wave timestamps (the two use different time layouts) |

The only edits are the row/element removals above and the `count` attribute in
`activestations.xml`.
