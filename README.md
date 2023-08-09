
# Pizza Order API

This Helm chart is designed to deploy the Pizza Order API and associated components into a Kubernetes cluster.
It includes configuration for the API itself, a queue worker, RabbitMQ, MongoDB, and associated scaling and routing settings.


## Features

- API: RESTful API for receiving and processing pizza orders.
- Queue Worker: A worker that processes orders and adds them to a database.
- RabbitMQ: Message broker for queuing orders.
- MongoDB: Database for storing order information.
- helmchart deployment
- github action docker build
- Horizontal Pod Autoscaler (HPA): Automatically scales the number of pods in a deployment.
- Ingress: Routing configuration to expose the API locally.
- Token helper


## Run Locally

Clone the project

```bash
  minikube start
  git clone https://github.com/yaront1111/HiredscoreHw.git
```

Go to the project directory

```bash
  cd HiredscoreHw/helm-charts
```
run Helm deployement
```bash
  kubectl create namespace pizzaapi
  kubectl apply -f templates/secrets.yaml -n pizzaapi
  helm install pizza-ordering . -n pizzaapi
```

use api

```bash
  minikube service api --url -n pizzaapi

```

GET <seriveip>:<serviceport>/health
