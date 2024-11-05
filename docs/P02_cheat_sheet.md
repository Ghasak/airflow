# CheetSheet for AIRFLOW

Here are some useful Airflow CLI commands to help you manage and monitor your Airflow environment from the terminal:

Certainly! Here’s a summarized table of useful Airflow commands that you can use as a quick-reference cheat sheet:

| **Category**              | **Command**                                                                    | **Description**                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| **DAG Management**        | `airflow dags list`                                                            | List all available DAGs and their statuses.                                                       |
|                           | `airflow dags trigger <dag_id>`                                                | Trigger a DAG run immediately.                                                                    |
|                           | `airflow dags trigger <dag_id> --run-id <custom_run_id>`                       | Trigger a DAG run with a custom `run_id`.                                                         |
|                           | `airflow dags list-runs -d <dag_id>`                                           | List all runs for a specific DAG, showing status, start time, and end time.                       |
|                           | `airflow dags pause <dag_id>`                                                  | Pause a DAG (stops automatic scheduling).                                                         |
|                           | `airflow dags unpause <dag_id>`                                                | Unpause a DAG (resumes automatic scheduling).                                                     |
|                           | `airflow dags state <dag_id> <execution_date>`                                 | Check the status of a DAG run for a specific execution date.                                      |
| **Task Management**       | `airflow tasks list <dag_id>`                                                  | List all tasks in a specified DAG.                                                                |
|                           | `airflow tasks run <dag_id> <task_id> <execution_date>`                        | Run a specific task in a DAG manually.                                                            |
|                           | `airflow tasks logs <dag_id> <task_id> <execution_date>`                       | View logs for a specific task instance.                                                           |
|                           | `airflow tasks state <dag_id> <task_id> <execution_date>`                      | Check the status of a specific task instance.                                                     |
|                           | `airflow tasks clear <dag_id> --start-date <start_date> --end-date <end_date>` | Clear/reset task instances in a DAG within a date range.                                          |
| **Database Maintenance**  | `airflow db cleanup`                                                           | Clean up old metadata, logs, and task instances based on retention policy.                        |
| **Scheduler & Webserver** | `airflow scheduler -l`                                                         | Run the scheduler in the foreground with logging enabled (for debugging).                         |
|                           | `airflow webserver -p 8080`                                                    | Start the webserver on port 8080.                                                                 |
|                           | `airflow webserver`                                                            | Start the webserver with default settings (port 8080).                                            |
| **Configuration & Debug** | `airflow config list`                                                          | Display the current Airflow configurations.                                                       |
|                           | `airflow <command> --help`                                                     | Get help for any specific command (replace `<command>` with any command, like `dags` or `tasks`). |
| **Exporting Metadata**    | `airflow dags list --output json > dag_list.json`                              | Export a list of all DAGs to a JSON file.                                                         |

This table should give you a handy, at-a-glance reference for managing Airflow tasks, DAGs, and configurations. Let me know if you need more specific commands added!

### 1. **Triggering and Managing DAG Runs**

- **Trigger a DAG run**:

  ```bash
  airflow dags trigger <dag_id>
  ```

  Triggers a DAG immediately. You can specify a custom `run_id` if needed:

  ```bash
  airflow dags trigger <dag_id> --run-id <custom_run_id>
  ```

- **List all DAGs**:

  ```bash
  airflow dags list
  ```

  Displays all available DAGs with their statuses.

- **List all runs for a DAG**:

  ```bash
  airflow dags list-runs -d <dag_id>
  ```

  Shows the status, start time, and end time for each run of the specified DAG.

- **Pause/Unpause a DAG**:
  ```bash
  airflow dags pause <dag_id>
  airflow dags unpause <dag_id>
  ```
  Pausing a DAG stops it from scheduling automatically, but you can still trigger it manually.

### 2. **Managing and Tracking Task Instances**

- **List tasks in a DAG**:

  ```bash
  airflow tasks list <dag_id>
  ```

  Displays all tasks in a specified DAG with their details.

- **Run a specific task in a DAG**:

  ```bash
  airflow tasks run <dag_id> <task_id> <execution_date>
  ```

  Executes a single task instance. Replace `<execution_date>` with a timestamp like `2024-11-05T00:00:00+00:00`.

- **View logs for a specific task instance**:
  ```bash
  airflow tasks logs <dag_id> <task_id> <execution_date>
  ```
  Shows the logs for the specified task run.

### 3. **Checking Statuses and Logs**

- **Check status of DAG runs**:

  ```bash
  airflow dags state <dag_id> <execution_date>
  ```

  Shows the status of a DAG run at a specific execution date.

- **Check status of a task**:
  ```bash
  airflow tasks state <dag_id> <task_id> <execution_date>
  ```
  Displays the current status of a specific task instance.

### 4. **Database Maintenance and Cleanup**

- **Clear task instances for a DAG**:

  ```bash
  airflow tasks clear <dag_id> --start-date <start_date> --end-date <end_date>
  ```

  Clears (resets) the state of tasks in a DAG for the specified date range. Useful for rerunning tasks after fixing issues.

- **Database cleanup**:
  ```bash
  airflow db cleanup
  ```
  Cleans up old metadata, logs, and task instances based on the retention policy set in `airflow.cfg`. Useful for managing database size.

### 5. **Monitoring Scheduler and Webserver**

- **Check status of the scheduler**:

  ```bash
  airflow scheduler -l
  ```

  Runs the scheduler in the foreground with logging enabled (useful for debugging). To check the scheduler's status when it’s running as a service, look for its process using `ps` or other system monitoring tools.

- **Stop and Start the Webserver**:
  ```bash
  airflow webserver -p 8080
  ```
  Starts the webserver on port 8080. You can stop it by finding the process ID and killing it or by using `systemctl` if running as a service.

### 6. **Exporting and Importing DAGs**

- **Export the list of all DAGs**:
  ```bash
  airflow dags list --output json > dag_list.json
  ```
  Exports DAG metadata to a JSON file, useful for tracking DAGs across environments.

### 7. **Additional Information and Help**

- **Display Airflow configurations**:

  ```bash
  airflow config list
  ```

  Shows the current configuration for Airflow.

- **Get CLI help for any command**:
  ```bash
  airflow <command> --help
  ```
  Replace `<command>` with any Airflow command (like `dags` or `tasks`) to see all options and parameters for that command.

---

These commands should help you manage Airflow more effectively from the terminal, from scheduling and monitoring to debugging and cleaning up. Let me know if you need further assistance with any specific command!
