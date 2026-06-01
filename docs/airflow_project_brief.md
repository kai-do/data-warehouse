# Airflow Project Brief

## Project overview
**Project name:** Local Weather Data Warehouse

**One-sentence goal:** Build a local, Dockerized data warehouse that ingests weather data from the Open-Meteo API into PostgreSQL and orchestrates repeatable ELT pipelines with Apache Airflow.

**Why this project matters:** This project will develop practical data engineering skills from the ground up by applying sound architecture, orchestration, storage, transformation, and software engineering practices in a real end-to-end system. The project is also intended to follow the principles described in *Fundamentals of Data Engineering* by Joe Reis and Matt Housley, with a strong emphasis on lifecycle thinking, reproducibility, loose coupling, and clarity of design.

**Current skill level:**
- Python: Low; stronger in R, with only basic Python experience.
- Docker: Low; some guided experience using AI-assisted projects.
- SQL/PostgreSQL: High; about 7 years of T-SQL experience.
- dbt: None.
- Airflow: None.

## Problem statement
There is currently no local, version-controlled analytics environment for collecting, storing, transforming, and serving weather data in a warehouse structure that can be understood end to end. This project solves that by creating a reproducible, containerized data warehouse that starts with one external source, Open-Meteo, and establishes a foundation that can later be extended with additional datasets.

## Primary objective
For version 1, create a fully working local data warehouse that pulls weather data from Open-Meteo on a schedule, stores it in bronze, silver, and gold layers in PostgreSQL, and orchestrates the full workflow with Apache Airflow.

## Success criteria
The project is successful if it meets all of the following:
- Every step in the pipeline is understandable, documented, and explainable.
- A version-controlled, portable data warehouse is built in Git and GitHub and can be run on other hardware using Docker Compose.
- Weather data is extracted from Open-Meteo and loaded into PostgreSQL through a layered bronze, silver, and gold warehouse design.
- The Airflow DAG runs successfully on a schedule and can also be triggered manually.
- Failures can be investigated through clear logs and basic retry behavior.
- The warehouse design leaves room to add more data domains later without major rework.

## Environment
- Operating system: Debian.
- Airflow setup approach: Docker Compose.
- PostgreSQL setup: Docker container with persistent storage.
- Python version: Python 3.12 unless compatibility issues require 3.11.
- Main editor/IDE: VS Code.
- Version control platform: Git with GitHub.

## Data flow
**Source data:**
- Type: API.
- Location: Open-Meteo weather API.
- Expected size/volume: Small in version 1; likely one or a few locations, with hourly or daily weather observations and forecasts stored as JSON and normalized relational tables.
- Refresh frequency: Start with a scheduled daily load, with the option to move to hourly later.

**Transformations needed:**
- Store the raw Open-Meteo API response with metadata in the bronze layer.
- Parse and normalize JSON fields into structured weather records in the silver layer.
- Build gold tables or views that support analysis, such as daily summaries, trend-ready aggregates, or location-based reporting tables.
- Standardize timestamps, weather variables, and load metadata for reproducibility and auditing.

**Destination:**
- Target database: PostgreSQL.
- Schema: `bronze`, `silver`, and `gold`.
- Table(s): Initial tables will likely include a bronze raw payload table, one or more silver structured weather tables, and one or more gold analytics-ready summary tables.
- Load type: Append in bronze; transform and upsert or replace in silver and gold as appropriate.

## Functional requirements
The project must do the following:
- Call the Open-Meteo API and retrieve weather data for at least one location.
- Persist raw source payloads and ingestion metadata in the bronze layer.
- Transform raw weather data into structured relational tables in the silver layer.
- Publish analytics-ready summary tables or views in the gold layer.
- Run the pipeline end to end through an Airflow DAG.
- Support local execution and repeatable deployment through Docker Compose.
- Include logging, basic retries, and clear error visibility.
- Be structured so that new data sources can be added later.

## Non-functional requirements
The project should satisfy the following quality constraints:
- Run locally first.
- Be understandable and easy to debug.
- Use clear folder structure and naming.
- Be reproducible on another machine with documented setup steps.
- Use persistent database storage through Docker volumes.
- Prefer simple, explicit design over premature optimization.
- Everything in the project should be version controlled unless it is explicitly generated, secret, or environment-specific.
- Follow basic version control and software engineering discipline using Git and GitHub.

## Learning goals
By the end of the project, the following should be understood:
- How to structure a small but real data warehouse using bronze, silver, and gold layers.
- How Docker Compose manages a multi-container local data platform.
- How Python is used to extract, validate, and load API data.
- How Airflow DAGs, tasks, scheduling, retries, and connections work.
- How PostgreSQL fits into ingestion, transformation, and serving layers.
- How to think through a data engineering project using lifecycle principles rather than tool hype.

## Scope
**In scope for version 1:**
- One weather data source: Open-Meteo.
- One local PostgreSQL warehouse with bronze, silver, and gold schemas.
- One Airflow DAG orchestrating extraction, loading, transformation, and publishing.
- One or a few locations to keep the problem tractable.
- Basic data quality checks and logging.
- Project documentation and version-controlled setup.

**Out of scope for version 1:**
- AWS deployment.
- Kubernetes.
- Advanced Airflow scaling.
- Multiple external data sources.
- Streaming or real-time ingestion.
- dbt, unless later introduced as a separate enhancement.
- BI dashboards as a required deliverable.

## Assumptions
- Open-Meteo provides enough free data for development and learning use.
- PostgreSQL is sufficient for the initial warehouse and analytics requirements.
- A local machine running Debian and Docker can support the needed containers.
- Starting with one source and one domain is the best way to learn the end-to-end lifecycle.

## Risks and blockers
- Low Python and Airflow experience may slow early development.
- Docker networking, permissions, or volume configuration could cause setup friction.
- API schema changes or misunderstood fields could create transformation errors.
- Over-scoping version 1 could delay completion and reduce learning focus.
- Designing too much up front without implementing incrementally may create avoidable complexity.

## Deliverables
What should exist when the project is done?
- A Docker Compose project that runs PostgreSQL and Airflow locally.
- A working Airflow DAG.
- Bronze, silver, and gold schemas in PostgreSQL.
- PostgreSQL tables populated by the DAG.
- A README or runbook with setup, run, and debugging steps.
- Basic architecture notes explaining the pipeline and warehouse layers.
- Version-controlled project files stored in GitHub and ready to run on another machine.
- A properly configured repository with sensible ignore rules, documentation, and project structure.

## Broad implementation plan
1. Configure the repository, including folder structure, Git and GitHub setup, `.gitignore`, README, environment file strategy, and conventions for version control.
2. Define the Open-Meteo source, target locations, warehouse schemas, and initial table design.
3. Confirm PostgreSQL connectivity and schema creation outside Airflow.
4. Set up Airflow and PostgreSQL locally with Docker Compose.
5. Create a simple Python extraction script for Open-Meteo.
6. Persist raw API responses into the bronze layer.
7. Transform bronze data into normalized silver tables.
8. Build gold tables or views for analytics-ready consumption.
9. Convert the workflow into Airflow tasks and define scheduling, retries, and dependencies.
10. Test, debug, and verify the full pipeline in PostgreSQL.
11. Clean up the project structure and document the workflow.

## Definition of done
The project is done when a new machine can clone the repository, start the Docker Compose environment, run Airflow, pull Open-Meteo weather data, and populate a working PostgreSQL warehouse with bronze, silver, and gold layers through a documented and understandable pipeline.

## Notes
This project should favor simplicity, learning value, and architectural clarity over speed or feature count. The design should support future expansion into other subject areas after the weather pipeline is stable and well understood.
