# Laravel DevOps Стек (Docker + Ansible)

Автоматическое развертывание Laravel + Nginx + MySQL + phpMyAdmin на чистом сервере Debian 11 с помощью Ansible.

## Стек технологий

* **Оркестрация:** Ansible
* **Контейнеризация:** Docker / Docker Compose
* **Сервисы:** Nginx (Reverse Proxy), PHP 8.4-FPM, MySQL 8.0, phpMyAdmin

## Быстрый запуск

### 1. Настройка конфигурации

Откройте `inventory.ini` в корне проекта и укажите параметры подключения к вашему серверу (IP, порт, пользователя и путь к приватному SSH-ключу):

```ini
[servers]
laravel-vm ansible_host=YOUR_SERVER_IP ansible_port=2222 

[servers:vars]
ansible_user=YOUR_SSH_USER
ansible_ssh_private_key_file=~/.ssh/YOUR_PRIVATE_KEY