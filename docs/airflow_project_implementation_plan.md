# Local Weather Data Warehouse Implementation Plan

This document is a detailed implementation guide for building the Local Weather Data Warehouse defined in the project brief. It is written to keep the implementation work sequenced, controlled, and aligned with the project requirements. It should function as the working script for future setup sessions with an AI assistant.

The implementation plan is intentionally ordered around data engineering lifecycle thinking: source generation, storage, ingestion, transformation, orchestration, and serving, while also applying the cross-cutting concerns emphasized in *Fundamentals of Data Engineering*: software engineering, DataOps, architecture, orchestration, reproducibility, and security awareness.[cite:1]

## How to use this document

Use this guide as the authoritative sequence for implementation. Each phase should be completed in order unless there is a clear and documented reason to deviate. If an assistant suggests skipping ahead, introducing extra tools, or adding complexity not described here, that change should be treated as out of scope until it is explicitly approved in the brief or a later revision of this guide.[cite:1]

For each phase, the expected output is listed. Do not proceed to the next phase until the expected output is achieved and documented. This follows the book's guidance to prefer reversible decisions, avoid unnecessary complexity, and build loosely coupled systems with clear boundaries.[cite:1]

## Governing principles

The following principles govern all implementation decisions:

- Prefer simple, common components over novelty. The project stack should remain Git/GitHub, Docker Compose, PostgreSQL, Python, and Airflow unless a strong reason exists to change it.[cite:1]
- Make reversible decisions whenever possible. Folder structure, schema naming, Docker service design, and DAG boundaries should be easy to change without rewriting the whole system.[cite:1]
- Build loosely coupled layers. Bronze, silver, and gold should have distinct responsibilities, and orchestration should coordinate the work rather than hide complex business logic.[cite:1]
- Treat software engineering as a first-class concern. Code should be version controlled, organized, testable, and readable.[cite:1]
- Keep version 1 local-first and educational. The goal is not maximum feature count; the goal is a robust, understandable foundation.[cite:1]
- Plan for failure. Assume containers will misconfigure, APIs will fail, schemas will drift, and runs will need to be repeated safely.[cite:1]

## Target architecture

Version 1 should produce a local, containerized data platform with the following components:

- A Git repository hosted on GitHub as the system of record for all code, SQL, configuration templates, and documentation.
- A Docker Compose environment that runs PostgreSQL and Airflow locally.
- A Python-based ingestion process that calls the Open-Meteo API.
- A PostgreSQL warehouse organized into `bronze`, `silver`, and `gold` schemas.
- An Airflow DAG that orchestrates extract, load, transform, validation, and publish steps.
- Documentation sufficient for reproducing the system on another machine.[cite:1]

The intended lifecycle is: request data from Open-Meteo, preserve the raw response in bronze, normalize and clean the data in silver, publish analysis-ready tables or views in gold, and orchestrate everything through Airflow.[cite:1]

## Phase 1: Configure the repository

### Objective
Establish the repository as the foundation of the project before writing infrastructure or pipeline code.

### Rationale
The book emphasizes software engineering, repeatability, and common components as central to modern data engineering. Repository discipline is part of DataOps and reduces future friction when code, SQL, config, and docs start to grow.[cite:1]

### Tasks
1. Create the GitHub repository.
2. Clone it locally to the Debian machine.
3. Confirm Git identity settings on the machine.
4. Create a minimal initial branch structure. For version 1, a simple main branch plus feature branches is sufficient.
5. Add a project-level `README.md` with a short description, project purpose, and status.
6. Add a `.gitignore` that excludes secrets, local virtual environments, Python caches, editor settings that should stay local, Airflow-generated files that should not be tracked, and other environment-specific artifacts.
7. Decide where secrets will live. The repository should track only templates such as `.env.example`, never live credentials.[cite:1]
8. Create the initial folder structure.

### Recommended folder structure

```text
local-weather-data-warehouse/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docs/
│   ├── airflow_project_brief.md
│   └── airflow_project_implementation_plan.md
├── dags/
├── src/
│   ├── ingest/
│   ├── transform/
│   ├── load/
│   └── common/
├── sql/
│   ├── ddl/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── tests/
├── infra/
│   └── airflow/
└── data/
    └── samples/
```

### Decisions to record
- Repository name.
- Branching approach.
- Commit message conventions, even if lightweight.
- Whether SQL will be run from files, Python, or both.
- Whether schema creation lives in `sql/ddl/` or startup scripts.

### Expected output
- A live GitHub repository.
- A local clone.
- Initial commit pushed.
- Clear folder structure.
- README and `.gitignore` in place.

## Phase 2: Define architecture and scope in technical terms

### Objective
Translate the brief into concrete architectural decisions before setting up containers.

### Rationale
Good architecture begins with business and operational clarity, not with random tool installation. This phase turns the project brief into technical boundaries and reversible design choices.[cite:1]

### Tasks
1. Confirm that the source system for version 1 is Open-Meteo only.
2. Decide the initial scope of weather coverage: one location first, then optionally multiple locations later.
3. Decide the refresh cadence for v1. Daily is preferred because it reduces complexity while still exercising scheduling and repeatability.
4. Decide what data is required from Open-Meteo for the first pass, for example hourly temperature, precipitation, wind speed, humidity, and timestamps.
5. Define what bronze, silver, and gold mean for this project specifically.
6. Decide whether gold will be implemented as tables, views, or a mix. A conservative starting point is silver tables plus gold views or small materialized tables.
7. Identify the minimum viable Airflow DAG structure.

### Required architecture decisions
- Bronze stores raw API responses and ingestion metadata.
- Silver stores cleaned, typed, normalized weather records.
- Gold stores analysis-ready summaries, aggregates, or business-friendly models.
- Airflow orchestrates but does not become the only place where business logic lives.
- PostgreSQL is both the warehouse and the serving layer for v1.[cite:1]

### Questions to resolve before moving on
- What location will be used first?
- Which endpoint and variables will be requested?
- Will raw payloads be stored as `jsonb`?
- What columns are needed to support reruns and lineage, such as `ingested_at`, `source_url`, `run_id`, and `load_date`?

### Expected output
- A short architecture note in `docs/`.
- Confirmed v1 source and weather variables.
- Clear interpretation of bronze, silver, and gold for the project.

## Phase 3: Model the warehouse

### Objective
Design the PostgreSQL warehouse schemas and initial table structures before writing ingestion code.

### Rationale
Storage is foundational across the lifecycle, and the way data is stored affects downstream ingestion, transformation, and serving. Thoughtful schema design makes later steps easier and safer.[cite:1]

### Tasks
1. Create a SQL design note that lists all planned schemas and tables.
2. Define the three schemas: `bronze`, `silver`, and `gold`.
3. Design a bronze raw ingestion table.
4. Design one or more silver normalized tables.
5. Design one or more gold serving tables or views.
6. Decide primary keys, natural keys, uniqueness expectations, and index strategy.
7. Decide the handling of timestamps, time zones, null values, and source metadata.
8. Decide how reruns should behave, especially in silver and gold.

### Recommended warehouse pattern

#### Bronze
- `bronze.weather_api_raw`
- Purpose: store each raw Open-Meteo response as received.
- Suggested columns: `bronze_id`, `source_system`, `endpoint_name`, `location_name`, `latitude`, `longitude`, `requested_at`, `ingested_at`, `http_status`, `request_url`, `payload_json`, `run_id`.
- Load behavior: append only.

#### Silver
- `silver.weather_hourly`
- Purpose: one clean row per location and timestamp.
- Suggested columns: `location_name`, `latitude`, `longitude`, `observation_ts`, `temperature_2m`, `relative_humidity_2m`, `precipitation`, `wind_speed_10m`, `apparent_temperature`, `source_run_id`, `loaded_at`.
- Load behavior: upsert or replace by location and timestamp.

- Optional additional silver tables:
  - `silver.location_dim`
  - `silver.load_audit`

#### Gold
- `gold.daily_weather_summary`
- Purpose: one row per day per location with rollups.
- Suggested columns: `location_name`, `weather_date`, `temp_min`, `temp_max`, `temp_avg`, `precip_total`, `wind_speed_avg`, `record_count`, `last_refresh_at`.

- Optional additional gold objects:
  - `gold.current_weather_snapshot`
  - `gold.weather_trend_7d`

### Best-practice reminders
- Keep bronze close to the source.
- Apply standardization and type enforcement in silver.
- Put reporting logic and business-facing simplifications in gold.[cite:1]
- Avoid putting everything into one giant table just because PostgreSQL can handle it.
- Favor schemas and views that can be extended when new domains arrive later.[cite:1]

### Expected output
- SQL DDL files for schemas and initial tables.
- A documented data model for bronze, silver, and gold.

## Phase 4: Set up PostgreSQL locally

### Objective
Bring up PostgreSQL in Docker with persistent storage and validate access before involving Airflow.

### Rationale
The book recommends reducing undifferentiated heavy lifting but also understanding the systems you depend on. PostgreSQL should work independently before it becomes a dependency inside orchestration.[cite:1]

### Tasks
1. Add PostgreSQL to `docker-compose.yml`.
2. Configure container name, image version, environment variables, port mapping, and a named volume for persistence.
3. Decide how schema initialization will work: startup SQL scripts, manual setup, or a dedicated bootstrap script.
4. Start PostgreSQL only.
5. Connect to it from the host machine using `psql` or a GUI client.
6. Create the `bronze`, `silver`, and `gold` schemas.
7. Run the initial DDL.
8. Verify that the database persists after container restarts.

### Validation checklist
- Can the container start reliably?
- Can the database be connected to from the host?
- Are schemas and tables present?
- Does data persist after stopping and restarting containers?

### Expected output
- Running PostgreSQL container.
- Persistent volume configured.
- Warehouse schemas and tables created.

## Phase 5: Set up the Python development environment

### Objective
Create a simple, controlled Python workflow for local development and pipeline code.

### Rationale
Python is one of the primary languages of data engineering and will be used as glue code for API interaction, parsing, and orchestration-friendly tasks.[cite:1]

### Tasks
1. Choose Python 3.12 unless compatibility issues emerge.
2. Decide whether local development will use a virtual environment outside Docker, inside Docker, or both. A practical approach is both: local venv for iteration and containerized execution for reproducibility.
3. Create a `requirements.txt` or `pyproject.toml` strategy for dependencies.
4. Add initial packages, likely including `requests`, `pandas` if needed, `psycopg2-binary` or `sqlalchemy`, and any lightweight config library if desired.
5. Add a basic project package structure under `src/`.
6. Confirm a minimal script can run locally and connect to PostgreSQL.

### Expected output
- Working Python environment.
- Dependency file checked into GitHub.
- Minimal Python-to-Postgres connectivity proven.

## Phase 6: Build the Open-Meteo extraction logic

### Objective
Implement the first source interaction in plain Python before wrapping it in Airflow.

### Rationale
A core recommendation from the book is to understand the source system and ingestion characteristics directly. Building and validating extraction outside orchestration reduces ambiguity and isolates failure points.[cite:1]

### Tasks
1. Read the Open-Meteo API documentation for the chosen endpoint.
2. Record the request parameters required for the project.
3. Create a Python module that builds the request URL in a deterministic, logged way.
4. Call the API and capture the response.
5. Validate the HTTP status code and handle non-200 responses.
6. Validate that expected fields exist in the payload.
7. Record request metadata such as request time, location, endpoint, and source URL.
8. Save one or more sample responses locally for inspection and schema design if useful.

### Best practices
- Keep API logic isolated in `src/ingest/`.
- Avoid mixing API requests, SQL DDL, and orchestration code in the same file.
- Design the request builder so new endpoints or new locations can be added later.[cite:1]
- Fail loudly on malformed responses instead of silently loading bad data.[cite:1]

### Expected output
- A script or module that can successfully call Open-Meteo and return validated JSON.
- Sample payloads for inspection.

## Phase 7: Load raw data into bronze

### Objective
Persist raw API responses into PostgreSQL without premature transformation.

### Rationale
Bronze should preserve source truth and ingestion metadata. This protects against reprocessing issues and supports lineage and troubleshooting.[cite:1]

### Tasks
1. Write a load function that inserts one raw API response into `bronze.weather_api_raw`.
2. Store the full payload in `jsonb`.
3. Capture metadata fields such as `run_id`, `source_system`, `endpoint_name`, and `ingested_at`.
4. Confirm append-only behavior.
5. Run the ingestion multiple times and verify multiple raw records are preserved.
6. Add a lightweight query or notebook snippet to inspect bronze contents.

### Validation checklist
- Does the raw JSON land intact?
- Is metadata sufficient to trace each load?
- Can raw rows be tied back to a specific execution or request?

### Expected output
- Repeatable bronze raw ingestion working outside Airflow.

## Phase 8: Transform bronze to silver

### Objective
Normalize raw weather JSON into clean, structured tables.

### Rationale
Transformation is where raw data becomes high-quality, reusable information. Silver should apply typing, normalization, and quality checks while remaining close enough to the source to preserve meaning.[cite:1]

### Tasks
1. Inspect the JSON structure for hourly arrays and metadata.
2. Decide the grain of the silver table. For v1, the grain should likely be one row per location per timestamp.
3. Parse the hourly payload into tabular form.
4. Cast strings to the correct types.
5. Standardize timestamps and time zone handling.
6. Apply basic data quality checks, such as row counts, null expectations, and duplicate detection.
7. Load the results into `silver.weather_hourly`.
8. Decide whether silver loads are full refreshes or idempotent upserts.

### Best practices
- Keep transformation code isolated from orchestration code.[cite:1]
- Keep business rules minimal in silver; this layer is for cleaned, reusable data, not reporting-specific logic.[cite:1]
- Record enough metadata to explain where silver rows came from.

### Expected output
- A populated silver weather table with typed, clean records.
- Documented grain and keys.

## Phase 9: Transform silver to gold

### Objective
Create analysis-ready serving objects for downstream use.

### Rationale
Gold exists so downstream users do not have to repeatedly reinvent calculations or understand source-specific quirks. It is the serving layer of the warehouse for this project.[cite:1]

### Tasks
1. Decide the first gold outputs.
2. Create SQL or Python transformations that summarize silver data into business-friendly structures.
3. Start with one gold object that clearly adds value, such as daily weather summaries.
4. If useful, add one current-state object such as a latest weather snapshot.
5. Document the purpose and grain of each gold object.

### Recommended first gold object
- `gold.daily_weather_summary`
- One row per date per location.
- Includes min, max, average temperature, total precipitation, average wind speed, and audit timestamps.

### Expected output
- At least one working gold object in PostgreSQL.
- Query-ready serving layer for analysis.
