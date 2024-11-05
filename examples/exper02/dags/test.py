from datetime import datetime, timedelta

import pytz
from airflow import DAG
from airflow.operators.bash import BashOperator

# Set JST as the timezone
jst = pytz.timezone("Asia/Tokyo")

# Define default arguments for the DAG
default_args = {
    "owner": "ghasak",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 5,
    "retry_delay": timedelta(minutes=1),
}

# Define the DAG
with DAG(
    "run_main_script_dag",
    default_args=default_args,
    description="This is our first DAG that we write",
    start_date=jst.localize(datetime(2024, 11, 4, 22, 5)),  # JST start time
    schedule_interval="*/10 * * * *",  # Every 10 seconds
    catchup=False,
) as dag:

    # Task to run the Python script using BashOperator
    run_main_script = BashOperator(
        task_id="run_main_script",
        bash_command="python -m src.main",
        cwd="/airflow/",
    )

    run_main_script
