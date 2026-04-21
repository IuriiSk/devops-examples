#!/bin/bash
# Установка NGINX Ingress Controller через Helm

# Добавляем репозиторий
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Устанавливаем с кастомными параметрами
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.replicaCount=2 \
  --set controller.resources.requests.cpu=100m \
  --set controller.resources.requests.memory=128Mi \
  --set controller.service.type=LoadBalancer \
  --set controller.metrics.enabled=true \
  --set controller.config.proxy-body-size="50m" \
  --set controller.config.log-format-upstream='{"time": "$time_iso8601", "remote_addr": "$remote_addr", "host": "$host", "request": "$request", "status": $status, "body_bytes_sent": $body_bytes_sent, "request_time": $request_time, "http_referrer": "$http_referer", "http_user_agent": "$http_user_agent"}'

# Проверяем установку
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

echo "✅ NGINX Ingress Controller установлен"