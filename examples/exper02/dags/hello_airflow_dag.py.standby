from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define the log file path in the dags directory
LOG_FILE_PATH = "/opt/airflow/dags/output_log.txt"


# Define the Python function to write "airflow" to the file with a counter
def append_to_file(**context):
    # Get the current timestamp and task instance counter
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task_instance = context['task_instance']
    counter = task_instance.try_number  # Auto-increment task try_number

    # Write the message to the log file
    with open(LOG_FILE_PATH, "a") as f:
        f.write(f"{counter} - {timestamp}: airflow\n")

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 27),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    'hello_airflow_dag',
    default_args=default_args,
    schedule_interval='*/1 * * * *',  # Run every second
    catchup=False,
)

# Task 1: BashOperator to print "hello" and append to the file
task_hello = BashOperator(
    task_id='say_hello',
    bash_command=f'echo "$(date +%Y-%m-%d\ %H:%M:%S) - hello" >> {LOG_FILE_PATH}',
    dag=dag,
)

# Task 2: PythonOperator to append "airflow" to the file with counter and timestamp
task_airflow = PythonOperator(
    task_id='say_airflow',
    python_callable=append_to_file,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
task_hello >> task_airflow

