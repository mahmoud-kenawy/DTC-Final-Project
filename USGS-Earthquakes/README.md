# 🌍 USGS Earthquakes — End-to-End Data Engineering Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![dlt](https://img.shields.io/badge/dlt-Data_Load_Tool-FF6B35)
![dbt](https://img.shields.io/badge/dbt-Data_Build_Tool-FF69B4?logo=dbt&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?logo=apache-airflow&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?logo=snowflake&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**An automated, production-grade ELT pipeline that ingests live global earthquake data, transforms it into analytics-ready models, and surfaces insights through an interactive dashboard.**

[📊 View Dashboard PDF](docs/Earthquake-Dashboard.pdf) · [🏗️ Architecture](#️-architecture) · [🚀 Quickstart](#-setup--installation)

</div>

---

## 📖 Table of Contents

- [Problem Statement](#-problem-statement)
- [Architecture](#️-architecture)
- [Tech Stack](#-tech-stack)
- [Data Source](#-data-source)
- [Data Models (dbt Lineage)](#-data-models--dbt-lineage)
- [Orchestration (Airflow DAG)](#-orchestration--airflow-dag)
- [Dashboard](#-dashboard)
- [Pipeline in Action](#-pipeline-in-action)
- [Setup & Installation](#-setup--installation)
- [Running the Pipeline](#-running-the-pipeline)
- [Project Structure](#-project-structure)

---

## 🎯 Problem Statement

> **Who is this for?** Rescue teams, governments, researchers, and residents in earthquake-prone regions who need reliable, up-to-date seismic data to make informed decisions.

Earthquake data is publicly available from the USGS, but it comes as raw GeoJSON — deeply nested, difficult to query, and updated continuously. There is no easy way for analysts to ask questions like:

- 🗺️ *Where do earthquakes cluster geographically?*
- 📉 *Is there a correlation between earthquake depth and magnitude?*
- 🌊 *Which events pose a tsunami risk?*
- ⚠️ *What is the distribution of alert levels (green / yellow / orange / red)?*

This project solves that by building a **robust, automated ELT pipeline** that:

1. **Extracts** live earthquake data from the USGS REST API every run
2. **Loads** raw GeoJSON into a Snowflake data warehouse using **dlt**
3. **Transforms** the raw data into clean, analytics-ready tables using **dbt**
4. **Orchestrates** the entire workflow on a schedule using **Apache Airflow**
5. **Visualises** the results in an interactive **dashboard**

---

## 🏗️ Architecture

The project follows a standard **ELT (Extract → Load → Transform)** pattern. Unlike ETL, data is loaded raw first and transformed *inside* the warehouse — making it easier to reprocess, audit, and extend.

![Architecture Diagram](docs/DTCFinal.drawio%20.svg)

```
USGS REST API  ──(dlt)──▶  Snowflake (raw)  ──(dbt)──▶  Snowflake (marts)  ──▶  Dashboard
      ↑                                                                              ↑
      └─────────────────────── Apache Airflow (Scheduler) ─────────────────────────┘
```

| Stage | Tool | What happens |
|-------|------|-------------|
| **Extract & Load** | `dlt` | Fetches GeoJSON from USGS API, flattens nested structures, upserts into Snowflake |
| **Transform** | `dbt` | Cleans, casts types, extracts coordinates, builds staging & mart models |
| **Orchestrate** | `Airflow` (Astronomer) | Schedules and monitors both tasks in sequence |
| **Visualise** | Dashboard (PDF) | Maps, charts, and KPIs built on top of the dbt mart tables |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Ingestion** | [dlt (data load tool)](https://dlthub.com/) | Schema-aware API ingestion into Snowflake |
| **Warehouse** | [Snowflake](https://www.snowflake.com/) | Cloud data warehouse — stores raw and transformed data |
| **Transformation** | [dbt](https://www.getdbt.com/) | SQL-based data modelling, testing & documentation |
| **Orchestration** | [Apache Airflow](https://airflow.apache.org/) via [Astronomer](https://www.astronomer.io/) | Scheduling, monitoring, retries |
| **Language** | Python 3.9+ | Pipeline scripting |
| **Containerisation** | Docker | Local Airflow runtime via Astro CLI |

---

## 📡 Data Source

| Property | Details |
|----------|---------|
| **Provider** | United States Geological Survey (USGS) |
| **Endpoint** | [USGS Earthquakes Feed](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson) |
| **Scope** | All recorded global earthquakes — past 30 days |
| **Format** | GeoJSON (nested) |
| **Update frequency** | Live / Continuous |
| **Key fields** | `id`, `magnitude`, `depth`, `longitude`, `latitude`, `alert_level`, `tsunami`, `event_type`, `review_status`, `time` |

---

## 🔗 Data Models & dbt Lineage

The dbt project transforms raw data through **three layers**:

```
Raw Source                Staging                     Mart (analytics-ready)
─────────────────────────────────────────────────────────────────────────────
usgs_data.earthquakes ──▶ stg_earthquake ──┬──▶ mrt_emergency
                                            ├──▶ mrt_earthquake_categories
                                            └──▶ mrt_aggregations
```

![dbt Lineage Graph](docs/dbt_lineage.jpg)

### Model Descriptions

| Model | Type | Description |
|-------|------|-------------|
| `stg_earthquake` | View | Cleans raw JSON: casts timestamps, extracts lon/lat/depth, standardises magnitude & alert fields |
| `mrt_emergency` | Table | Filters events by alert level; used for emergency preparedness reporting |
| `mrt_earthquake_categories` | Table | Categorises earthquakes by magnitude range, depth band, and event type |
| `mrt_aggregations` | Table | Time-based and geo-based aggregate statistics for dashboard KPIs |

> **For non-engineers:** Think of dbt models like Excel formulas that live in version-controlled SQL files. Raw data goes in dirty; clean, structured tables come out.

---

## ✈️ Orchestration & Airflow DAG

The pipeline is orchestrated by Apache Airflow running inside Docker via Astronomer's Astro CLI. The DAG (`usgs_dag`) contains two tasks that run sequentially:

![Airflow DAG Graph](docs/usgs_dag-graph.png)

| Task | Operator | Description |
|------|----------|-------------|
| `run_pipeline` | `PythonOperator` | Executes `usgs_pipeline.py` — fetches USGS data and loads it into Snowflake via dlt |
| `dbt_build` | `BashOperator` | Runs `dbt build` — executes all models AND runs all data quality tests |

The DAG ensures dbt only runs *after* fresh data has been successfully loaded. If the ingestion step fails, the transformation step is skipped automatically.

---

## 📊 Dashboard

The dashboard PDF (`docs/Earthquake-Dashboard.pdf`) showcases the final output of the pipeline. It is built directly on the dbt mart tables in Snowflake.

**📄 [Click here to open the Dashboard PDF](docs/Earthquake-Dashboard.pdf)**

**Dashboard highlights:**
- 🗺️ **Global earthquake map** — geographical distribution with magnitude-scaled markers
- 📊 **Magnitude distribution** — histogram of earthquake sizes
- 🌊 **Tsunami risk breakdown** — proportion of events flagging tsunami potential
- ⚠️ **Alert level distribution** — green / yellow / orange / red severity counts
- 📅 **Temporal trends** — earthquake frequency over the last 30 days
- 💡 **KPI cards** — total events, average depth, max magnitude

---

## 🔬 Pipeline in Action

### `run_pipeline` Task — dlt Ingestion Log

The pipeline task connects to the USGS API, loads data into Snowflake, and completes in ~37 seconds.

![Pipeline Task Log](docs/pipelinetask_log.jpg)

Key log highlights:
- ✅ REST API source configured successfully
- ✅ Connected to Snowflake (Global domain)
- ✅ Pipeline `usgs_earthquake_pipeline` completed in **23.52 seconds**
- ✅ 1 load package successfully pushed to `usgs_data` dataset with **0 failed jobs**

---

### `dbt_build` Task — Transformation & Testing Log

dbt runs all models and 8 data quality tests end-to-end in under 8 seconds.

![dbt Build Task Log](docs/dbttask_log.jpg)

Key log highlights:
- ✅ Found **5 models**, **8 data tests**, **1 source**
- ✅ `stg_earthquake` view created in 0.36s
- ✅ All **8 data tests passed** (uniqueness, not-null, accepted values)
- ✅ `mrt_aggregations` → 36 rows, `mrt_earthquake_categories` → 12,982 rows, `mrt_emergency` → 164 rows, `mrt_earthquakes_dashboard` → 12,982 rows
- ✅ Completed in **7.08 seconds** — `PASS=13 WARN=0 ERROR=0 SKIP=0`

---

## 🚀 Setup & Installation

### Prerequisites

Before you begin, make sure you have:

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **Docker Desktop** — [Download](https://docs.docker.com/get-docker/) *(required for running Airflow locally)*
- **Astro CLI** — [Install guide](https://docs.astronomer.io/astro/cli/install-cli) *(Astronomer's tool for Airflow)*
- **Snowflake account** — [Free trial](https://signup.snowflake.com/) *(the data warehouse)*

> **New to Snowflake?** You need a `database`, `warehouse`, `schema`, `username`, `password`, and `account` identifier. These are all created during Snowflake setup.

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/mahmoud-kenawy/DTC-Final-Project.git
cd DTC-Final-Project/USGS-Earthquakes
```

### Step 2 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Configure dlt (Snowflake credentials)

Create the file `.dlt/secrets.toml` in the project root:

```toml
[destination.snowflake.credentials]
database  = "YOUR_DATABASE"
password  = "YOUR_PASSWORD"
username  = "YOUR_USERNAME"
host      = "YOUR_ACCOUNT.snowflakecomputing.com"
warehouse = "YOUR_WAREHOUSE"
role      = "YOUR_ROLE"
```

> ⚠️ Never commit this file. It is already listed in `.gitignore`.

### Step 4 — Configure dbt Profile

Add the following to your `~/.dbt/profiles.yml` (create the file if it doesn't exist):

```yaml
usgs_earthquake_dbt:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: YOUR_ACCOUNT
      user: YOUR_USERNAME
      password: YOUR_PASSWORD
      role: YOUR_ROLE
      database: YOUR_DATABASE
      warehouse: YOUR_WAREHOUSE
      schema: usgs_data
      threads: 4
```

---

## 🏃 Running the Pipeline

### Option A — Manual (no Airflow)

Run each step individually from the project root:

```bash
# 1. Ingest data from USGS into Snowflake
python usgs_pipeline.py

# 2. Transform raw data and run tests
cd usgs_earthquake_dbt
dbt build
```

### Option B — Orchestrated via Airflow (recommended)

```bash
# Navigate to the airflow directory
cd airflow

# Start the Docker-based Airflow environment
astro dev start
```

Once started:
1. Open your browser at **http://localhost:8080**
2. Login with `admin` / `admin`
3. Find the `usgs_dag` DAG and toggle it **ON**, or click **Trigger DAG** to run it immediately
4. Watch the `run_pipeline` → `dbt_build` tasks execute in sequence ✅

---

## 📁 Project Structure

```text
USGS-Earthquakes/
│
├── 📄 usgs_pipeline.py          # dlt ingestion script (connects to USGS API → Snowflake)
├── 📄 requirements.txt          # Python package dependencies
├── 📄 .env                      # Environment variables (not committed)
│
├── 📂 .dlt/                     # dlt configuration & secrets (not committed)
│   └── secrets.toml
│
├── 📂 airflow/                  # Astronomer Airflow environment
│   ├── dags/
│   │   └── usgs_dag.py          # Airflow DAG definition (run_pipeline → dbt_build)
│   ├── Dockerfile
│   └── airflow_settings.yaml
│
├── 📂 usgs_earthquake_dbt/      # dbt project
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_earthquake.sql
│   │   └── marts/
│   │       ├── mrt_emergency.sql
│   │       ├── mrt_earthquake_categories.sql
│   │       ├── mrt_aggregations.sql
│   │       └── mrt_earthquakes_dashboard.sql
│   ├── dbt_project.yml
│   └── profiles.yml
│
└── 📂 docs/                     # Project documentation & assets
    ├── DTCFinal.drawio.svg      # Architecture diagram
    ├── Earthquake-Dashboard.pdf # Final dashboard export
    ├── dbt_lineage.jpg          # dbt model lineage graph
    ├── usgs_dag-graph.png       # Airflow DAG graph
    ├── pipelinetask_log.jpg     # Airflow run_pipeline task log
    └── dbttask_log.jpg          # Airflow dbt_build task log
```

---

## 🙏 Acknowledgements

- [DataTalks.Club](https://datatalks.club/) — for the Data Engineering Zoomcamp curriculum
- [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/) — for providing the free public API
- [dlt Hub](https://dlthub.com/) — for the lightweight, schema-aware data loading library
- [Astronomer](https://www.astronomer.io/) — for the managed Airflow runtime and Astro CLI

---

<div align="center">

Made with ❤️ as part of the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) Final Project

</div>
