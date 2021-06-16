import sys
import json
from datetime import timedelta
from os.path import abspath
from os.path import dirname
from os.path import join

import airflow.contrib.operators.kubernetes_pod_operator
import pendulum

default_args = {
    "owner": "someone",
    "depends_on_past": False,
    "email": ["test@somesite.de"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

APP_ENV_VARS = {"key": "var", "env": "demo", (1, 2): [3, 4]}

app_environment = airflow.models.Variable.get("app_environment", default_var="dev")
log_environment = {"prod": "Production"}.get(app_environment, "Development")
default_log_level = {"prod": "INFO"}.get(app_environment, "INFO")
log_level = airflow.models.Variable.get("log_level", default_var=default_log_level)

default_args["start_date"] = pendulum.datetime(2021, 6, 16, 11, tz="UTC")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"handlers": ["console"], "level": log_level},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json", "level": log_level}},
    "formatters": {
        "json": {
            "()": "logmatic.JsonFormatter",
            "extra": {
                "environment": log_environment,
                "log_id": "{{ ti.dag_id }}-{{ ti.task_id }}-{{ ti.execution_date.strftime('%Y_%m_%dT%H_%M_%S_%f') }}-{{ ti.try_number }}",
            },
            "fmt": "%(asctime) %(name) %(processName) %(filename)  %(funcName) %(levelname) %(lineno) %(module) %(threadName) %(message) %(msg) %(args)",
        }
    },
}


def build_command_string(filename, content):
    return ["write", filename, "--content", content]

def build_environment():
    environment = APP_ENV_VARS
    environment["LOGGING_CONF"] = json.dumps(LOGGING)
    return environment


environment = build_environment()

with airflow.DAG(
    dag_id="test_dag",
    description="Some sample dag",
    default_args=default_args,
    schedule_interval="4/15 * * * *",
    catchup=True,
) as dag:
    x = [
        airflow.contrib.operators.kubernetes_pod_operator.KubernetesPodOperator(
            task_id="test_dag_first",
            arguments=build_command_string(
                "test_first_task",
                "Dummy data"
            ),
            retries=3,
            retry_delay=timedelta(seconds=10),
            sla=timedelta(minutes=5),
            execution_timeout=timedelta(minutes=5),
            # KubernetesPodOperator specific args
            name="test_dag_first",
            namespace="aif",
            startup_timeout_seconds=180,
            image="ilhnctn/python-cli:v1",
            is_delete_operator_pod=True,
            env_vars=environment,
            cmds=["write"],
        ),
        airflow.contrib.operators.kubernetes_pod_operator.KubernetesPodOperator(
            task_id="test_dag_first_derived",
            arguments=build_command_string(
                "test_second_task",
                "Another Content"
            ),
            name="test_dag_first_derived",
            namespace="aif",
            retries=3,
            retry_delay=timedelta(seconds=10),
            sla=timedelta(minutes=5),
            execution_timeout=timedelta(minutes=5),
            startup_timeout_seconds=180,
            image="ilhnctn/python-cli:v1",
            is_delete_operator_pod=True,
            env_vars=environment,
            cmds=["write"],
        ),
    ] >> airflow.contrib.operators.kubernetes_pod_operator.KubernetesPodOperator(
        task_id="create_callculation",
        name="create_callculation",
        namespace="aif",
        retries=1,
        arguments=build_command_string(
            "test_dag",
            "Last content"
        ),
        retry_delay=timedelta(seconds=10),
        sla=timedelta(minutes=9),
        execution_timeout=timedelta(minutes=9),
        startup_timeout_seconds=180,
        image="ilhnctn/python-cli:v1",
        is_delete_operator_pod=True,
        env_vars=environment,
        cmds=["write"],
        trigger_rule="all_done",
    )
