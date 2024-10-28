# CONFIGURATION

You can provide a **root directory** via an environment variable and
reference it dynamically within `airflow.cfg` when initializing the database or
configuring Airflow 2.10.2. Here’s how you can achieve this:

---

### **1. Define a Root Directory via Environment Variable**

You can export a **`PROJECT_HOME`** or **`AIRFLOW_ROOT`** directory environment
variable to act as the base path.

```sh
export PROJECT_HOME=$(pwd)  # or your desired path
export AIRFLOW_HOME=$PROJECT_HOME/airflow  # Ensure Airflow paths align
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:///$PROJECT_HOME/database/airflow.db
```

After defining these, reload your environment (if using `direnv`):

```sh
direnv allow
```

---

### **2. Generate a Customized `airflow.cfg`**

When you initialize the Airflow database using:

```sh
airflow db init
```

Airflow will generate a new `airflow.cfg` within the `AIRFLOW_HOME` directory.
The database connection URL will be set based on the value in the environment
variable.

---

### **3. Modify `airflow.cfg` with Environment Variables**

If you want more flexibility (e.g., embedding variables directly inside
`airflow.cfg`), you can reference environment variables within the
configuration file by using **Jinja-style templating**.

Example of how to use it inside `airflow.cfg`:

```ini
[core]
dags_folder = {{ var.value.get('PROJECT_HOME') }}/dags
base_log_folder = {{ var.value.get('PROJECT_HOME') }}/logs

[database]
sql_alchemy_conn = {{ var.value.get('AIRFLOW__DATABASE__SQL_ALCHEMY_CONN') }}
```

To use this dynamic template, you may need a **startup script** that renders it
before starting Airflow. However, the simplest approach is to use environment
variables directly through:

```sh
export AIRFLOW__CORE__DAGS_FOLDER=$PROJECT_HOME/src
export AIRFLOW__LOGGING__BASE_LOG_FOLDER=$PROJECT_HOME/logs
```

---

### **4. Upgrade Your Airflow Setup**

To ensure you're following best practices for production and have the latest
improvements from **Airflow 2.10.2**, install the necessary components:

1. **Upgrade Airflow** and ensure dependencies are aligned:

   ```sh
   pip install --upgrade apache-airflow==2.10.2 apache-airflow-providers-postgres redis
   ```

2. **Configure Production-Ready Components:**
   Set up **PostgreSQL** and **Redis** as described earlier for your database and Celery backend.

3. **Initialize the Database with the Updated Config:**

   ```sh
   airflow db init
   ```

4. **Restart the Services:**
   Run your web server, scheduler, and workers to ensure everything is in sync.

---

### **Conclusion**

By setting `PROJECT_HOME` and other key paths via environment variables, you
can manage your Airflow project more flexibly, with paths properly resolved
during initialization. This setup ensures that your configuration works
consistently in **both development and production** environments.
