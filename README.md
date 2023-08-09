Pizza Order API Helm Chart

This Helm chart is designed to deploy the Pizza Order API and associated components into a Kubernetes cluster. It includes configuration for the API itself, a queue worker, RabbitMQ, MongoDB, and associated scaling and routing settings.

Components
API: RESTful API for receiving and processing pizza orders.
Queue Worker: A worker that processes orders and adds them to a database.
RabbitMQ: Message broker for queuing orders.
MongoDB: Database for storing order information.
Horizontal Pod Autoscaler (HPA): Automatically scales the number of pods in a deployment.
Ingress: Routing configuration to expose the API locally.
Prerequisites
Kubernetes cluster (e.g., Minikube for local development)
Helm v3.x installed
Access to Docker Hub or another container registry if not using public images

Configuration
helm-charts/values.yaml

Installation
Using Helm CLI
Clone the repository.
https://github.com/yaront1111/HiredscoreHw.git

Navigate to the Helm chart directory.

Install the Helm chart with:

helm install my-release-name .


on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Helm
      uses: azure/setup-helm@v1
      with:
        version: '3.x'

    - name: Deploy with Helm
      run: |
        helm install my-release-name .
Make sure to adjust paths, chart names, and any necessary authentication for your specific registry or cluster.

Accessing the API
With a local Minikube setup and configured ingress, you can access the API at http://127.0.0.1.
