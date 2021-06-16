## Setup

Prepare docker image

```sh
docker build -t ilhnctn/python-cli:v1 .
docker push ilhnctn/python-cli:v1

```

### Deployment
```sh
helm repo add apache-airflow https://airflow.apache.org
helm repo update
kubectl create ns airflow
helm install -f values.yaml airflow apache-airflow/airflow --namespace airflow --debug

# Upgrade/changes
helm upgrade -f values.yaml airflow --namespace airflow --debug apache-airflow/airflow
```