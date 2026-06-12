# Laravel DevOps Стек (Docker + Ansible)

Автоматическое развертывание Laravel + Nginx + MySQL + phpMyAdmin на чистом сервере Debian 11 с помощью Ansible.

## Стек технологий
* **Оркестрация:** Ansible
* **Контейнеризация:** Docker / Docker Compose
* **Сервисы:** Nginx (Reverse Proxy), PHP 8.3-FPM, MySQL 8.0, phpMyAdmin

## Быстрый запуск

### 1. Настройка конфигурации
Откройте `inventory.ini` в корне проекта и укажите IP вашего сервера, пользователя и путь к SSH-ключу:

```ini
[servers]
YOUR_SERVER_IP  # <-- Впишите IP сервера сюда

[servers:vars]
ansible_user=debian
ansible_ssh_private_key_file=~/.ssh/id_ed25519

2. Запуск развертывания
Выполните команду на локальной машине:

ansible-playbook -i inventory.ini playbook.yml

Плейбук автоматически обновит систему, установит Docker, развернет контейнеры, установит чистый Laravel, настроит права и применит миграции.
Доступ к веб-интерфейсам
После успешного завершения команды сервисы доступны по HTTP:
•	Laravel (Сайт): http://<IP_СЕРВЕРА>/ — Отвечает кодом 200 (Приветственная страница)
•	phpMyAdmin: http://<IP_СЕРВЕРА>/pma/
•	Пользователь: db
•	Пароль: dbpassword

Особенности реализации
•	Идемпотентность: Повторный запуск плейбука безопасен и не изменяет работающие конфигурации.
•	Автомиграции: Laravel дожидается полной готовности MySQL (через Docker healthcheck) и автоматически накатывает базу при старте.
•	Персистентность: Данные базы хранятся в named volume mysql_data и не теряются при docker compose down.
•	Права доступа: Автоматически выставлены права www-data на папки storage и bootstrap/cache во избежание ошибок Permission Denied.