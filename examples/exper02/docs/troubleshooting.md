# AIRFLOW with DOCKER Compose

## Troubleshooting

1. Be careful
   Here’s the **full corrected code** for your `hello_airflow_dag_v2.py` to avoid the **duplicate DAG ID issue**:

---

### **How to Apply the Changes**

1. **Place the Modified DAG in the Correct Directory:**

   Ensure the updated DAG is placed in your mounted **DAGs directory**:

   ```
   ~/devCode/pythonHub/airflow_with_docker/airflow/dags/hello_airflow_dag_v2.py
   ```

2. **Remove the Old DAG File if Not Needed:**

   If the old DAG file is no longer needed, delete it:

   ```bash
   rm ~/Desktop/devCode/pythonHub/airflow_with_docker/airflow/dags/hello_airflow_dag.py
   ```

3. **Restart Airflow Scheduler and Webserver:**

   ```bash
   docker compose restart airflow-scheduler airflow-webserver
   ```

4. **Verify in Airflow UI:**

   - Open [http://localhost:8080](http://localhost:8080).
   - Ensure `hello_airflow_dag_v2` appears in the DAGs list.

5. **Check for Errors:**

   Use the following command to ensure there are no import errors:

   ```bash
   docker exec -it <scheduler_container_id> airflow dags list
   ```

---

This version ensures your DAG works properly by giving it a **unique
`dag_id`**. Restarting the scheduler and webserver after placing the new DAG
will allow Airflow to detect and execute it without conflicts. Let me know if
this resolves your issue!

## What I did - Fixed

```sh
╭─  gmbp 󰇄 GMacBookPro   ~/Desktop/devCode/pythonHub/airflow_with_docker/airflow                                    Sun.Oct.27th,2024- 8:14:53 PM ─╮
├─ 󰚩 INSERT 󰇎                                                                                                                                   ⏱ :0ms ─┤
╰─ docker container ls                                                                                                               󰒍  3.11.5 airflow ─╯
CONTAINER ID   IMAGE                   COMMAND                  CREATED ago          STATUS                    PORTS                    NAMES
f900c4579678   apache/airflow:2.10.2   "/usr/bin/dumb-init …"   24 minutes ago ago   Up 8 minutes (healthy)    8080/tcp                 airflow-airflow-worker-1
88e1e5936187   apache/airflow:2.10.2   "/usr/bin/dumb-init …"   24 minutes ago ago   Up 42 seconds (healthy)   8080/tcp                 airflow-airflow-scheduler-1
5f9e6a9d493e   apache/airflow:2.10.2   "/usr/bin/dumb-init …"   24 minutes ago ago   Up 8 minutes (healthy)    8080/tcp                 airflow-airflow-triggerer-1
af1dc078d1a3   apache/airflow:2.10.2   "/usr/bin/dumb-init …"   24 minutes ago ago   Up 41 seconds (healthy)   0.0.0.0:8080->8080/tcp   airflow-airflow-webserver-1
b1f29cba3bd4   redis:7.2-bookworm      "docker-entrypoint.s…"   42 minutes ago ago   Up 8 minutes (healthy)    6379/tcp                 airflow-redis-1
bb547eaa4117   postgres:13             "docker-entrypoint.s…"   42 minutes ago ago   Up 8 minutes (healthy)    5432/tcp                 airflow-postgres-1

╭─  gmbp 󰇄 GMacBookPro   ~/Desktop/devCode/pythonHub/airflow_with_docker/airflow                                                                                                                                                                                                 Sun.Oct.27th,2024- 8:15:03 PM ─╮
├─ 󰚩 INSERT 󰇊                                                                                                                                                                                                                                                                                                ⏱ :0ms ─┤
╰─ docker container exec -it 88e1e5936187 airflow dags list                                                                                                                                                                                                                                       󰒍  3.11.5 airflow ─╯
Error: Failed to load all files. For details, run `airflow dags list-import-errors`
dag_id            | fileloc                                | owners  | is_paused
==================+========================================+=========+==========
hello_airflow_dag | /opt/airflow/dags/hello_airflow_dag.py | airflow | False


╭─  gmbp 󰇄 GMacBookPro   ~/Desktop/devCode/pythonHub/airflow_with_docker/airflow                                                                                                                                                                                                 Sun.Oct.27th,2024- 8:15:38 PM ─╮
├─ 󰚩 INSERT 󰇎                                                                                                                                                                                                                                                                                                  ⏱ 2s ─┤
╰─ docker container exec -it 88e1e5936187 airflow dags list-import-errors                                                                                                                                                                                                                         󰒍  3.11.5 airflow ─╯
filepath                                  | error
==========================================+======================================================================================================================================================================
/opt/airflow/dags/hello_airflow_dag_v2.py | AirflowDagDuplicatedIdException: Ignoring DAG hello_airflow_dag from /opt/airflow/dags/hello_airflow_dag_v2.py - also found in /opt/airflow/dags/hello_airflow_dag.py


```

## More debugging

To make sure your **new DAG** (`hello_airflow_dag_v2.py`) is detected and correctly reflected in the Airflow UI while using **Docker Compose**, follow these steps:

---

### **Steps to Ensure New DAGs are Detected**

1. **Check the Scheduler's DAG Parsing Interval**:

   - By default, the **Airflow scheduler** checks the DAGs directory periodically. If your DAG does not appear immediately, it could be because of a delay in the parsing interval.
   - You can reduce this interval by setting the following environment variable in your `docker-compose.yaml`:
     ```yaml
     environment:
       AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL: 10
     ```
     This ensures that the scheduler checks for new DAGs every 10 seconds instead of the default setting, which might take longer.

2. **Restart the Scheduler**:

   - If the DAG still doesn’t appear, **restart the scheduler and webserver** to ensure they reload the DAGs:
     ```bash
     docker compose restart airflow-scheduler airflow-webserver
     ```

3. **Check for Syntax Errors or DAG Import Issues**:

   - Airflow can silently skip a DAG if there are **syntax errors** or other issues with the file. Verify that your DAG has no import errors by using:
     ```bash
     docker exec -it <scheduler_container_id> airflow dags list
     ```
   - If the DAG appears here but not in the UI, check the **DAG Import Errors** section under **Browse > DAG Import Errors** in the Airflow UI.

4. **Verify the DAG File is in the Correct Directory**:

   - Ensure that the **DAG file** is placed in the correct **mounted directory** (`dags/`). Inside the webserver container, you can verify it by running:
     ```bash
     docker exec -it <webserver_container_id> ls /opt/airflow/dags
     ```
     If the file doesn’t appear, there might be an issue with the **volume mount** in `docker-compose.yaml`.

5. **Try Manually Triggering a DAG**:
   - Sometimes, the DAG might be detected but in a **paused** state by default.
     Go to the Airflow UI, click on the **DAG toggle** to unpause it, and
     **trigger the DAG manually** to verify it works.

---

### **When to Rebuild the Docker Image**

In general, you **don't need to rebuild the entire Docker image** each time you
add a new DAG. However, if you’re making structural changes to how DAGs are
handled (like adding packages or changing mounted directories), you may need
to:

1. Update the `docker-compose.yaml`.
2. Run:
   ```bash
   docker compose build
   docker compose up -d
   ```

Using the above steps, you should be able to see your DAGs in the Airflow UI
without rebuilding the Docker container every time. If issues persist, consider
adjusting the **parsing intervals** and double-checking any import errors
through the CLI and the Airflow UI logs. This should streamline the process and
ensure your DAGs are detected correctly.

## What is the differences?

The commands you are asking about:

1. **`docker compose restart airflow-scheduler airflow-webserver`**
2. **`docker compose restart`**

Both serve to **restart services** within your Docker Compose setup, but there are **key differences** between them.

---

### **1. Command: `docker compose restart airflow-scheduler airflow-webserver`**

- **What it Does**:

  - This command **restarts only the specified services** (in this case, `airflow-scheduler` and `airflow-webserver`).
  - It **stops and immediately starts** these specific services without affecting others (e.g., the **database, Redis**, or **worker containers**).

- **Why You Need It**:
  - Use this when:
    - You’ve made changes to DAGs, and the **scheduler is not detecting them**.
    - The Airflow **UI isn’t showing updates** or becomes unresponsive.
    - You want to **reload configurations** related to scheduling or webserver behavior without disrupting the entire stack (e.g., Postgres).

---

### **2. Command: `docker compose restart`**

- **What it Does**:

  - This command **restarts all the services** defined in your `docker-compose.yaml`.
  - It affects all services, including **PostgreSQL, Redis, Airflow scheduler, webserver, and workers**.

- **When to Use**:
  - Use this when:
    - **Multiple services are unresponsive** or not behaving as expected.
    - You need to ensure that **everything is reset** and synchronized properly.
    - There are **dependencies between services** that require a clean restart (e.g., Redis messaging for workers).

---

### **Key Differences**

| **Command**                                                  | **Purpose**                                                   | **Impact**                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------- | --------------------------------------------------------- |
| `docker compose restart airflow-scheduler airflow-webserver` | Restart only the specified services (scheduler and webserver) | Minimal impact; other services keep running               |
| `docker compose restart`                                     | Restart **all services** defined in `docker-compose.yaml`     | Stops and starts everything, including database and cache |

---

### **Which Command Should You Use?**

- **Use `docker compose restart airflow-scheduler airflow-webserver`** if:

  - The **scheduler** or **webserver** is not reflecting changes (e.g., new DAGs or UI updates).
  - You want **minimal disruption** and only need to reset the scheduling or webserver layer.

- **Use `docker compose restart`** if:
  - **Multiple services** are not functioning correctly (e.g., the database isn’t reachable or Redis messaging fails).
  - You’ve made configuration changes that affect the entire stack.

---

This approach helps you **target specific services** when needed, while also
providing an option to reset everything in case of larger issues.

