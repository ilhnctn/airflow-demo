FROM python:3.9

ENV APP_USER=health
ENV AIRFLOW_HEALTH_ENDPOINT=http://airflow-cr-web.airflow-community:8080/health

RUN useradd --create-home --shell /bin/bash $APP_USER

USER $APP_USER

RUN pip install --no-cache-dir requests kubernetes
COPY ./health.py /home/$APP_USER
WORKDIR /home/$APP_USER


ENTRYPOINT ["python", "health.py"]
