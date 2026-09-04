Overview
========

my-northwind-pipeline/
├── .astro/                   # Astro configuration (auto-generated)
├── dags/                     # Airflow DAGs
│   └── northwind_pipeline.py # Main orchestration DAG
├── dbt_northwind/            # Full dbt project directory
│   ├── analyses/
│   ├── macros/
│   ├── models/               # dbt transformation models
│   │   ├── staging/          # Staging models (clean raw DuckDB data)
│   │   └── marts/            # Business-ready models
│   ├── seeds/                # Raw Northwind CSVs (optional, if loading via dbt)
│   ├── tests/
│   ├── dbt_project.yml       # dbt project configuration
│   └── profiles.yml          # dbt connection profile for DuckDB
├── include/                  # Extra files for Airflow tasks
│   ├── great_expectations/   # Great Expectations configuration
│   │   ├── expectations/     # JSON files containing validation rules
│   │   ├── checkpoints/      # Checkpoint definitions
│   │   └── great_expectations.yml
│   └── scripts/
│       └── extract_to_duckdb.py # Python script to ingest raw data into DuckDB
├── data/
│   └── northwind.duckdb      # The persistent DuckDB database file
├── .dockerignore
├── .gitignore
├── Dockerfile                # Custom Dockerfile to install dbt and GX
├── packages.txt              # System-level dependencies (e.g., build-essential)
├── README.md
└── requirements.txt          # Python libraries (cosmos, great-expectations, etc.)
