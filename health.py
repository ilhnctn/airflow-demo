import os
from typing import Dict
from logging import getLogger

import requests
from requests.exceptions import HTTPError
from kubernetes import client, config


logger = getLogger(__name__)
url: str = os.environ.get(
    "AIRFLOW_HEALTH_ENDPOINT", "http://airflow-cr-web.airflow-community:8080/health"
)

CONNECT_TIMEOUT: int = 1
READ_TIMEOUT: int = 5


def handle_scheduler_not_ready_event(namespace: str = "airflow-community"):
    v1 = client.CoreV1Api()
    # Handle error here (restarting the scheduler is an option)


try:
    response = requests.get(url=url, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
except HTTPError as e:
    print(str(e))
    exit(1)
data = response.json()
scheduler_status = data["scheduler"]["status"]


if scheduler_status == "healthy":
    # logger.info("Everything is fine")
    print("Everything is fine")
elif scheduler_status == "unhealthy":
    logger.info("Hell")
    with open("stats.txt", "a") as f:
        w.write(data["scheduler"]["latest_scheduler_heartbeat"])
    handle_scheduler_not_ready_event()
