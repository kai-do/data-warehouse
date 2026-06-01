# Bronze Table Design

The bronze layer stores the raw Open-Meteo response with just enough metadata to trace where it came from and when it was fetched.

## Design goals

- Keep the API payload intact so it can be reprocessed later.
- Store one row per fetched response.
- Make it easy to filter by location and request time.
- Avoid business logic in bronze; transformations belong in silver.

## Table shape

The first bronze table is `bronze.weather_api_raw`.

It stores:

- `source_system`: the upstream system name, currently `open_meteo`
- `endpoint`: the API endpoint used
- `request_params`: the exact request parameters sent
- `latitude` and `longitude`: the location requested
- `requested_at`: when the request was made
- `response_received_at`: when the response came back
- `http_status`: the response status code
- `response_metadata`: small response-level metadata
- `payload_json`: the full JSON response body
- `payload_hash`: optional fingerprint for deduplication or change tracking

## How this helps later

- Silver can expand `payload_json.hourly` into one row per hour.
- Gold can build map-ready summary tables from the cleaned data.
- Because bronze keeps the raw response, you can rebuild later layers without hitting the API again.