#!/bin/bash
PROJECT_ID="my-gcp-project"
CLUSTER_NAME="prod-cluster"
ZONE="us-central1-a"

gcloud config set project $PROJECT_ID

gcloud container clusters create $CLUSTER_NAME \
  --zone $ZONE \
  --machine-type n1-standard-2 \
  --num-nodes 3 \
  --enable-autoscaling --min-nodes 2 --max-nodes 6 \
  --enable-network-policy \
  --enable-ip-alias

gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE

# Install NGINX Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.0/deploy/static/provider/cloud/deploy.yaml