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


Running

minikube start

kubectl create namespace pizzaapi

kubectl apply -f k8s/secrets.yaml -n pizzaapi

helm dependency update

pizzaapi