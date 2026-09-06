from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


def extract_bronze():
    from pipelines.extract_to_bronze import main

    main()


def validate_bronze():
    import runpy

    runpy.run_path(
        "/usr/local/airflow/include/pipelines/validate_raw_orders.py",
        run_name="__main__",
    )


with DAG(
    dag_id="northwind_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["northwind", "data-engineering"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_bronze",
        python_callable=extract_bronze,
    )

    validate_task = PythonOperator(
        task_id="validate_raw_orders",
        python_callable=validate_bronze,
    )

    dbt_task = BashOperator(
        task_id="dbt_stg_orders",
        bash_command=(
            "/usr/local/airflow/dbt_venv/bin/dbt run "
            "--project-dir /usr/local/airflow/include/dbt/northwind "
            "--profiles-dir /usr/local/airflow/include/dbt/northwind "
            "--select stg_orders"
        ),
    )

    extract_task >> validate_task >> dbt_task