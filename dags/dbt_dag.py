from datetime import datetime

from airflow import DAG
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig


with DAG(
    dag_id="my_first_dbt_project",
    start_date=datetime(2026, 8, 12),
    schedule=None,
    catchup=False,
) as dag:

    dbt_project = DbtTaskGroup(
        group_id="dbt_project",

        project_config=ProjectConfig(
            dbt_project_path="/usr/local/airflow/dags/dbt/my_first_project",
        ),

        profile_config=ProfileConfig(
            profile_name="my_first_project",
            target_name="dev",
            profiles_yml_filepath="/usr/local/airflow/dags/dbt/profiles.yml",
        ),

        execution_config=ExecutionConfig(
            dbt_executable_path="/usr/local/airflow/dbt_venv/bin/dbt",
        ),
    )