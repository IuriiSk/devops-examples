FROM python:3.11

WORKDIR /app

# зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# весь код сервиса
COPY . .

# запуск
CMD ["python", "app.py"]