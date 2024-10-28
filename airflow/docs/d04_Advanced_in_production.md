# ADVANCED TOPICS FOR PRODUCTION

This will fix the production warning messages which come from two sources. From
the `Webserver` and one from the `Airflow`.

- Message in the webserver
- Message with the UI of AIRFLOW

<!-- vim-markdown-toc Marked -->

* [WARNING from the UI](#warning-from-the-ui)
    * [**1. Replace SQLite with PostgreSQL (Recommended) or MySQL**](#**1.-replace-sqlite-with-postgresql-(recommended)-or-mysql**)
        * [**Set up PostgreSQL Database**](#**set-up-postgresql-database**)
    * [**2. Configure the Executor for Production**](#**2.-configure-the-executor-for-production**)
        * [**Option A: LocalExecutor (Simple Setup)**](#**option-a:-localexecutor-(simple-setup)**)
        * [**Option B: CeleryExecutor (Distributed Execution)**](#**option-b:-celeryexecutor-(distributed-execution)**)
    * [**3. Monitoring and Optimization**](#**3.-monitoring-and-optimization**)
    * [**Conclusion**](#**conclusion**)
* [Warning with the Websever](#warning-with-the-websever)
    * [**1. Install Redis as a Storage Backend**](#**1.-install-redis-as-a-storage-backend**)
    * [**2. Configure Redis Backend for Flask-Limiter**](#**2.-configure-redis-backend-for-flask-limiter**)
    * [**3. Verify Redis Setup**](#**3.-verify-redis-setup**)
    * [**Alternative Storage Options**](#**alternative-storage-options**)

<!-- vim-markdown-toc -->


## WARNING from the UI

To make your **Airflow setup production-ready**, you need to address both the
**database backend** and **executor configuration**. Below are detailed steps
to transition your environment to a production setup.

---

### **1. Replace SQLite with PostgreSQL (Recommended) or MySQL**

SQLite is not suitable for production as it lacks concurrency and scalability.
Using **PostgreSQL** is highly recommended for production deployments.

#### **Set up PostgreSQL Database**

1. **Install PostgreSQL:**
   On macOS, you can use Homebrew:

   ```bash
   brew install postgresql
   brew services start postgresql
   ```

2. **Create a PostgreSQL Database and User:**

   ```bash
   psql postgres
   CREATE DATABASE airflow;
   CREATE USER airflow WITH PASSWORD 'yourpassword';
   ALTER ROLE airflow SET client_encoding TO 'utf8';
   ALTER ROLE airflow SET default_transaction_isolation TO 'read committed';
   ALTER ROLE airflow SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
   \q
   ```

3. **Update Airflow Configuration:**
   In your `.envrc` or `airflow.cfg`, set the PostgreSQL connection string:

   **`.envrc`:**

   ```bash
   export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:yourpassword@localhost/airflow
   ```

   Reload it:

   ```bash
   direnv allow
   ```

4. **Install PostgreSQL Dependencies:**
   Ensure your Airflow installation includes the PostgreSQL provider:

   ```bash
   pip install apache-airflow-providers-postgres
   ```

5. **Reinitialize the Airflow Database:**
   After configuring the database, run:
   ```bash
   airflow db init
   ```

---

### **2. Configure the Executor for Production**

The default **SequentialExecutor** is designed for development and testing,
running tasks sequentially. For production, use **LocalExecutor** or
**CeleryExecutor**.

#### **Option A: LocalExecutor (Simple Setup)**

This allows concurrent task execution on a single machine.

1. **Update `airflow.cfg`:**

   ```ini
   [core]
   executor = LocalExecutor
   ```

2. **Restart Airflow Services:**
   ```bash
   airflow scheduler &
   airflow webserver --port 8080 &
   ```

#### **Option B: CeleryExecutor (Distributed Execution)**

This setup is more complex and suitable for larger deployments with distributed workers.

1. **Install Redis:**
   Redis is required for message brokering:

   ```bash
   brew install redis
   brew services start redis
   ```

2. **Configure `airflow.cfg` for CeleryExecutor:**

   ```ini
   [core]
   executor = CeleryExecutor

   [celery]
   broker_url = redis://localhost:6379/0
   result_backend = postgresql+psycopg2://airflow:yourpassword@localhost/airflow
   ```

3. **Install Required Dependencies:**

   ```bash
   pip install apache-airflow[celery] redis apache-airflow-providers-postgres
   ```

4. **Start Redis, Scheduler, Web Server, and Workers:**
   - **Redis:** Already running via Homebrew.
   - **Scheduler:**
     ```bash
     airflow scheduler &
     ```
   - **Web Server:**
     ```bash
     airflow webserver --port 8080 &
     ```
   - **Worker:**
     ```bash
     airflow celery worker &
     ```

---

### **3. Monitoring and Optimization**

- **Set up logging:** Ensure your `logs/` directory is properly configured to
capture all Airflow logs.
- **Add a robust database backend:** Consider scaling PostgreSQL or switching
to managed solutions like AWS RDS for better reliability.
- **Configure resource limits:** Monitor the memory and CPU usage, especially
if using CeleryExecutor with multiple workers.

---

### **Conclusion**

This setup ensures your Airflow environment is ready for production with a
robust **PostgreSQL backend** and either **LocalExecutor** or
**CeleryExecutor** for efficient task scheduling. The CeleryExecutor is more
complex but better suited for large-scale deployments with distributed task
execution【6†source】【7†source】【8†source】.


## Warning with the Websever

The warning you're encountering suggests that **Flask-Limiter** is using an
**in-memory storage** for tracking rate limits, which is not recommended for
production. In production environments, in-memory storage can be problematic
because:

- **Rate limits won’t persist** across restarts or if multiple processes are
used.
- **Distributed systems** require external storage like Redis to properly
synchronize state.

Here’s how you can resolve it:

---

### **1. Install Redis as a Storage Backend**

Since Redis is often used with Flask and Celery, you can reuse it for rate limiting.

1. **Install Redis:**
   On macOS:
   ```bash
   brew install redis
   brew services start redis
   ```

2. **Install Redis Dependencies for Flask-Limiter:**
   ```bash
   pip install redis flask-limiter[redis]
   ```

---

### **2. Configure Redis Backend for Flask-Limiter**

Update your **Airflow configuration or Flask application** to point to Redis
for rate limit storage. Add the following to your `airflow.cfg` or your Flask
app configuration file:

```ini
[flask_limiter]
RATELIMIT_STORAGE_URL = redis://localhost:6379/0
```

Or in your **Python Flask app**:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

app = Flask(__name__)
redis_client = Redis(host='localhost', port=6379)

limiter = Limiter(
    get_remote_address,
    storage_uri="redis://localhost:6379/0",
    app=app,
)
```

---

### **3. Verify Redis Setup**

Restart all services (e.g., Redis, Airflow webserver, scheduler) and check if
the warning persists. You can also monitor Redis to ensure connections are
established properly:

```bash
redis-cli ping
```

---

### **Alternative Storage Options**
If Redis is not suitable for your setup, **other storage backends** like
Memcached or MongoDB can also be configured. See the Flask-Limiter
documentation for [more storage
options](https://flask-limiter.readthedocs.io#configuring-a-storage-backend).

---

This change ensures proper **rate limiting** in your production environment,
preventing potential bottlenecks or abuse.


