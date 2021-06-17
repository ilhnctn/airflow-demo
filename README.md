## Motivation
This project intends to compare apache airflow deployment methods and give an idea about which method is better (cost & performance comparision later.)

Current Deployment Methods:
 - Helm Charts
   - [x] Official Chart ([here](https://github.com/apache/airflow/tree/main/chart))
   - [ ] Astronomer Chart ([here](https://github.com/astronomer/airflow-chart))
   - [ ] Community Chart ([here](https://github.com/airflow-helm/charts/tree/main/charts/airflow))
 - Docker Deployment
 - Dedicated VM deployment
 - Paid Subscriptions
   - GCP Composer
   - Astronomer

## Setup
Prepare docker image with sample python cli

```sh
docker build -t ilhnctn/python-cli:v1 .
docker push ilhnctn/python-cli:v1

```

### Helm Deployments
1. Official
```sh
helm repo add apache-airflow https://airflow.apache.org
helm repo update
kubectl create ns airflow
helm install -f values.yaml airflow apache-airflow/airflow --namespace airflow --debug

# Upgrade/changes
helm upgrade -f values.yaml airflow --namespace airflow --debug apache-airflow/airflow
```


## Healtcheck Cron
I plan to restart scheduler pod in case of long unavailabilities (like more than 2 minutes).
GCP side apparently needs some extra configurations for security issues.

Resources are listed here but will be cleaned later

```sh
# Build & push python image
docker build -f health.Dockerfile -t ilhnctn/scheduler-hc:v3 .
docker push ilhnctn/scheduler-hc:v3

# Change image version in k8s resource and apply the change
kubectl apply -f gcloud/airflow/official_rls/scheduler-health-cron.yaml

```