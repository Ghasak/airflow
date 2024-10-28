# STARTING POINT WITH AIRFLOW

## Install

The issue you encountered with installing Apache Airflow 2.10.2 on your Mac M1
may stem from Python version incompatibilities or dependency constraints.
Here’s how you can resolve it:

1. **Ensure Compatible Python Version:** Apache Airflow 2.10.2 works best with
   Python 3.8, 3.9, 3.10, or 3.11. Verify your Python version with:

   ```bash
   python --version
   ```

   If you don't have the required version, install it via Homebrew:

   ```bash
   brew install python@3.9
   ```

2. **Use a Virtual Environment:** Create a virtual environment to isolate dependencies:

   ```bash
   python3 -m venv airflow_venv
   source airflow_venv/bin/activate
   ```

3. **Correct Constraint File:** Ensure the constraint file matches your Python
   version. Adjust the constraint URL if needed:

   ```bash
   pip install 'apache-airflow==2.10.2' \
   --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.9.txt"
   ```

   Replace `3.9` in the URL with the version of Python you are using.

4. **Handle Dependency Conflicts:** If you still encounter dependency issues,
   try using Airflow’s `extras` installation, which ensures all required
   dependencies are properly installed:

   ```bash
   pip install 'apache-airflow[async,postgres,google]==2.10.2' \
   --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.9.txt"
   ```

5. **Initialize the Database:** After installation, run:
   ```bash
   airflow db init
   ```

This approach should address most dependency and constraint-related issues on
macOS M1 systems. If further conflicts arise, ensure your `pip` installation is
up-to-date (`pip install --upgrade pip`) and consult the [official Airflow
documentation](https://airflow.apache.org) for troubleshooting tips.
Additionally, using Docker can offer an alternative way to run Airflow in an
isolated environment if native installation issues
persist【6†source】【7†source】【8†source】.

## STARTING POINT - AIRFLOW

Now that Apache Airflow is installed, here are the necessary commands to get it
fully up and running, including setting up the web server, scheduler, and
creating the necessary database and user:

### 1. **Set Airflow Home Directory (Optional)**

If you want to define a specific directory for Airflow:

```bash
export AIRFLOW_HOME=~/airflow
```

### 2. **Initialize the Database**

Airflow requires a database to track tasks and DAGs. By default, it uses SQLite.

```bash
airflow db init
```

### 3. **Create an Admin User**

This step is required to access the Airflow web interface.

```bash
airflow users create \
--username admin \
--firstname FIRST_NAME \
--lastname LAST_NAME \
--role Admin \
--email admin@example.org
```

### 4. **Start the Scheduler**

The scheduler continuously monitors DAGs and triggers tasks as needed.

```bash
airflow scheduler
```

### 5. **Start the Web Server**

Launch the web server on port 8080 (or another port if preferred).

```bash
airflow webserver --port 8080
```

After this, you can access the web interface at `http://localhost:8080`.

### 6. **Run Airflow in Standalone Mode (Optional)**

For a quick setup with the database, web server, and scheduler running in one process:

```bash
airflow standalone
```

### 7. **Trigger a DAG Manually**

If you want to trigger a DAG (Direct Acyclic Graph) immediately:

```bash
airflow dags trigger <dag_id>
```

### 8. **Pause or Unpause a DAG**

To control whether a DAG is active:

```bash
airflow dags pause <dag_id>
airflow dags unpause <dag_id>
```

### 9. **View Logs**

To check logs for specific tasks:

```bash
airflow tasks logs <dag_id> <task_id> <execution_date>
```

### 10. **Stop the Services**

Use the following to stop the web server or scheduler (find the process ID):

```bash
ps aux | grep airflow  # Find the relevant PID
kill -9 <PID>
```

These commands should allow you to fully control Airflow on your system【7†source】【8†source】.
