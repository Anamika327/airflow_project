airflow_project/
└── include/
    ├── data/
    │   └── northwind.duckdb
    ├── pipelines/
    │   └── extract_to_bronze.py
    └── gx/
        ├── checkpoints/
        ├── expectations/
        ├── validation_definitions/
        ├── plugins/
        ├── uncommitted/
        ├── great_expectations.yml
        └── .gitignore


API
 ↓
Python
 ↓
DuckDB Bronze
 ↓
Great Expectations
      ↓
SQL Data Source
      ↓
Validation
 ↓
dbt