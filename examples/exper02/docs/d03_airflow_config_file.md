# AIRFLOW CONFIG file

What we need is a way to use the presistent configurations on our root directory and we can get it from container.

```sh
instruct me how to see the original airflow.cfg using the docker container with bash
then how to expose it to my project this file given that I have
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
  user: "${AIRFLOW_UID:-50000}:0"
in my current project that can be presistence
I wish to make it in config directory
```

Here’s how you can **access the original `airflow.cfg`** inside the Airflow Docker container and **persist it to your project’s `config/` directory**.

---

### **Step 1: Open a Bash Shell Inside the Container**

1. **List the Running Containers**:

   ```bash
   docker ps
   ```

2. **Find the `airflow-webserver` Container ID** (or any container running Airflow).

3. **Access the Container's Shell**:
   ```bash
   docker exec -it <container_id> /bin/bash
   ```

---

### **Step 2: Locate the `airflow.cfg` File Inside the Container**

Once inside the container, **navigate to the `airflow.cfg` file**:

```bash
cat /opt/airflow/airflow.cfg
```

This command will display the contents of the **default Airflow configuration file** used by the container.

---

### **Step 3: Copy `airflow.cfg` from the Container to the Host Machine**

Now, **exit the container** and copy the `airflow.cfg` to your host machine's **`config/` directory**.

1. **Create the `config/` Directory on Your Host Machine (if not already present)**:

   ```bash
   mkdir -p /Users/gmbp/Desktop/devCode/pythonHub/airflow_with_docker/config
   ```

2. **Copy the Configuration File from the Container**:

   ```bash
   docker cp <container_id>:/opt/airflow/airflow.cfg ~/Desktop/devCode/pythonHub/airflow_with_docker/config/airflow.cfg
   ```

   if you inside the root directory of your project you can use only

   ```sh
   docker cp <container_id>:/opt/airflow/airflow.cfg ./config/airflow.cfg
   ```

This command will copy the original `airflow.cfg` from the container to your **host machine**.

---

### **Step 4: Modify `docker-compose.yaml` to Persist the Configuration**

To ensure your custom `airflow.cfg` is used going forward, **mount the `config/` directory** in `docker-compose.yaml`:

```yaml
services:
  airflow-webserver:
    volumes:
      - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
      - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
      - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
      - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    environment:
      AIRFLOW_CONFIG: /opt/airflow/config/airflow.cfg
  airflow-scheduler:
    volumes:
      - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
      - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
      - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
      - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    environment:
      AIRFLOW_CONFIG: /opt/airflow/config/airflow.cfg
  user: "${AIRFLOW_UID:-50000}:0"
```

At this step, what I ended up doing is just uncomment the following `yaml` file
from the `docker_compose.yaml`, which works perfectly instead of the `Step 4`
above.

```sh
    AIRFLOW_CONFIG: '/opt/airflow/config/airflow.cfg'
```

- ***

### **Step 5: Restart Airflow Services**

After making these changes, **restart the Airflow services** to ensure they use
your custom configuration:

```bash
docker compose down
docker compose up -d
```

---

### **Step 6: Verify the Changes**

1. **Check that Airflow is using your custom configuration**:

   - Open the Airflow UI at [http://localhost:8080](http://localhost:8080).
   - Verify that the changes you made in `airflow.cfg` (e.g., disabling example DAGs) are applied.

2. **Inspect the Configuration**:
   You can also enter the container and confirm that the mounted config is used:
   ```bash
   docker exec -it <container_id> cat /opt/airflow/config/airflow.cfg
   ```

---

### **Summary**

By following these steps, you:

1. Accessed the original `airflow.cfg` from the container.
2. Persisted it to your project directory (`config/`).
3. Updated the `docker-compose.yaml` to use the custom configuration file.

This setup ensures that all configuration changes are **persistent** across container restarts.

## Priority of configurations

```sh
in this config for airflow.cfg
I have for example
sql_alchemy_conn = sqlite:////opt/airflow/airflow.db

for the database, while the docker-compose ensure to use postgres
which one will be installed and used in that case?
```

In your current setup, you have **conflicting database configurations**. The Airflow configuration file (`airflow.cfg`) specifies:

```
sql_alchemy_conn = sqlite:////opt/airflow/airflow.db
```

However, your **`docker-compose.yaml`** is configured to use **PostgreSQL** as the backend database.

---

### **Which Database Will Be Used?**

1. **PostgreSQL from `docker-compose.yaml` Should Take Priority**:

   - If the **Docker container environment** specifies a **PostgreSQL
     database** (via environment variables or mounted configs), it will
     **override the settings** in the default `airflow.cfg`.

2. **How Airflow Prioritizes Configuration**:

   - Airflow follows a **priority order** for configurations:
     1. **Environment variables** take the highest precedence.
     2. **Settings in `airflow.cfg`** (if not overridden by environment variables).
     3. **Airflow's default settings** (fallback if nothing is set).

3. **Example from Your Setup**:

   - If the `docker-compose.yaml` defines the `sql_alchemy_conn` environment variable, such as:
     ```yaml
     environment:
       AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
     ```
   - This environment variable will override the value in `airflow.cfg` (`sqlite:////opt/airflow/airflow.db`).

4. **Verify Active Configuration**:
   - To check which database is in use, you can run the following inside the **scheduler container**:
     ```bash
     docker exec -it <scheduler_container_id> airflow config get-value database sql_alchemy_conn
     ```
   - If the output shows PostgreSQL (`postgresql+psycopg2://...`), it confirms that the **environment variable is taking precedence**.

---

### **What Happens if There’s a Conflict?**

If you don't explicitly set the **PostgreSQL connection** in the environment
variables, Airflow will fall back to **SQLite**, as defined in `airflow.cfg`.
However, **SQLite is not suitable for production** and may cause issues with
concurrency.

---

### **Recommended Fix**

Ensure your `docker-compose.yaml` includes the following under the **webserver
and scheduler services** to guarantee PostgreSQL is used:

```yaml
environment:
  AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
```

This ensures that the **PostgreSQL backend** is used consistently across your services.

---

### **Conclusion**

- If properly configured, the **PostgreSQL backend defined in
  `docker-compose.yaml`** will take precedence over the **SQLite setting in
  `airflow.cfg`**.
- Always verify your **database configuration** using the Airflow CLI inside
  your containers to avoid conflicts. This ensures that Airflow is running in a
  **stable, production-ready environment**【84†source】.
