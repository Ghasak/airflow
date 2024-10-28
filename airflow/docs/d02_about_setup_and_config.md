# Preconfiguration and setup for DAG

## WORKING WITH AIRFLOW

The current cofigurations are located in the generated file called
`airflow.cfg` which is generated after installing and initializing the
`aifflow`.

1. Using the `Dag` location can be also alter to `src/main.py`, but currently I
   am using it for the directory `dags`, for experimenting.

```sh

[core]
# The folder where your airflow pipelines live, most likely a
# subfolder in a code repository. This path must be absolute.
#
# Variable: AIRFLOW__CORE__DAGS_FOLDER
#
dags_folder = /Users/gmbp/Desktop/devCode/pythonHub/airflow/dags
```

2. The following is for the database for storing all actrivities for the
   `Airflow`.

- You can use `postgres`, `mysql`, and currently I am using `sqlite`.

```sh
sql_alchemy_conn = sqlite:////Users/gmbp/Desktop/devCode/pythonHub/airflow/airflow.db
```

3. for The webserver_config I use the default

```sh

[webserver]
# The message displayed when a user attempts to execute actions beyond their authorised privileges.
#
# Variable: AIRFLOW__WEBSERVER__ACCESS_DENIED_MESSAGE
#
access_denied_message = Access is Denied

# Path of webserver config file used for configuring the webserver parameters
#
# Variable: AIRFLOW__WEBSERVER__CONFIG_FILE
#
config_file = /Users/gmbp/Desktop/devCode/pythonHub/airflow/webserver_config.py

# The base url of your website: Airflow cannot guess what domain or CNAME you are using.
# This is used to create links in the Log Url column in the Browse - Task Instances menu,
# as well as in any automated emails sent by Airflow that contain links to your webserver.
#
# Variable: AIRFLOW__WEBSERVER__BASE_URL
#
base_url = http://localhost:8080

# Default timezone to display all dates in the UI, can be UTC, system, or
# any IANA timezone string (e.g. **Europe/Amsterdam**). If left empty the
# default value of core/default_timezone will be used
#
# Example: default_ui_timezone = America/New_York
#
# Variable: AIRFLOW__WEBSERVER__DEFAULT_UI_TIMEZONE
#
default_ui_timezone = UTC

# The ip specified when starting the web server
#
# Variable: AIRFLOW__WEBSERVER__WEB_SERVER_HOST
#
web_server_host = 0.0.0.0

# The port on which to run the web server
#
# Variable: AIRFLOW__WEBSERVER__WEB_SERVER_PORT
#
web_server_port = 8080
```
