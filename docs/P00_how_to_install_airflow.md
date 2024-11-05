# HOW TO INSTALL APACHE AIRFLOW

Ensure that you have the environment variables as shown

- Observe that I am utilizing `.config` to store the config for `airflow` in the virtual machine.
- In case it is not utilized, the system's `airflow` will be used instead.
- Verify which `airflow` you are running by executing `which airflow`.
- The testing database will not be in production, and I am using `sqlite`, which can also be stored at `.config/airflow_database/`.

1. id -u `<username>`, and replace `<username>` with the actual username.

```sh

export AIRFLOW_UID=501
export AIRFLOW_VERSION=2.10.2
export PYTHON_VERSION=3.11
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
export AIRFLOW_HOME=$(pwd)
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:///$AIRFLOW_HOME/.config/airflow_database/airflow.db
export AIRFLOW_CONFIG=$(pwd)/.config/airflow.cfg
export AIRFLOW__CORE__LOAD_EXAMPLES='false'
export _AIRFLOW_WWW_USER_USERNAME="admin"
export _AIRFLOW_WWW_USER_PASSWORD="admin"

```

1. Install airflow using

```sh
mkdir -p .config/airflow_database
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

2. Activite the airflow

```sh
airflow db migrate

```

3. Define user name and password for the dag operations

```sh
airflow users create \
    --username admin \
    --firstname FIRST_NAME \
    --lastname LAST_NAME \
    --role Admin \
    --email admin@example.com
```

4. Activite the scheduler

```sh
airflow scheduler
```

5. Run the webserver

```sh

airflow webserver --port 9000
```

6. Modify the `config_airflow.`
