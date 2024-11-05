# Airflow Up and Running

Here’s a refined version of your notes with enhanced clarity, corrected spelling, and logical flow. I've also added some `bonus` notes for additional considerations:

---

### Airflow Usage in a Docker-Based Environment

- **Containerized Python Execution**:

  - When using `Airflow` within a container based on a Docker image, you are limited to the Python environment inside that container.
  - This means that any tasks or scripts you want to execute with `BashOperator` must have all dependencies available within the container.

- **Accessing Project Files**:

  - To run scripts like `src/main.py` using `BashOperator`, map the required directories as volumes. This allows the container to access your project's files.
  - Alternatively, you can create a custom Docker image by using the official Airflow image as a base. During the image build, include a `requirements.txt` file to install any additional Python dependencies.

- **Controlling Python Dependencies**:

  - If you need more control over the Python environment (such as specific library versions), use a custom Docker image that includes your `requirements.txt` file.
  - This approach ensures that all necessary packages are available in the environment, which is helpful for complex workflows.

- **Time Zone Awareness**:

  - Be mindful of time zones when scheduling tasks in Airflow. If not configured properly, tasks may not trigger at expected times. Setting `timezone` in the DAG or globally in `airflow.cfg` can help manage time zone discrepancies.

- **Local Airflow Installation Compatibility**:
  - When running Airflow on a local installation with a virtual environment, you can execute any `bash` commands your system supports, such as `fzf`, `bat`, or `pipenv`.
  - This flexibility makes local setups convenient for development and testing workflows that require external CLI tools.

### Common Practices for Workflow Organization

- **ETL-Based Task Organization**:

  - When using `ETL` tasks, each module can be decorated with `@task` (e.g., `@task` or `@task.python`) to define its role in the pipeline.
  - In `airflow.cfg`, specify `dags_folder` to point to the directory where your DAG scripts are located, such as `dags_folder = ~/airflowHub/examples/dags`.
  - Use `PythonOperator` or task decorators to run specific Python functions or scripts. You can update `dags_folder` in `airflow.cfg` to direct Airflow to locate your tasks in files like `src/main.py`.

- **Single-Entry-Point Workflow Execution**:
  - A simplified alternative is to set a single entry point, such as `src.main`, to run the entire project at once. This can be executed with a command like `pipenv run python -m src.main`.
  - For this setup, use `BashOperator` with the `bash_command` argument to specify the full execution command.
  - Ensure that `cwd` in `BashOperator` points to the root directory of your project so Airflow knows where to locate the files and start the workflow.

---

### Bonus Notes

- **Managing Data Transfer Between Tasks**:

  - **XCom Size Limitations**: Data transfer between tasks in Airflow (using XCom) is limited in size (typically a few KB). For larger data, consider using an intermediary storage solution (e.g., database, file storage).
  - **External Data Storage**: Use systems like S3, Google Cloud Storage, or shared databases to store larger datasets. Tasks can then read from and write to these systems, bypassing XCom limitations.

- **Optimizing Logging**:

  - **Reduce Log Verbosity**: In `airflow.cfg`, you can adjust the log levels for different Airflow components (e.g., `INFO`, `WARN`, `ERROR`) to minimize excessive logging.
  - **Disable Unnecessary Logging**: Certain executors, such as the `SequentialExecutor`, produce verbose logs. Consider using a more robust executor like `LocalExecutor` or `CeleryExecutor` if you need better logging control and higher parallelism.
  - **Log Retention**: Set up log rotation or log cleanup to avoid clutter and manage disk space effectively, especially for long-running or frequently scheduled DAGs.

- **Improving Scheduler Performance**:

  - **Parallelism and Concurrency**: Adjust `parallelism`, `dag_concurrency`, and `max_active_runs_per_dag` in `airflow.cfg` based on your system's capabilities and workload requirements.
  - **Executor Choice**: Use `CeleryExecutor` for distributed task execution across multiple workers, especially for heavy workloads. `LocalExecutor` is more suited for single-machine deployments with moderate parallelism.
  - **Database Performance**: Optimize your Airflow metadata database with indexing and proper maintenance to speed up the scheduler and reduce latency in task status updates.

- **Error Handling and Retries**:

  - **Retries and Delays**: Configure `retries` and `retry_delay` for each task to ensure resilience. This allows tasks to retry automatically in case of transient failures.
  - **Alerts**: Set up `email_on_failure` or `slack_on_failure` notifications to alert you in case of critical task failures.

- **Testing DAGs Locally**:
  - Use commands like `airflow dags trigger <dag_id>` and `airflow tasks test <dag_id> <task_id> <execution_date>` to test DAGs and individual tasks before deployment.
  - This approach helps catch issues early and provides a controlled environment to debug problems without affecting production workflows.

These refined notes should provide a clearer understanding of Airflow best practices, along with some additional tips to enhance your workflow management and efficiency.

---

## CONSIDERATIONS

To apply changes made in the `airflow.cfg` file, it's generally necessary to
restart the relevant Airflow components, such as the scheduler, webserver, and
workers. This ensures that the updated configurations are loaded and take
effect.

**Steps to Apply Configuration Changes:**

1. **Modify `airflow.cfg`:**

   - Edit the `airflow.cfg` file located in your `AIRFLOW_HOME` directory to update the desired settings.

2. **Restart Airflow Components:**

   - After saving the changes, restart the Airflow components to apply the new
     configurations. The method to restart these components depends on how
     Airflow is deployed:

   - **Systemd Managed Services:**

     - If Airflow services are managed by systemd, use the following commands:
       ```bash
       sudo systemctl restart airflow-scheduler
       sudo systemctl restart airflow-webserver
       sudo systemctl restart airflow-worker # If using CeleryExecutor or similar
       ```
     - This approach is detailed in the Airflow webserver restart guide. citeturn0search8

   - **Manually Started Services:**
     If you start Airflow components manually, stop and then start each component:

     #### Stop the components

     ```sh
     pkill -f 'airflow scheduler'
     pkill -f 'airflow webserver'
     pkill -f 'airflow worker' # If applicable
     ```

     #### Start the components

   ```sh
    airflow scheduler &
    airflow webserver &
    airflow worker & # If applicable
   ```

### **Note on Environment Variables:**

- Airflow configurations can also be set using environment variables in the
  format `AIRFLOW__{SECTION}__{KEY}`. For example, to set the `parallelism`
  parameter in the `[core]` section:

```bash
export AIRFLOW__CORE__PARALLELISM=10
```

- Hanges made via environment variables typically require restarting the affected
  Airflow components to take effect. citeturn0search1

**Special Considerations:**

Some configuration changes may not require a full restart. For instance,
certain settings can be updated without restarting the scheduler, depending on
the executor in use.However, to ensure all changes are applied consistently,
it's advisable to restart the relevant components after modifying
`airflow.cfg`.cite turn search

By following these steps, you can ensure that your Airflow instance operates with the updated configurations.
