# Airflow Up and Running

## My collected notes.

- It seems that if you want to use `Airflow` from the container based on a
  `docker` image. You will be stuck to the python inside the container itself.
- Therefore, if you want to run a `BashExecturator` you must provide first a
  way to map the volume to see the `src/main.py` file and all related files.
- Or you can use the `Airflow` image as a base to build on top of it to make
  python more controllable by providing the `requiremetns.txt` while building the
  image.
- You have to be careful about scheduling a task, you must be aware about the
  timezone when you schedule a task.
- It has been tested that for a local installation of `Airflow` with also
  `virtualenv` you can run all `bash` commands that you system is supporting,
  that includes `fzf`, `bat`, `pipenv` ..etc.

- Common practice for your workflow:
  - Either you specify the tasks as `ETL` then call the modules that you want
    and decorate them with `@taskx`.
    - This invovlve using the variable `dag_folder`,
      such as `dags_folder = ~/airflowHub/examples/dags`. in the `airflow.cfg`.
    - Then you use the pythonExcutor for running the tasks, you can change
      the `dag_folder` to `src/main.py` and write your tasks at the `main.py`
      file.
  - Or as I use always, run the full project at once from a starting point such
    as `src.main` using `pipenv run python -m src.main`.
    - This will require from you to run the full project by specifying the
      `Bashexecutor` and you must use the `cmd` keyword to sepfified the
      correct directory of your tasks starting point by providing the root
      directory to your project.

## CONSIDERATIONS

To apply changes made in the `airflow.cfg` file, it's generally necessary to
restart the relevant Airflow components, such as the scheduler, webserver, and
workers. This ensures that the updated configurations are loaded and take
effect.

**Steps to Apply Configuration Changes:**

1. **Modify `airflow.cfg`:**

   - Edit the `airflow.cfg` file located in your `AIRFLOW_HOME` directory to update the desired settings.

2. **Restart Airflow Components:**

   - After saving the changes, restart the Airflow components to apply the new
     configurations. The method to restart these components depends on how
     Airflow is deployed:

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




