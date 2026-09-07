airflow_project/
│
├── dags/
│   └── northwind_pipeline.py
│
├── include/
│   ├── data/
│   │   └── northwind.duckdb
│   │
│   ├── pipelines/
│   │   ├── extract_to_bronze.py
│   │   ├── configure_raw_orders_gx.py
│   │   └── validate_raw_orders.py
│   │
│   ├── gx/
│   │   ├── checkpoints/
│   │   ├── expectations/
│   │   ├── validation_definitions/
│   │   ├── plugins/
│   │   ├── uncommitted/
│   │   ├── great_expectations.yml
│   │   └── .gitignore
│   │
│   └── dbt/
│       └── northwind/
│           ├── dbt_project.yml
│           ├── profiles.yml
│           ├── models/
│           │   └── staging/
│           │       ├── sources.yml
│           │       └── stg_orders.sql
│           ├── macros/
│           ├── seeds/
│           ├── snapshots/
│           ├── tests/
│           └── analyses/
│
├── Dockerfile
└── .astro/
    └── config.yaml