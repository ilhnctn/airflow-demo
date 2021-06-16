FROM python:3.9

ENV APP_USER=dag_user

RUN useradd --create-home --shell /bin/bash $APP_USER

USER $APP_USER

RUN pip install --no-cache-dir click pendulum
COPY ./cli.py /home/$APP_USER
WORKDIR /home/$APP_USER


ENTRYPOINT ["python", "cli.py"]
