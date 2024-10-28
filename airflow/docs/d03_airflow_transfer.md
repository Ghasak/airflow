# How to transfer Airflow

## Steps and configurations

1. Use the `Pipfile.lock` and then install it using

```sh
pipenv install --ignore-pipfile

```

2. Now, after finish install all the dependencies, you will need to load the
   environment variables using the `.envrc` with `direnv`. Put it in your
   project directory.

3. Initilize the airflow dependencies after creating a `database` and `dags`
   directory in your project root directory.

```sh
mkdir dags database
```

4. Now Initilize

```sh
airflow db migrate
```

5. Pass the credentials to airflow using

```sh
airflow users create \
--username admin \
--firstname Admin \
--lastname User \
--role Admin \
--email admin@example.org
```

6. Now, lets work with the `scheduler`.

```sh
airflow scheduler
```

7. Also, we need to run the server

```sh
airflow webserver --port 8080
```

8. Optional: Debug Logs and Tasks
   To view logs for a specific task or troubleshoot:

```bash
airflow tasks logs <dag_id> <task_id> <execution_date>
```

Use airflow dags list to list all DAGs and airflow dags trigger <dag_id> to
trigger a DAG manually.

9. Restart Airflow Services If the scheduler or webserver was running, stop
   them:

```sh
ps aux | grep airflow # Find PIDs
kill -9 <PID>
```
